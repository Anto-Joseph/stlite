import streamlit as st 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

#st.set_page_config(layout="wide")
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    auto_hash=True
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)


if st.session_state.get('authentication_status'):
    st.title(f'Welcome *{st.session_state.get("name")}*')
    st.write(f'Role :*{st.session_state.get("roles")}*')
    authenticator.logout()

elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')