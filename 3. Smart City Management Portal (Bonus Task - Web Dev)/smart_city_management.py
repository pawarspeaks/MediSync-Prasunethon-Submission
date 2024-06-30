import streamlit as st
import pandas as pd
import os
import tempfile
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import plotly.express as px
import requests

# Set Streamlit page configuration (move this to the beginning)
st.set_page_config(page_title="Smart City Management System", layout="wide")

# Function to load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS (assuming styles.css is in the same directory as your script)
load_css('styles.css')

# Include Mapbox GL JS CSS
st.markdown('<link href="https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css" rel="stylesheet">', unsafe_allow_html=True)

# Initialize or load the CSV file
csv_file = 'raisedIssues.csv'

def load_csv(csv_file):
    if not os.path.exists(csv_file):
        # Create a new CSV file with columns
        df = pd.DataFrame(columns=['Issue Type', 'Description', 'Location', 'Status', 'Date Reported', 'Email'])
        df.to_csv(csv_file, index=False)
    else:
        # Load existing data
        df = pd.read_csv(csv_file)
        # Ensure 'Date Reported' and 'Email' columns exist
        if 'Date Reported' not in df.columns:
            df['Date Reported'] = pd.NaT
        if 'Email' not in df.columns:
            df['Email'] = ''
    return df

df = load_csv(csv_file)

# Function to send email notifications
def send_email(receiver_email, message):
    sender_email = "atharvapaymode11@gmail.com"  # Replace with your email address
    password = "ltgv wbjh yufs owxk"  # Replace with your email password or app-specific password

    # Check if receiver_email is a valid string and not NaN
    if isinstance(receiver_email, str) and receiver_email:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Smart City Management System Notification"
        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()  # Secure the connection
                smtp.login(sender_email, password)
                smtp.send_message(msg)
            st.success(f"Email sent to {receiver_email}")
        except Exception as e:
            st.error(f"Failed to send email to {receiver_email}: {e}")

# Function to automatically update issue status based on a condition
def auto_update_issue_status(df, csv_file):
    if 'Date Reported' in df.columns:
        df['Date Reported'] = pd.to_datetime(df['Date Reported'], errors='coerce')
        condition = datetime.now() - df['Date Reported'] > timedelta(days=7)
        df.loc[condition, 'Status'] = 'In Progress'

        # Send reminders to users with issues in progress
        issues_in_progress = df[df['Status'] == 'In Progress']
        for idx, row in issues_in_progress.iterrows():
            if row['Email']:
                send_email(row['Email'], f"Reminder: Your issue '{row['Issue Type']}' is in progress!")

        # Save the updated DataFrame to a temporary file, then replace the original
        temp_csv = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv')
        try:
            df.to_csv(temp_csv.name, index=False)
            temp_csv.close()
            shutil.move(temp_csv.name, csv_file)
        except Exception as e:
            st.error(f"Error saving CSV: {e}")
        finally:
            if os.path.exists(temp_csv.name):
                os.remove(temp_csv.name)

# Function to authenticate admin login
def admin_login(username, password):
    # Hardcoded admin credentials (replace with secure storage or database lookup)
    admin_username = "admin"
    admin_password = "admin@123"

    if username == admin_username and password == admin_password:
        return True
    else:
        return False

# Update statuses automatically when the app starts
auto_update_issue_status(df, csv_file)

# Sample data for surveillance and emergency response routes (replace with actual data)
routes_data = {
    'Route Name': ['Route A', 'Route B', 'Route C'],
    'Start Location': ['Gateway of India', 'Juhu Beach', 'Siddhivinayak Temple'],
    'End Location': ['Chhatrapati Shivaji Maharaj Terminus', 'Marine Drive', 'Haji Ali Dargah'],
    'Status': ['Active', 'Inactive', 'Active'],
    'Latitude': [18.9217, 19.1006, 19.0177],  # Updated Latitude values for popular tourist spots in Mumbai
    'Longitude': [72.8349, 72.8265, 72.8162]  # Updated Longitude values for popular tourist spots in Mumbai
}

