import streamlit as st
import datetime
import streamlit_authenticator as stauth
import pandas as pd
import sqlite3
st.title('Daily Work Sheet')
# --- DATABASE CONNECTION ---

con = sqlite3.connect("database.db")


# --- ---

@st.dialog("Add Employye", width="large")
def AddEmpAct(ActDate):
    st.write(f"Add Emplye for {ActDate}")
    newEmp = st.selectbox(
    "Select Employee",
    ("Email", "Home phone", "Mobile phone"),
    index=None,
    placeholder="Employee Name",
)
    newAct = st.selectbox(
    "Select Activity",
    ("Email", "Home phone", "Mobile phone"),
    index=None,
    placeholder="Activity",
)
    if st.button("Submit"):
        #st.session_state.vote = {"newEmp": newEmp, "newAct": newAct}
        st.rerun()


A_date = st.date_input("Select Input date")
if st.button("Add New", icon="➕") :
    AddEmpAct(A_date)

# ----- Table Data ---- 

df = pd.read_sql_query("SELECT EmpID,EmpName from EMP", con)

res = cursor.execute("SELECT EmpName FROM EMP")
df = pd.DataFrame(res.fetchall())


df_EmpAct = pd.DataFrame(
    [
       {"command": 'Admin', "Activity": "x", "Comments" : "Jamie Lawlore - Snagging Level 2.0"},
       {"command": 'Lar Murphy', "Activity": "Lar Murphy", "Comments" : ""},
       {"command": 'Joe Finnegan', "Activity": "Joe Finnegan", "Comments" : "fdfsdf"},
   ]
)

EmpList = df[0].to_list()
ActList = ['anto','Joe','tojo','goe','leo']

# ----- Table -----

edited_df = st.data_editor(
    df_EmpAct, 
    num_rows="dynamic",
    column_config= {
        "command" : st.column_config.SelectboxColumn("Employye Name", 
                                                      width = 'Medium', 
                                                      options= EmpList,
                                                      required=True,
                                                    ),
      "Activity" : st.column_config.SelectboxColumn("Activity",
                                                     width = 'large', 
                                                     options= ActList,
                                                     required=True,
                                                   ),
      "Comments" : st.column_config.Column("Comments", width = 'large',),

    },

)
