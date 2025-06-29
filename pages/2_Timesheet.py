import streamlit as st
import datetime
import streamlit_authenticator as stauth

st.title('Daily Timesheet')
st.write(f'Entered By : *{st.session_state.get("name")}*')


T_date = st.date_input("Select Input date")


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)