# Detailed descriptions and coordinates for tourist spots in Mumbai
tourist_locations = {
    "Gateway of India": {
        "description": "A historic monument and iconic landmark overlooking the Arabian Sea.",
        "coordinates": [18.9217, 72.8349]
    },
    "Marine Drive (Queen's Necklace)": {
        "description": "A picturesque promenade along the coastline, offering stunning views of the sea.",
        "coordinates": [18.9500, 72.8230]
    },
    "Elephanta Caves": {
        "description": "Located on Elephanta Island, these ancient rock-cut caves are renowned for their sculptures and UNESCO World Heritage status.",
        "coordinates": [18.9647, 72.9313]
    },
    "Chhatrapati Shivaji Maharaj Terminus (CSMT)": {
        "description": "Formerly known as Victoria Terminus, this UNESCO-listed railway station is a masterpiece of Victorian Gothic architecture.",
        "coordinates": [18.9401, 72.8353]
    },
    "Juhu Beach": {
        "description": "A popular beach destination where locals and tourists alike gather to relax and enjoy Mumbai's vibrant atmosphere.",
        "coordinates": [19.1006, 72.8270]
    },
    "Haji Ali Dargah": {
        "description": "A mosque and tomb located on an islet off the coast of Worli, accessible via a causeway during low tide.",
        "coordinates": [18.9829, 72.8154]
    },
    "Siddhivinayak Temple": {
        "description": "A revered Hindu temple dedicated to Lord Ganesha, attracting a large number of devotees.",
        "coordinates": [19.0177, 72.8300]
    },
    "Sanjay Gandhi National Park": {
        "description": "Located in the northern part of Mumbai, this park offers a refreshing escape from the city with lush greenery, hiking trails, and the Kanheri Caves.",
        "coordinates": [19.2143, 72.9106]
    },
    "Colaba Causeway": {
        "description": "A bustling street market in South Mumbai offering a variety of goods including clothing, jewelry, and souvenirs.",
        "coordinates": [18.9157, 72.8258]
    },
    "Bandra-Worli Sea Link": {
        "description": "An engineering marvel connecting Bandra and Worli, offering panoramic views of the Mumbai skyline and Arabian Sea.",
        "coordinates": [19.0300, 72.8154]
    },
    "Nehru Centre and Planetarium": {
        "description": "A science and cultural center featuring interactive exhibits, a planetarium, and art galleries.",
        "coordinates": [19.0227, 72.8462]
    },
    "Film City (Goregaon)": {
        "description": "Where Bollywood movies are filmed, offering tours to visitors interested in the Indian film industry.",
        "coordinates": [19.1551, 72.8648]
    },
    "Chowpatty Beach": {
        "description": "Known for its lively atmosphere, street food stalls, and festivals like Ganesh Chaturthi where large idols of Lord Ganesha are immersed in the sea.",
        "coordinates": [18.9553, 72.8089]
    },
    "Bollywood Studios": {
        "description": "Various studios across Mumbai offer tours where visitors can get a glimpse into the world of Bollywood.",
        "coordinates": [19.1195, 72.9057]
    },
    "Mahalakshmi Temple": {
        "description": "A famous temple dedicated to Goddess Mahalakshmi, known for its unique architecture and religious significance.",
        "coordinates": [18.9823, 72.8244]
    }
}

# Update routes DataFrame with detailed descriptions and coordinates
routes_df = pd.DataFrame(routes_data)
routes_df['Description'] = routes_df['Start Location'].apply(lambda loc: tourist_locations[loc]['description'])
routes_df['Latitude'] = routes_df['Start Location'].apply(lambda loc: tourist_locations[loc]['coordinates'][0])
routes_df['Longitude'] = routes_df['Start Location'].apply(lambda loc: tourist_locations[loc]['coordinates'][1])

# Function to update routes dynamically
def update_routes_data():
    # Implement logic to update routes dynamically (e.g., from a database or API)
    pass

