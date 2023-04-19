import streamlit as st
import urllib.request
import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection
print("Connecting to database...")
url = 'https://github.com/CNielsen94/Exercises_AAUBSDS/blob/main/MLOps_assignments/Assignment_three/Database/HR_DB.db?raw=true'
filename = 'HR_DB.db'
urllib.request.urlretrieve(url, filename)

conn = sqlite3.connect('HR_DB.db')
print("Connection established.")

# Setting up dataframe for EDA
print("Loading dataframes...")
query = 'SELECT * FROM EmployeeTiers'
employee_tiers = pd.read_sql(query, conn)

query = 'SELECT * FROM manager_survey'
manager_survey = pd.read_sql(query, conn)

query = 'SELECT * FROM employee_survey'
employee_survey = pd.read_sql(query, conn)

query = 'SELECT * FROM general'
df_general = pd.read_sql(query, conn)
print("Dataframes loaded.")

# Merging dataframe manager_survey to df_general based on 'EmployeeID'
print("Merging dataframes...")
df_general = df_general.merge(manager_survey[['EmployeeID', 'JobInvolvement', 'PerformanceRating', 'total_mn']], on='EmployeeID')
df_EDA = df_general.merge(manager_survey[['EmployeeID', 'JobInvolvement', 'PerformanceRating', 'total_mn']], on='EmployeeID')
# Merging dataframe employee_survey to df_general based on 'EmployeeID'
df_general = df_general.merge(employee_survey[['EmployeeID', 'EnvironmentSatisfaction', 'JobSatisfaction', 'WorkLifeBalance', 'total_em']], on='EmployeeID')
df_EDA = df_general.merge(manager_survey[['EmployeeID', 'JobInvolvement', 'PerformanceRating', 'total_mn']], on='EmployeeID')
print("Dataframes merged.")

# Dropping rows containing NaN-values
print("Dropping rows with NaN values...")
df_EDA.dropna(axis=0, inplace=True)
df_general.dropna(axis=0, inplace=True)
print("Rows dropped.")

def app():
    st.set_page_config(page_title="Employee Attrition Analysis", page_icon=":guardsman:", layout="wide")

    st.title("Employee Attrition Analysis")

    st.sidebar.header("Select an analysis")

    analysis_type = st.sidebar.selectbox("", ["Exploratory Data Analysis (EDA)", "Predictive Modeling"])

    if analysis_type == "Exploratory Data Analysis (EDA)":
        st.subheader("Exploratory Data Analysis (EDA)")

        # Age filter for talented employees
        print("Filtering by age...")
        df_EDA_u30 = df_EDA[df_EDA['Age'] < 30]

        # Filter for employees with higher manager survey score than employee survey score
        print("Filtering by survey score...")
        talented_employees = df_EDA_u30[(df_EDA_u30['total_mn_y'] - df_EDA_u30['total_em']) > 1]

        # Visualize attrition distribution
        print("Visualizing data...")
        fig, ax = plt.subplots()
        sns.countplot(data=df_general, x='Attrition', hue='Department')
        st.pyplot(fig)

if __name__ == '__main__':
    app()

