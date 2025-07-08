import streamlit as st
import pandas as pd
import sqlite3

st.session_state.data = []
# --- DATABASE CONNECTION ---

con = sqlite3.connect("database-1.db")
cursor =  con.cursor()


def process_changes():
    data_add = []
    editor_state = st.session_state.get("EmpTaskTbl_Key", {})
    edited = editor_state.get("edited_rows",{})
    added = editor_state.get("added_rows",{})
    deleted = editor_state.get("deleted_rows",{})

    # ---- ADD DATA TO DATABASE ---




    # ---- DELETE DATA FROM TABLE ---
    deletedList = editor_state.get("deleted_rows",{})
    deleted_df = df_EmpAct.iloc[deletedList]
    deleteListToQuery = []
    for delID in deleted_df['TaskEmpID'].to_list() :
        deleteListToQuery.append((delID,))
    del_query = """DELETE from EMPTASK where TaskEmpID = ?"""
    cursor.executemany(del_query, deleteListToQuery)
    con.commit()



st.title("This is a title")
# ---- input date ----
A_date = st.date_input("Select Input date")

# ----- TABLE DATA ---- 
df_AllEmpActList = pd.read_sql_query(f"SELECT * from View_EmpTaskSheet WHERE TaskDate = '{A_date}'", con)
st.session_state.data = pd.read_sql_query(f"SELECT * from View_EmpTaskSheet WHERE TaskDate = '{A_date}'", con)
df_EmpAct = st.session_state["data"].copy()

# ---- Emp List list for dropdown from DB ----
df_empList = pd.read_sql_query("SELECT EmpID,EmpName,EmpStatus,EmpDesignation from EMP", con)
EmpList = df_empList["EmpName"]

# ---- Task list for dropdown from DB ----
df_taskList = pd.read_sql_query("SELECT * from TASK", con)
TaskList = df_taskList["TaskDescription"].to_list()


# ----- TABLE EDITOR  RENDER -----

edited_df = st.data_editor(
    st.session_state["data"],
    key = "EmpTaskTbl_Key",
    on_change =  process_changes,
    num_rows="dynamic",
    column_config= {
        "EmpName" : st.column_config.SelectboxColumn("Employye Name", 
                                                      options= EmpList,
                                                      required=True,
                                                    ),
      "TaskDescription" : st.column_config.SelectboxColumn("Activity",
                                                     options= TaskList,
                                                     required=True,
                                                   ),
      "Comments" : st.column_config.Column("Comments",),
      "EnteredBy" : st.column_config.TextColumn("Widgets", default= st.session_state.get("name")),

    },

    column_order=("EmpName", "TaskDescription","Comments","EnteredBy"),

)

print("xxx")
print(st.session_state.get("EmpTaskTbl_Key"))
