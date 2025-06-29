import sqlite3
import pandas as pd
print("XX")
con = sqlite3.connect("database.db")
cursor = con.cursor()
#cur.execute("CREATE TABLE EMP(EmpID, EmpName, EmpDesignation, EmpStatus,EmpType, EmpRole )")
#cursor.execute("CREATE TABLE TASK(TaskID,TaskDescription, TaskType,TaskScope,TaskStatus)")
#cursor.execute("CREATE TABLE EMPTASK(EmpID,TaskID,TaskDate,Comments,EnteredBy,AcceptEMPTASK)")

CREATE VIEW view_EMPTASK AS
SELECT EMPTASK.EmpID,EMPTASK.TaskID,EMPTASK.TaskDate,EMPTASK.Comments,EMPTASK.EnteredBy,EMPTASK.AcceptEMPTASK, EMP.EmpID, EMP.EmpName, EMP.EmpDesignation, EMP.EmpStatus,EMP.EmpType, EMP.EmpRole,
FROM table_name
WHERE condition;



#data = [
 #   ("12354", "Admin", "System Admin", True, "Admin", "Admin"),
  #  ("595", "Anto Joseph", "Planner", True, "Management", "Planner"),
   # ("E8569", "Joe Finnegan", "Project Manager", True, "Management", "Manager"),
    #("E85", "Lar Murphy", "Site Supervisor", True, "In-direct OnSite", "Supervisor"),
    #("489", "Erin D", "HSE Supervisor", True, "In-direct OnSite", "Supervisor"),
    #("489dd", "Anderson K", "Spoter", True, "Construction", "Technician"),
#]

#data = [
#    ("L00-1B-VESDA", "Level 0.0 Zone 1B VESDA", "Construction", "BOQ-R05",True),
#    ("L00-H(Corridor)-FA-CBL", "Level 0.0 Corridor FA CABLE", "Construction", "BOQ-R05",True),
#    ("LL00-D(PD)-SEC-TER", "Level 0.0 D - Waste Water - SEC Termination", "Construction", "BOQ-R05",True),
#    ("L0X-WH-CNT", "External Warehouse - Secondary Containment", "Construction", "PJH-WH",True),
#    ("M-HSE-S", "Safety", "Indirect On-Site", "BOQ-R05",True),
    
#]




#cursor.executemany("INSERT INTO TASK VALUES(?, ?, ?, ?, ?)", data)
#con.commit() 

#res = cursor.execute("SELECT EmpName FROM EMP")

#mov = pd.DataFrame(res.fetchall())

#print(mov[0].to_list())

con = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * from EMPTASK", con)
print(df.head())