# Function to calculate travel time using OpenRouteService API
def calculate_travel_time(start_location, end_location):
    url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    params = {
        'api_key': '5b3ce3597851110001cf6248396905cf657f4f13902098e82e693da9',  # Replace with your OpenRouteService API key
        'start': f'{start_location[1]},{start_location[0]}',  # Latitude, Longitude
        'end': f'{end_location[1]},{end_location[0]}'  # Latitude, Longitude
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'features' in data and len(data['features']) > 0:
            # Extract route details
            route = data['features'][0]
            duration_sec = route['properties']['segments'][0]['duration']  # Duration in seconds
            duration_min = round(duration_sec / 60, 2)  # Convert seconds to minutes
            
            # Extract route geometry for visualization (if needed)
            route_geometry = route['geometry']
            
            return duration_min
        else:
            st.error("No routes found. Please check the locations and try again.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error calculating travel time: {e}")
        return None

# Example usage in your Streamlit app
start_location = (18.9696, 72.8194)  # Mumbai Central
end_location = (19.0208, 72.8426)  # Dadar

travel_time = calculate_travel_time(start_location, end_location)
if travel_time is not None:
    print(f"Estimated travel time from Mumbai Central to Dadar: {travel_time} minutes")
else:
    print("Failed to calculate travel time. Please try again later.")


# Page navigation
page = st.sidebar.selectbox("Choose a page", ["Home", "All Raised Issues", "Admin"])

if page == "Home":
    st.title("Smart City Management System")

    # Efficient Resource Management Section
    st.header("Efficient Resource Management")

    with st.expander("Utilities Monitoring"):
        # Simulated data display for utilities
        resource_data = {
            'Resource': ['Water', 'Electricity', 'Waste'],
            'Usage': [1200, 3500, 900],
            'Unit': ['Liters', 'kWh', 'kg']
        }
        resource_df = pd.DataFrame(resource_data)
        st.table(resource_df)

        # Interactive chart for resource usage
        fig_resource = px.bar(resource_df, x='Resource', y='Usage', color='Resource', title='Resource Usage')
        st.plotly_chart(fig_resource)

    # Public Safety Section
    st.header("Public Safety")

    with st.expander("Surveillance and Emergency Response"):
        # Combine public safety data and routes data for the map
        combined_data = routes_df

        # Use Plotly Express to create the map
        fig_map = px.scatter_mapbox(combined_data, lat='Latitude', lon='Longitude', hover_name='Start Location',
                                    color='Status', zoom=11, height=600, width=800)

        # Customize map layout and initial center for Mumbai
        fig_map.update_layout(mapbox_style="open-street-map",
                              mapbox_center={"lat": 19.0760, "lon": 72.8777},  # Centered on Mumbai
                              mapbox_zoom=11)  # Adjust zoom level as needed
        st.plotly_chart(fig_map)

        # Display table with surveillance and emergency response routes
        st.subheader('Surveillance and Emergency Response Routes in Mumbai')
        st.dataframe(routes_df[['Start Location', 'End Location', 'Status', 'Description']])

        # Calculate and display travel time between selected locations
        st.subheader("Calculate Travel Time")
        start_location = st.selectbox("Select Start Location", routes_df['Start Location'])
        end_location = st.selectbox("Select End Location", routes_df['End Location'])

        if st.button("Calculate"):
            if start_location and end_location:
                start_coords = tourist_locations[start_location]['coordinates']
                end_coords = tourist_locations[end_location]['coordinates']

                travel_time = calculate_travel_time(start_coords, end_coords)
                if travel_time is not None:
                    st.success(f"Estimated travel time from {start_location} to {end_location}: {travel_time} minutes")
                else:
                    st.error("Failed to calculate travel time. Please try again later.")
            else:
                st.warning("Please select both start and end locations.")

    # Citizen Engagement Section
    st.header("Citizen Engagement")

    # Layout for raising an issue and displaying all issues side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Raise an Issue")

        issue_type = st.selectbox("Issue Type", ["Road Maintenance", "Street Lighting", "Garbage Collection"])
        description = st.text_area("Description")
        location = st.text_input("Location")
        email = st.text_input("Email (optional)")

        if st.button("Submit Issue"):
            if issue_type and description and location:
                new_issue = {
                    'Issue Type': issue_type,
                    'Description': description,
                    'Location': location,
                    'Status': 'Pending',
                    'Date Reported': datetime.now(),
                    'Email': email
                }
                df = df.append(new_issue, ignore_index=True)

                # Save to CSV using a temporary file
                temp_csv = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv')
                try:
                    df.to_csv(temp_csv.name, index=False)
                    temp_csv.close()
                    shutil.move(temp_csv.name, csv_file)
                    st.success("Issue submitted successfully!")
                    # Send confirmation email if email is provided
                    if email:
                        send_email(email, f"Thank you for submitting your issue '{issue_type}'. We will keep you updated!")
                except Exception as e:
                    st.error(f"Error saving CSV: {e}")
                finally:
                    if os.path.exists(temp_csv.name):
                        os.remove(temp_csv.name)
            else:
                st.error("Please fill in all fields (email is optional).")

    with col2:
        st.subheader("Update Issue Status")

        if len(df) > 0:
            issue_index = st.number_input("Issue Index to Update", min_value=1, max_value=len(df), step=1) - 1
            new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])

            if st.button("Update Status"):
                if 0 <= issue_index < len(df):
                    if new_status == "Resolved" and not admin_login(st.text_input("Admin Username"), st.text_input("Admin Password", type="password")):
                        st.error("Only admin can update issue status to Resolved.")
                    else:
                        df.at[issue_index, 'Status'] = new_status
                        # Save to CSV using a temporary file
                        temp_csv = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv')
                        try:
                            df.to_csv(temp_csv.name, index=False)
                            temp_csv.close()
                            shutil.move(temp_csv.name, csv_file)
                            st.success(f"Issue {issue_index + 1} status updated to {new_status}")
                        except Exception as e:
                            st.error(f"Error saving CSV: {e}")
                        finally:
                            if os.path.exists(temp_csv.name):
                                os.remove(temp_csv.name)
                else:
                    st.error("Invalid issue index")
        else:
            st.write("No issues to update.")

    # Access City Services Section
    st.header("Access City Services")

    with st.expander("Public Transport"):
        # Simulated data display for public transport
        public_transport_data = {
            'Route': ['A', 'B', 'C'],
            'Frequency': ['10 min', '15 min', '20 min'],
            'Capacity': [100, 120, 80]
        }
        public_transport_df = pd.DataFrame(public_transport_data)
        st.table(public_transport_df)

        # Interactive line chart for public transport frequency
        fig_transport = px.line(public_transport_df, x='Route', y='Frequency', title='Public Transport Frequency')
        st.plotly_chart(fig_transport)

