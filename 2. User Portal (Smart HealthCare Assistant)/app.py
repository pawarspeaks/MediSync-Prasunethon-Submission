import streamlit as st
from pymongo import MongoClient
import bcrypt
import uuid
from datetime import datetime, time
from streamlit_cookies_manager import EncryptedCookieManager
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Timer
import os  # Import os module for environment variables

# Fetch OpenAI API Key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize cookies manager with a password
password = "your_secret_password"  # Replace with a secure password
cookies = EncryptedCookieManager(
    password=password, 
    prefix="app"
)

# Initialize OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)

# MongoDB Connection
client_mongo = MongoClient('mongodb+srv://atharva2021:123@cluster0.so5reec.mongodb.net/')
db = client_mongo['HospitalManagement']
users_collection = db['user']
raisedappointment_collection = db['raisedappointment']

# Email setup
email_user = 'odop662@gmail.com'
email_pass = 'zykvuppkoznmpgzn'

# Utility functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def user_signup(user_data):
    user_data['password'] = hash_password(user_data['password'])
    users_collection.insert_one(user_data)

def user_login(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password(password, user['password']):
        return True, username, user.get('name', '')
    return False, None, None

def generate_token():
    return str(uuid.uuid4())

@st.cache_data
def insert_appointment_data(appointment_data):
    try:
        result = raisedappointment_collection.insert_one(appointment_data)
        if result.acknowledged:
            return True
        else:
            st.error("Failed to schedule the appointment")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def save_user_session(username, name):
    cookies["user"] = username
    cookies["name"] = name
    cookies["token"] = generate_token()
    cookies.save()

def load_user_session():
    return cookies.get("user"), cookies.get("token"), cookies.get("name")

def clear_session():
    cookies["user"] = ""
    cookies.save()

def get_chatbot_response(prompt):
    user, _, username = load_user_session()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return f"Hello {username}, {answer}"

def schedule_email(to_email, subject, body, send_time):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    def send_email():
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_pass)
            text = msg.as_string()
            server.sendmail(email_user, to_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    delay = (send_time - datetime.now()).total_seconds()
    Timer(delay, send_email).start()

# Streamlit Pages
def main():
    st.markdown(
        """
        <style>
            body {
                background-color: #f0f2f6;
                font-family: 'Arial', sans-serif;
            }
            .main {
                background-color: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-top: 2rem;
            }
            .sidebar .sidebar-content {
                background-color: #002b36;
                color: white;
            }
            h1 {
                color: #333;
            }
            h2, h3 {
                color: #555;
            }
            label {
                color: #666;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 16px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Smart Healthcare Assistant")

    menu = ["User Login", "User Signup", "Schedule Appointment", "Medication Reminder", "Chatbot", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "User Login":
        st.subheader("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            success, user, name = user_login(username, password)
            if success:
                st.success(f"Welcome {username}")
                save_user_session(username, name)
            else:
                st.error("Invalid username or password")

    elif choice == "User Signup":
        st.subheader("Create a New User Account")
        with st.form("signup_form"):
            username = st.text_input("Username")
            age = st.number_input("Age", min_value=0)
            city = st.text_input("City")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            comorbidities = st.text_area("Comorbidities (separate by commas)")
            past_medical_history = st.text_area("Past Medical History")
            special_disability = st.text_area("Special Disability")
            contact_number = st.text_input("Contact Number")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            preferred_language = st.selectbox("Preferred Language", ["English", "Spanish", "Other"])
            primary_care_physician = st.text_input("Primary Care Physician")
            primary_care_physician_contact = st.text_input("Primary Care Physician Contact (Optional)")

            if st.form_submit_button("Signup"):
                user_data = {
                    "username": username,
                    "name": username,  # Use the username as the name for now
                    "age": age,
                    "city": city,
                    "gender": gender,
                    "comorbidities": comorbidities,
                    "past_medical_history": past_medical_history,
                    "special_disability": special_disability,
                    "contact_number": contact_number,
                    "email": email,
                    "password": password,
                    "preferred_language": preferred_language,
                    "primary_care_physician": primary_care_physician,
                    "primary_care_physician_contact": primary_care_physician_contact
                }
                user_signup(user_data)
                st.success("You have successfully created a new user account")

    elif choice == "Schedule Appointment":
        st.subheader("Schedule an Appointment")
        user, _, _ = load_user_session()
        if user:
            organizations = db.organization.distinct("organization_name")
            organization_name = st.selectbox("Organization Name", organizations)

            if organization_name:
                organization = db.organization.find_one({"organization_name": organization_name})
                if organization:
                    doctors = [doc['doctor_name'] for doc in organization['doctors']]
                    doctor_name = st.selectbox("Doctor Name", doctors)
                    specializations = [doc['doctor_specialist'] for doc in organization['doctors']]
                    specialization = st.selectbox("Specialization", specializations)

                    appointment_date = st.date_input("Appointment Date", min_value=datetime.today().date())
                    appointment_time = st.time_input("Appointment Time", value=time(9, 0))

                    email = st.text_input("Email")  # Add email input field if necessary

                    if st.button("Schedule"):
                        appointment_data = {
                            "Organization Name": organization_name,
                            "Doctor Name": doctor_name,
                            "Specialization": specialization,
                            "Appointment Date": appointment_date.strftime("%Y/%m/%d"),
                            "Appointment Time": appointment_time.strftime("%H:%M"),
                            "Email": email,
                            "Status": "Pending"
                        }
                        if insert_appointment_data(appointment_data):
                            st.success("Appointment scheduled successfully")
                        else:
                            st.error("Failed to schedule the appointment")
                else:
                    st.error("Organization not found")
        else:
            st.error("Please login to schedule an appointment")

    elif choice == "Medication Reminder":
        st.subheader("Schedule Medication Reminder")
        user, _, _ = load_user_session()
        if user:
            with st.form("medication_form"):
                medication_name = st.text_input("Medication Name")
                dosage = st.text_input("Dosage")
                frequency = st.text_input("Frequency (e.g., once a day, twice a day)")
                reminder_date = st.date_input("Reminder Date", min_value=datetime.today().date())
                reminder_time = st.time_input("Reminder Time", value=time(9, 0))
                email = st.text_input("Email")

                if st.form_submit_button("Schedule Reminder"):
                    reminder_datetime = datetime.combine(reminder_date, reminder_time)
                    body = f"Reminder to take your medication:\n\nMedication Name: {medication_name}\nDosage: {dosage}\nFrequency: {frequency}\n\nPlease take it on time."
                    schedule_email(email, "Medication Reminder", body, reminder_datetime)
                    st.success("Medication reminder scheduled successfully")

    elif choice == "Chatbot":
        st.subheader("Chatbot")
        user_input = st.text_input("You: ")
        if user_input:
            response = get_chatbot_response(user_input)
            st.write(f"Bot: {response}")

    elif choice == "Logout":
        clear_session()
        st.success("You have been logged out")

    user, _, _ = load_user_session()
    if user:
        st.sidebar.success(f"Logged in as: {user}")

if __name__ == '__main__':
    main()
