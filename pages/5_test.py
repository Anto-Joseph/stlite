import streamlit as st
import pandas as pd
import sqlite3
import time
import uuid

# ----- INITIALIZE USER -----
AddedByUser = st.session_state.get("name")
# Create de key
st.session_state['EmpTaskTbl_Key'] = str(uuid.uuid4())

# ----- ON CHANGE FUNCTION -------
def process_changes():
    e_df_TempKey = st.session_state['EmpTaskTbl_Key']
    editor_state = st.session_state.get(str(e_df_TempKey), {})
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
            data_add.to_sql(name='EMPTASK', if_exists="append", con = con, index=False)
        except sqlite3.Error as error:
            st.warning(error)
            st.toast('Employe Alread Entered!', icon='🚩')
            time.sleep(.5)


    # ---- DELETE DATA FROM TABLE ---
    if len(deleted) != 0:
        deletedList = editor_state.get("deleted_rows",{})
        deleted_df = st.session_state["EmpTaskDate"].iloc[deletedList]
        deleteListToQuery = []
        for delID in deleted_df['TaskEmpID'].to_list() :
            deleteListToQuery.append((delID,))
            try : 
                del_query = """DELETE from EMPTASK where TaskEmpID = ?"""
                cursor.executemany(del_query, deleteListToQuery)
                con.commit()
            except sqlite3.Error as error:
                st.warning(error)
                st.toast(error, icon='🚩')
                time.sleep(.5)

    # ----- EDITED -----
    if len(edited) != 0:
        len(edited)
        edited = pd.DataFrame.from_dict(edited)
        editedCol = edited.index[0]
        editedRowID = edited.T.index[0]
        #edited Col ID
        st.title('Column name')
        update_TaskEmpID = edited_df.iloc[editedRowID]['TaskEmpID']

        #old value
        update_OldValue = edited_df.iloc[editedRowID][editedCol]
        #new value
        update_NewValue = edited[ editedRowID][editedCol]


        #convert 'editedCol to Col ID
        if editedCol == 'EmpName' :
            editedColID = 'EmpID'
            update_NewValueID  = df_empList.loc[df_empList['EmpName'] == update_NewValue,['EmpID']]
            update_NewValueID = update_NewValueID.iloc[0,0]

        elif editedCol == 'TaskDescription' :
            editedColID = 'TaskID'
            update_NewValueID  = df_taskList.loc[df_taskList['TaskDescription'] == update_NewValue,['TaskID']]
            update_NewValueID = update_NewValueID.iloc[0,0]


        
        try:
            update_query = f"""UPDATE EMPTASK SET {editedColID} = ? WHERE TaskEmpID = ?"""
            cursor.execute(update_query, (update_NewValueID, update_TaskEmpID))
            con.commit()
           

        except sqlite3.Error as error:
            st.warning(error)
            st.toast(error, icon='🚩')
            time.sleep(.5)
    





    # ---- update session state to trigger table -----
    st.session_state["EmpTaskTbl_Key"] = str(uuid.uuid4())



# --- DATABASE CONNECTION ---

con = sqlite3.connect("database-1.db")
cursor =  con.cursor()


# ---- DATE ENTRY WIDGET ----
st.title('Daily Work Sheet')
A_date = st.date_input("Select Input date")

# ----- Table Data ---- 
st.session_state["EmpTaskDate"] = pd.read_sql_query(f"SELECT * from View_EmpTaskSheet WHERE TaskDate = '{A_date}'", con)


# ---- Emp List list for dropdown from DB ----
df_empList = pd.read_sql_query("SELECT EmpID,EmpName,EmpStatus,EmpDesignation from EMP", con)
EmpList = df_empList["EmpName"]

# ---- Task list for dropdown from DB ----
df_taskList = pd.read_sql_query("SELECT * from TASK", con)
TaskList = df_taskList["TaskDescription"].to_list()



edited_df = st.data_editor(
    st.session_state["EmpTaskDate"],
    key = st.session_state['EmpTaskTbl_Key'],
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
      "EnteredBy" : st.column_config.TextColumn("Added By", default= st.session_state.get("name")),

    },

    column_order=("EmpName", "TaskDescription","Comments","EnteredBy"),

)