# Hack Wizards - Smart HealthCare Assistant and Smart City Management Portal

## Team Name
**Hack Wizards/team atharvapaymode 11**

## Project Overview

### 1. Smart HealthCare Assistant 

The Smart HealthCare Assistant project is divided into two main portals: Hospital Portal and User Portal. This platform aims to streamline healthcare management for both patients and healthcare providers.

#### 1.1 Hospital Portal [Link: https://smart-healthcare-assistant-prasunethon.streamlit.app/]

**File:** `hospital_app.py`  
**Description:** The Hospital Portal allows hospital administrators to manage doctor profiles and patient appointments effectively.

**Features:**
- **Hospital Signup/Login:** Hospitals can sign up and log in using an admin email and password.
- **Dashboard:** A comprehensive dashboard to manage appointments and doctor profiles.
- **Doctor Management:** Add, edit, and delete doctor profiles.
- **Appointment Management:** View and manage patient appointments.

**Installation:**
```sh
pip install -r requirements.txt
```

#### 1.2 User Portal [Link: https://hospital-management-user.streamlit.app/]

**File:** `app.py`  
**Description:** The User Portal is designed for patients to manage their health and medical appointments.

**Features:**
- **User Signup/Login:** Users can sign up and log in to manage their health data.
- **Health Records:** Maintain and view health records and appointments.
- **Appointment Scheduling:** Schedule appointments with doctors.

**Installation:**
```sh
pip install -r requirements.txt
```

### 2. Smart City Management Portal (Bonus Task - Web Dev) [Link: https://smart-city-management.streamlit.app/]

**File:** `smart_city_management.py`  
**Description:** The Smart City Management Portal is an additional web development task aimed at enhancing city management through efficient resource management, public safety, and citizen engagement.

**Features:**
- **Utilities Monitoring:** Monitor the usage of city resources such as water, electricity, and waste management.
- **Public Safety:** Track surveillance and emergency response routes with detailed descriptions and statuses.
- **Citizen Engagement:** Allow citizens to raise issues and track their status.
- **Admin Panel:** Admin login to update issue statuses and send notifications.

**Installation:**
```sh
pip install -r requirements.txt
```

**Additional Files:**
- **styles.css:** Custom CSS for the Smart City Management Portal.
- **raisedIssues.csv:** CSV file to store raised issues.

## File Structure

```
.
├── 1. Hospital Portal (Smart HealthCare Assistant)
│   ├── .devcontainer
│   │   └── devcontainer.json
│   ├── hospital_app.py
│   ├── requirements.txt
│
├── 2. User Portal (Smart HealthCare Assistant)
│   ├── README.md
│   ├── app.py
│   ├── requirements.txt
│
├── 3. Smart City Management Portal (Bonus Task - Web Dev)
│   ├── raisedIssues.csv
│   ├── requirements.txt
│   ├── smart_city_management.py
│   └── styles.css
```

## How to Run

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo-url
   cd your-repo-url
   ```

2. **Install Dependencies:**
   Navigate to the respective directory (Hospital Portal, User Portal, or Smart City Management Portal) and run:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```sh
   streamlit run hospital_app.py   # For Hospital Portal
   streamlit run app.py            # For User Portal
   streamlit run smart_city_management.py  # For Smart City Management Portal
   ```

## Team Members
- Pratap Pawar
- Atharva Awatade
- Atharva Paymode

We hope you find our Smart HealthCare Assistant and Smart City Management Portal projects useful. For any questions or contributions, feel free to reach out to our team.
