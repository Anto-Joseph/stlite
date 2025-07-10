import streamlit as st
import datetime
import streamlit_authenticator as stauth
import pandas as pd
from openpyxl import load_workbook
import numpy as np

Xl_SkipColumns = []


st.title('Daily Timesheet')
st.write(f'Entered By : *{st.session_state.get("name")}*')
file_df = []

T_date = st.date_input("Select Input date")


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    try :
        file_df = load_workbook(uploaded_file)

    except Exception as e :
        st.warning("Opps wrong file format")
        st.write(e)

if file_df != []:
    Xl_Sheet = st.selectbox(
                                "Select your sheet",
                                file_df.sheetnames,
                                index=None,
                                placeholder="Select Sheet...",
                            )
    Xl_FormatDataType = st.selectbox(
                                "Load Data As",
                                ("By Sheet","By Table"),
                                index=None,
                                placeholder="Format as...",
                            )
    if Xl_FormatDataType == "By Sheet" :
        Xl_selectedSheetDF = pd.DataFrame(file_df[Xl_Sheet].values)
        Xl_SkipRowNo =  st.number_input("Header Row Number",step = 1,min_value  = 0)
        headerRow = Xl_selectedSheetDF.loc[Xl_SkipRowNo].to_frame()
        headerRow['ColNum'] = headerRow.index
        headerRow = headerRow.dropna()
        headerRow.T
        Xl_selectedSheetDF = Xl_selectedSheetDF.iloc[0:][headerRow['ColNum']]
        Xl_selectedSheetDF.columns = Xl_selectedSheetDF.iloc[Xl_SkipRowNo]
        Xl_selectedSheetDF =  Xl_selectedSheetDF.iloc[Xl_SkipRowNo:]
        Xl_selectedSheetDF






