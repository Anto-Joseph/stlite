import streamlit as st
import pandas as pd
import sqlite3


# --- DATABASE CONNECTION ---

con = sqlite3.connect("database-1.db")
cursor =  con.cursor()


def process_changes():
    editor_state = st.session_state.get("EmpTaskTbl_Key", {})
    edited = editor_state.get("edited_rows",{})
    added = editor_state.get("added_rows",{})
    deleted = editor_state.get("deleted_rows",{})

    # ---- ADD DATA TO DATABASE ---

    added = pd.DataFrame.from_dict(added)
    added['TaskDate'] = A_date
    if not added.empty:
        data_add = pd.merge(added, df_taskList, how="inner", on=["TaskDescription"])
        data_add = pd.merge(data_add, df_empList, how="inner", on=["EmpName"])
        data_add = data_add.filter(['EmpID','TaskID','TaskDate','Comments','EnteredBy','TaskDate'])
        try :
            data_add.to_sql(name='EMPTASK', if_exists="append", con = con, index=False)
            st.session_state.EmpTaskTbl_Key["added_rows"] = []
        except sqlite3.Error as error:
            st.write(error)
            st.session_state.EmpTaskTbl_Key["added_rows"] = []
            rows_to_delete = edited_df.index.max()
            st.write(rows_to_delete)
            st.session_state["data"] = (st.session_state["data"].drop(rows_to_delete, axis=0).reset_index(drop=True)
    )






st.title("This is a title")
# ---- input date ----
A_date = st.date_input("Select Input date")
if st.button("Add New", icon="➕") :
    AddEmpAct(A_date)

df_AllEmpActList = pd.read_sql_query(f"SELECT * from View_EmpTaskSheet WHERE TaskDate = '{A_date}'", con)
df_AllEmpActList = df_AllEmpActList.filter(['TaskEmpID','EmpName','TaskDescription', 'Comments', 'EnteredBy','TaskDate'], axis=1)
st.session_state.data = df_AllEmpActList


# ----- TABLE DATA ---- 
if "data" not in st.session_state:
    df_AllEmpActList = pd.read_sql_query(f"SELECT * from View_EmpTaskSheet WHERE TaskDate = '{A_date}'", con)
    st.session_state.data = df_AllEmpActList.filter(['TaskEmpID','EmpName','TaskDescription', 'Comments', 'EnteredBy','TaskDate'], axis=1)


print(st.session_state["data"])   
df_EmpAct = st.session_state["data"].copy()
# ---- Emp List list for dropdown from DB ----
df_empList = pd.read_sql_query("SELECT EmpID,EmpName,EmpStatus,EmpDesignation from EMP", con)
EmpList = df_empList["EmpName"]

# ---- Task list for dropdown from DB ----
df_taskList = pd.read_sql_query("SELECT * from TASK", con)
TaskList = df_taskList["TaskDescription"].to_list()




# ----- TABLE EDITOR  RENDER -----

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