elif page == "All Raised Issues":
    st.title("All Raised Issues")

    # Display all raised issues
    if len(df) > 0:
        for idx, row in df.iterrows():
            st.subheader(f"Issue Index {idx + 1}")
            st.write(f"Issue Type: {row['Issue Type']}")
            st.write(f"Description: {row['Description']}")
            st.write(f"Location: {row['Location']}")
            st.write(f"Status: {row['Status']}")
            st.write(f"Date Reported: {row['Date Reported']}")
            st.write(f"Email: {row['Email']}")
            st.write("---")
    else:
        st.write("No issues have been raised yet.")

elif page == "Admin":
    st.title("Admin Section")

    st.subheader("Login to Admin Panel")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if admin_login(username, password):
            st.success("Logged in as admin.")
            st.subheader("Update Issue Status")

            if len(df) > 0:
                issue_index = st.number_input("Issue Index to Update", min_value=1, max_value=len(df), step=1) - 1
                new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])

                if st.button("Update Status"):
                    if 0 <= issue_index < len(df):
                        df.at[issue_index, 'Status'] = new_status
                        # Save to CSV using a temporary file
                        temp_csv = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv')
                        try:
                            df.to_csv(temp_csv.name, index=False)
                            temp_csv.close()
                            shutil.move(temp_csv.name, csv_file)
                            st.success(f"Issue {issue_index + 1} status updated to {new_status}")
                        except Exception as e:
                            st.error(f"Error saving CSV: {e}")
                        finally:
                            if os.path.exists(temp_csv.name):
                                os.remove(temp_csv.name)
                    else:
                        st.error("Invalid issue index")
            else:
                st.write("No issues to update.")
        else:
            st.error("Invalid credentials. Please try again.")

else:
    st.error("Page not found. Please select a valid page.")
