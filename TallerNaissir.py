# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 17:30:18 2025

@author: Farid
"""

import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Taller Naissir Maintenance Dashboard", layout="wide")

# --- HEADER ---
st.title("Maintenance Management Dashboard")
st.markdown("Taller Naissir maintenance tracking system")
st.markdown("This is a demo version built with **Streamlit + Python** for data protection of Taller Naissir's operations")

# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.radio("Navigate", ["Dashboard", "Maintenance Log", "Add Record", "Analytics"])

# --- LOAD DATA ---
DATA_PATH = "data/maintenance_log.csv"
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Equipment", "Task", "Technician", "Status", "Priority", "Notes"])

# --- DASHBOARD ---
if menu == "Dashboard":
    st.subheader("📊 System Overview")

    total_tasks = len(df)
    completed = len(df[df["Status"] == "Completed"])
    pending = len(df[df["Status"] == "Pending"])
    in_progress = len(df[df["Status"] == "In Progress"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed)
    col3.metric("Pending", pending)

    st.markdown("---")
    if not df.empty:
        st.write("### 📈 Status Distribution")
        st.bar_chart(df["Status"].value_counts())

        st.write("### 🧰 Tasks per Category")
        st.bar_chart(df["Category"].value_counts())

        st.write("### 🧑‍🔧 Tasks per Technician")
        st.bar_chart(df["Technician"].value_counts())
    else:
        st.warning("No data available yet.")

# --- MAINTENANCE LOG ---
elif menu == "Maintenance Log":
    st.subheader("📋 Maintenance Log")

    # --- Filters ---
    if not df.empty:
        with st.expander("🔍 Filter Records"):
            category_filter = st.multiselect("Category", options=df["Category"].unique(), default=df["Category"].unique())
            status_filter = st.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())
            technician_filter = st.multiselect("Technician", options=df["Technician"].unique(), default=df["Technician"].unique())
            priority_filter = st.multiselect("Priority", options=df["Priority"].unique(), default=df["Priority"].unique())

        # --- Apply filters ---
        filtered_df = df[
            (df["Category"].isin(category_filter)) &
            (df["Status"].isin(status_filter)) &
            (df["Technician"].isin(technician_filter)) &
            (df["Priority"].isin(priority_filter))
        ]
        st.dataframe(filtered_df)
    else:
        st.warning("No maintenance records yet. Add a new one under 'Add Record'.")

# --- ADD RECORD ---
elif menu == "Add Record":
    st.subheader("➕ Add Maintenance Record")
    with st.form("entry_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.date.today())
        category = st.selectbox("Category", ["Mechanical", "Electrical", "Hydraulics", "Logistics", "Other"])
        equipment = st.text_input("Equipment")
        task = st.text_area("Task Description")
        technician = st.text_input("Technician")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save Record")

        if submitted:
            new_entry = pd.DataFrame([[date, category, equipment, task, technician, status, priority, notes]], 
                                     columns=df.columns)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_PATH, index=False)
            st.success("✅ Record saved successfully!")

# --- ANALYTICS ---
elif menu == "Analytics":
    st.subheader("📈 Maintenance Analytics")
    if not df.empty:
        st.bar_chart(df["Status"].value_counts())

        st.write("### Task Completion Over Time")
        df["Date"] = pd.to_datetime(df["Date"])
        st.line_chart(df.groupby("Date").size())

        st.write("### ⚠️ Pending Tasks by Priority")
        pending_df = df[df["Status"] != "Completed"]
        st.dataframe(pending_df[["Date", "Equipment", "Priority", "Technician", "Status", "Notes"]])
    else:
        st.warning("No data available for analytics.")

