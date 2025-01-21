import streamlit as st
import json
from pathlib import Path

# Utility functions for saving/loading user data
def load_users():
    if not Path("users.json").exists():
        with open("users.json", "w") as file:
            json.dump({}, file)
    with open("users.json", "r") as file:
        return json.load(file)

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

# Enhanced UI and functionality
def login_signup_page():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        .section-header {
            background-color: black;
            color: #2C3333;
            font-size: 1.8em;
            font-weight: 600;
            margin-top: 1em;
            text-align: left;
        }
        
        .auth-container {
            background-color: #CBE4DE;
            padding: 2em;
            border-radius: 10px;
            margin: 2em 0;
            max-width: 500px;
        }
        
        .tab-container {
            margin-bottom: 2em;
        }
        
        .stButton button {
            background-color: #0E8388;
            color: white;
            font-weight: bold;
            width: 100%;
            padding: 0.5em;
            border-radius: 5px;
            border: none;
            margin-top: 1em;
        }
        
        .stButton button:hover {
            background-color: #2E4F4F;
        }
        
        .normal-text {
            font-size: 1.1em;
            color: white;
            line-height: 1.6;
        }
        
        .error-text {
            color: #FF4B4B;
            font-weight: bold;
        }

        .success-text {
            color: #4CAF50;
            font-weight: bold;
        }
        
        .input-label {
            font-weight: bold;
            color: #393E46;
        }
        </style>
    """, unsafe_allow_html=True)

    # Core logic for Login/Signup
    users_db = load_users()

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        # Login Form
        with tab1:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            with st.form("login_form"):
                st.markdown('<h3 style="color: #2E4F4F;">Welcome Back!</h3>', unsafe_allow_html=True)

                email = st.text_input("Email")
                password = st.text_input("Password", type="password")

                remember_me = st.checkbox("Remember me")

                if st.form_submit_button("Login"):
                    if not email or not password:
                        st.error("All fields are required.")
                    elif email not in users_db:
                        st.error("No account found for this email. Please sign up.")
                    elif users_db[email] != password:
                        st.error("Incorrect password. Please try again.")
                    else:
                        st.success(f"Welcome back, {email}!")
                
                st.markdown(""" 
                    <div style="text-align: center; margin-top: 1em;">
                        <a href="#" style="color: #0E8388;">Forgot Password?</a>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Sign Up Form
        with tab2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            with st.form("signup_form"):
                st.markdown('<h3 style="color: #2E4F4F;">Create Account</h3>', unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name")
                with col2:
                    last_name = st.text_input("Last Name")

                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                user_type = st.selectbox("I want to:", ["Buy Materials", "Sell Materials", "Both"])

                terms = st.checkbox("I agree to the Terms and Conditions")

                if st.form_submit_button("Create Account"):
                    if not first_name or not last_name or not email or not password or not confirm_password:
                        st.error("All fields are required.")
                    elif "@" not in email:
                        st.error("Please provide a valid email.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif not terms:
                        st.error("You must accept the Terms and Conditions.")
                    else:
                        if email in users_db:
                            st.error("Email already registered.")
                        else:
                            users_db[email] = password
                            save_users(users_db)
                            st.success("🎉 Account created successfully!")
            st.markdown('</div>', unsafe_allow_html=True)

# Main execution block
if __name__ == "__main__":
    login_signup_page()
