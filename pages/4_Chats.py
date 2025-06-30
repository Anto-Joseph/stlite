import streamlit as st 

# ---- INITIALIZE CHAT HISTORY --- 

if "messages" not in st.session_state :
    st.session_state.messages = []

#  ---- DISPLAY CHAT MESSAGE FROM HISTORY ON APP RUN ----

for message  in st.session_state.messages :
    with st.chat_message(message["role"]) :
        st.markdown(message["content"])

# ---- REACT TO USER INPUT ----
if prompt := st.chat_input("Message") :
    # ---- DISPLAY USER MESSAGE IN CHAT MESSAGE CONTAINER ----
    with st.chat_message("user") :
        st.markdown(prompt)
    # ---- ADD USER MESSAGE TO CHAT HISTORY ----
    st.session_state.messages.append({"role" : "user", "content" : prompt})

    response = f"Echo : {prompt}"

    # ---- DISPLAY ASSISTANT RESPONSE IN CHAT MESSAGE CONTAINER ----

    with st.chat_message("assistant"):
        st.markdown(response)
    # ----- ADD ASSISTANT RESPONSE TO CHAT HISTORY ----
    st.session_state.messages.append({"role" :"assistant", "content" : response})