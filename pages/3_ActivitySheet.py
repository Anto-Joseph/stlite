import streamlit as st
import datetime
import streamlit_authenticator as stauth
import pandas as pd
import sqlite3


st.title('Daily Work Sheet')
AddedByUser = st.session_state.get("name")
# --- DATABASE CONNECTION ---

con = sqlite3.connect("database-1.db")


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

# ---- input date ----
A_date = st.date_input("Select Input date")
if st.button("Add New", icon="➕") :
    AddEmpAct(A_date)

# ----- Table Data ---- 

df_empList = pd.read_sql_query("SELECT EmpID,EmpName,EmpStatus,EmpDesignation from EMP", con)
df_taskList = pd.read_sql_query("SELECT * from TASK", con)
df_AllEmpActList = pd.read_sql_query(f"SELECT * from View_EmpTaskSheet WHERE TaskDate = '{A_date}'", con)
df_EmpAct = df_AllEmpActList.filter(['TaskEmpID','EmpName','TaskDescription', 'Comments', 'EnteredBy'], axis=1)
EmpList = df_empList["EmpName"]
TaskList = df_taskList["TaskDescription"].to_list()


# ----- Table -----

edited_df = st.data_editor(
    df_EmpAct, 
    num_rows="dynamic",
    column_config= {
        "EmpName" : st.column_config.SelectboxColumn("Employye Name", 
                                                      width = 'Medium', 
                                                      options= EmpList,
                                                      required=True,
                                                    ),
      "TaskDescription" : st.column_config.SelectboxColumn("Activity",
                                                     width = 'large', 
                                                     options= TaskList,
                                                     required=True,
                                                   ),
      "Comments" : st.column_config.Column("Comments", width = 'large',),
      "EnteredBy" : st.column_config.TextColumn("Widgets", default= st.session_state.get("name")),
      "TaskDate" : st.column_config.DateColumn(default= A_date ),


    },

    column_order=("EmpName", "TaskDescription","Comments","EnteredBy"),

)

#df_taskList
#df_empList
#edited_df

df_x = pd.merge(edited_df, df_taskList, how="inner", on=["TaskDescription"])
df_x = pd.merge(df_x, df_empList, how="inner", on=["EmpName"])
df_x = df_x.filter(['EmpID','TaskID','TaskDate','Comments','EnteredBy'])


#df_x = df_x.filter(['TaskEmpID','EmpName','TaskDescription','Comments','EnteredBy'])
df_x
df_EmpAct

#compare identical dataframes
#x = df_x.compare(df_EmpAct)



#df.to_sql(name='users', con=engine)
#st.session_state.get("name")