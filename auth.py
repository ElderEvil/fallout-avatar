import requests
import streamlit as st

FASTAPI_URL = "http://elderevil.net:30008/api/v1"


# Function to log in with FastAPI
def authenticate(email, password):
    url = f"{FASTAPI_URL}/login/access-token"
    data = {"grant_type": "password", "username": email, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    return None


# Function to register users via FastAPI
def register_user(username, password, email):
    url = f"{FASTAPI_URL}/users/open"
    user_data = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=user_data)

    return response.status_code == 200


# Authentication handler with toggle
def authenticate_user():
    st.sidebar.title("🔐 Authentication")

    auth_mode = st.sidebar.radio("Select Mode", ["Login", "Register"])

    if auth_mode == "Login":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        login_btn = st.sidebar.button("Login")

        if login_btn:
            auth_response = authenticate(email, password)
            if auth_response:
                st.session_state["auth_token"] = auth_response["access_token"]
                st.session_state["email"] = email
                st.sidebar.success(f"Welcome, {email}!")
            else:
                st.sidebar.error("Invalid credentials")

    elif auth_mode == "Register":
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        new_email = st.sidebar.text_input("Email")
        register_btn = st.sidebar.button("Register")

        if register_btn:
            if register_user(new_username, new_password, new_email):
                st.sidebar.success("Registration successful! Please log in.")
            else:
                st.sidebar.error("Registration failed. Try again.")

    # Logout button
    if "auth_token" in st.session_state:
        if st.sidebar.button("Logout"):
            st.session_state.pop("auth_token", None)
            st.session_state.pop("email", None)
            st.sidebar.success("Logged out successfully!")
