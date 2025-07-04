# source tutorial-env/bin/activate
import streamlit as st 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


if st.session_state.get('authentication_status') is None:
    st.title("XYZ Company Name")
    pages = [st.Page("pages/1_Login.py", title="Create your account")]
    pg = st.navigation(pages)
    pg.run()

elif st.session_state.get('roles') == 'admin' :
    st.write(f" *{st.session_state.get('name')}*")
    pages = {
    "Dasboards" : [
        st.Page("pages/1_Login.py", title = "Home Login Page"),
        st.Page("pages/2_Timesheet.py", title = "Add Timesheet"),
    ],

    "Manage Timeshhets" : [
        st.Page("pages/3_ActivitySheet.py", title = "Daily Activity"),
        st.Page("pages/4_Chats.py", title = "Messages"),
        st.Page("pages/test.py", title = "Testing"),
        st.Page("pages/test2.py", title = "Testing2"),
    ],
}

    pg = st.navigation(pages)
    pg.run()

elif st.session_state.get('roles') == 'supervisor' :
    st.title(f"*{st.session_state.get('name')}*")
    pages = {
    "Dasboards" : [
        st.Page("pages/1_Login.py", title = "Home Login Page"),
    ],

    "Manage Timeshhets" : [
        st.Page("pages/3_ActivitySheet.py", title = "Daily Activity"),
        st.Page("pages/4_Chats.py", title = "Messages"),
    ],
}

    pg = st.navigation(pages)
    pg.run()

    
    


else :
    st.title(f"Welcome *{st.session_state.get('name')}*")
    pages = [st.Page("pages/1_Login.py", title="Create your account")]
    pg = st.navigation(pages)
    pg.run()