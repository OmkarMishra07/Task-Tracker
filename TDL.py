import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import numpy as np
from streamlit_option_menu import option_menu

# File to store tasks for each user
DATA_FILE = "task.json"

# Function to load all user tasks
# Function to load all user tasks
def load_all_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):  # Ensure it is a dictionary
                    return data
            except json.JSONDecodeError:
                pass  # If there's an error in JSON structure, we return an empty dict
    return {}  # Return an empty dictionary if file doesn't exist or is invalid


# Function to save all user tasks
def save_all_tasks(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Authenticate user
def authenticate(user_id, password):
    if user_id and password:
        return True
    return False

# Start the Streamlit app
st.title("Task Tracker with User Authentication")

# User authentication section
st.sidebar.header("User Login")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None

if not st.session_state.logged_in:
    user_id = st.sidebar.text_input("User ID")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate(user_id, password):
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid User ID or Password")

# Load user-specific tasks
if st.session_state.logged_in:
    user_id = st.session_state.user_id
    all_tasks_data = load_all_tasks()
    user_tasks = all_tasks_data.get(user_id, [])

    # Define the option menu
    selected = option_menu(
        menu_title=None,
        options=["Home", "Tasks", "Analysis"],
        icons=["house", "list-task", "pie-chart-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # Home page
    if selected == "Home":
        st.markdown("<h1 style='text-align: center; color: BLACK;'>TASK TRACKER 📃 </h1>", unsafe_allow_html=True)
        task = st.text_input("📜 Enter a new task or habit")
        task_due_date = st.date_input("📆 Select due date for task (optional)")

        if st.button("Add Task"):
            if task:
                new_task = {"task": task, "completed": False}
                if task_due_date:
                    new_task["due_date"] = str(task_due_date)
                user_tasks.append(new_task)
                all_tasks_data[user_id] = user_tasks
                save_all_tasks(all_tasks_data)
                st.success(f"Task '{task}' added successfully!")
            else:
                st.warning("Please enter a task.")

    # Tasks page
    elif selected == "Tasks":
        st.markdown("<h1 style='text-align: center; color: BLACK;'>TASK LIST</h1>", unsafe_allow_html=True)

        if st.button("Clear All Tasks"):
            user_tasks.clear()
            all_tasks_data[user_id] = user_tasks
            save_all_tasks(all_tasks_data)
            st.success("All tasks cleared!")

        for i, task in enumerate(user_tasks):
            task_name = task["task"]
            is_completed = st.checkbox(task_name, task["completed"], key=f"{user_id}_{i}")

            if is_completed != task["completed"]:
                task["completed"] = is_completed
                all_tasks_data[user_id] = user_tasks
                save_all_tasks(all_tasks_data)

        total_tasks = len(user_tasks)
        completed_tasks = sum(1 for task in user_tasks if task["completed"])

        if total_tasks > 0:
            st.write(f"Completed {completed_tasks} out of {total_tasks} tasks.")
            st.progress(completed_tasks / total_tasks)
        else:
            st.write("No tasks to display.")

    # Analysis page
    elif selected == "Analysis":
        st.header("📊 Task Completion Pie Chart")
        
        total_tasks = len(user_tasks)
        completed_tasks = sum(1 for task in user_tasks if task["completed"])

        if total_tasks > 0:
            sizes = [completed_tasks, total_tasks - completed_tasks]
            labels = ['Completed', 'Pending']
            
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
            st.pyplot(fig1)
        else:
            st.write("No tasks available for analysis.")
else:
    st.sidebar.warning("Please log in to access your tasks.")
