import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json  
import os  
import numpy as np  # Import numpy to handle NaN values
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,  
    options=["Home", "Tasks", "Analysis"],  
    icons=["house", "list-task", "pie-chart-fill"], 
    menu_icon="cast",  
    default_index=0,  
    orientation="horizontal",
)


Data_file = "task.json"  

def load_tasks():  
    if os.path.exists(Data_file):  
        with open(Data_file, "r") as file:  
            return json.load(file)  
    return []  

def save_tasks(tasks):  
    with open(Data_file, "w") as file:  
        json.dump(tasks, file)  

def clear_tasks():  
    with open(Data_file, "w") as file:  
        json.dump([], file)  


tasks = load_tasks()

if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: BLACK;'>TASK TRACKER 📃 </h1>", unsafe_allow_html=True)
    with st.container(border=True):
        task = st.text_input("📜 Enter a new task or habit")  
        task_due_date = st.date_input("📆 Select due date for task (optional)")
    
    if st.button("Add Task"):  
        if task:  
            new_task = {"task": task, "completed": False}  
            if task_due_date:  
                new_task["due_date"] = str(task_due_date)  
            tasks.append(new_task)  
            save_tasks(tasks)  
            st.success(f"Task '{task}' added successfully!")  
        else:
            st.warning("Please enter a task.")
    
if selected == "Tasks":
    st.markdown("<h1 style='text-align: center; color: BLACK;'>TASK LIST</h1>", unsafe_allow_html=True)
    
    if st.button("Clear All Tasks"):  
        clear_tasks()  
        tasks = []  
        st.success("All tasks cleared!")  

    for i, task in enumerate(tasks):  
        task_name = task["task"]
        with st.container(border=True):  
            is_completed = st.checkbox(task_name, task["completed"], key=i)  
    
        if is_completed != task["completed"]:  
            task["completed"] = is_completed  
            save_tasks(tasks)  

    total_tasks = len(tasks)  
    completed_tasks = sum(1 for task in tasks if task["completed"])  

    if total_tasks > 0:  
        st.write(f"Completed {completed_tasks} out of {total_tasks} tasks.")  
        st.progress(completed_tasks / total_tasks)  
    else:  
        st.write("No tasks to display.")  

if selected == "Analysis":
    st.header("📊 Task Completion Pie Chart")
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])

    if total_tasks > 0:
        sizes = [completed_tasks, total_tasks - completed_tasks]
        labels = ['Completed', 'Pending']
        
        sizes = np.nan_to_num(sizes)  # Ensure no NaN values
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
        
        st.pyplot(fig1)
