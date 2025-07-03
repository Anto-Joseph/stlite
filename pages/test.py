import streamlit as st
import datetime
import streamlit_authenticator as stauth
import pandas as pd
import sqlite3
import time
import uuid


# ---- VARIABLE ----
st.title('Daily Work Sheet')
AddedByUser = st.session_state.get("name")

# --- DATABASE CONNECTION ---

con = sqlite3.connect("database-1.db")
cursor =  con.cursor()


# ---- FUNCTIONS ---

  # ---- TABLE CHANGE -----
def process_changes():
    editor_state = st.session_state.get("EmpTaskTbl_Key", {})
    edited = editor_state.get("edited_rows",{})
    added = editor_state.get("added_rows",{})
    deleted = editor_state.get("deleted_rows",{})


    # ---- ADD DATA TO DATABASE ---

    added = pd.DataFrame.from_dict(added)
    added['TaskDate'] = A_date
    if not added.empty:
      try:
        data_add = pd.merge(added, df_taskList, how="inner", on=["TaskDescription"])
        data_add = pd.merge(data_add, df_empList, how="inner", on=["EmpName"])
        data_add = data_add.filter(['EmpID','TaskID','TaskDate','Comments','EnteredBy','TaskDate'])
        data_add.set_index('EmpID')
        data_add.to_sql(name='EMPTASK', if_exists="append", con = con, index=False)
      except sqlite3.Error as error:
        df_EmpAct = df_AllEmpActList.filter(['TaskEmpID','EmpName','TaskDescription', 'Comments', 'EnteredBy','TaskDate'], axis=1)
        st.write(empTaskDatabase_df)
        data_add.set_index('EmpID')
        st.write(data_add)
        inner_merged = pd.merge(empTaskDatabase_df["EmpID"], data_add["EmpID"], on=["EmpID"], how='inner')
        st.write(inner_merged)




    # ---- DELETE DATA FROM TABLE ---
    deletedList = editor_state.get("deleted_rows",{})
    deleted_df = df_EmpAct.iloc[deletedList]
    deleteListToQuery = []
    for delID in deleted_df['TaskEmpID'].to_list() :
      deleteListToQuery.append((delID,))
    del_query = """DELETE from EMPTASK where TaskEmpID = ?"""
    cursor.executemany(del_query, deleteListToQuery)
    con.commit()
     

    




  # ---- POP UP WINDOW -----

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
df_EmpAct = df_AllEmpActList.filter(['TaskEmpID','EmpName','TaskDescription', 'Comments', 'EnteredBy','TaskDate'], axis=1)
EmpList = df_empList["EmpName"]
TaskList = df_taskList["TaskDescription"].to_list()


# ----- Table -----

edited_df = st.data_editor(
    df_EmpAct,
    key = "EmpTaskTbl_Key",
    use_container_width = True,
    on_change =  process_changes,
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

    },

    column_order=("EmpName", "TaskDescription","Comments","EnteredBy"),

)
