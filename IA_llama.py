import streamlit as st
import openpyxl
import sqlite3

st.title("Excel Data Loader")

# Connect to SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS excel_data (Name TEXT, Age INTEGER, Email TEXT)''')
conn.commit()

# Load Excel file
file_upload = st.file_uploader("Select an Excel file", type=["xlsx"])

if file_upload is not None:
    workbook = openpyxl.load_workbook(file_upload)
    sheet = workbook.active

    # Read data from Excel file
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append([x for x in row])

    # Insert data into SQLite database
    for row in data[1:]:
        c.execute("INSERT INTO excel_data VALUES (?, ?, ?)", row)
    conn.commit()

    st.write("Data inserted successfully!")

    # Close connection to database
    conn.close()
