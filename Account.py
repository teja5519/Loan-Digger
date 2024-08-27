import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Replace with your service account key path
cred = credentials.Certificate("loan-digger-analysis-a7fdf8b046e7.json")
firebase_admin.initialize_app(cred)

def app():
    st.title("Welcome to Loan Digger Application")
    choice = st.selectbox('Login/Signup', ['Sign Up'])

    if choice == 'Sign Up':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input('Enter your unique username')

        if st.button('Create my account'):
            try:
                user = auth.create_user(email=email, password=password, uid=username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
            except Exception as e:
                st.error(f"Account creation failed: {e}")

    # ... other logic ...

if __name__ == "__main__":
    app()
