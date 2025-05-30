import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def api_request(method, endpoint, data=None):
    try:
        url = f"{API_URL}{endpoint}"
        response = requests.request(method, url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def list_projects():
    return api_request('GET', '/projects')

def list_tasks():
    return api_request('GET', '/tasks')

def create_project(name, description):
    return api_request('POST', '/projects', {
        "name": name,
        "description": description
    })

def create_task(title, status, project_id, assigned_to):
    return api_request('POST', '/tasks', {
        "title": title,
        "status": status,
        "project_id": project_id,
        "assigned_to": assigned_to
    })

def update_task_status(task_id, status):
    return api_request('PATCH', f'/tasks/{task_id}', {"status": status})

def render_task_card(task, projects):
    with st.container():
        st.markdown(f"### {task['title']}")
        st.write(f"**Project:** {next((p['name'] for p in projects if p['id'] == task['project_id']), 'Unknown')}")
        st.write(f"**Assigned to:** {task['assigned_to'] or 'Unassigned'}")
        
        # Add status update
        new_status = st.selectbox(
            "Status",
            ["To Do", "In Progress", "Done"],
            index=["To Do", "In Progress", "Done"].index(task['status']),
            key=f"status_{task['id']}"
        )
            
        if new_status != task['status']:
            update_task_status(task['id'], new_status)
            st.rerun()

st.set_page_config(page_title="Project Management Tool", layout="wide")
st.title("📋 Project Management Tool")

# Sidebar for navigation
page = st.sidebar.selectbox("Navigation", ["Projects", "Tasks", "Kanban Board"])

if page == "Projects":
    st.header("Create a new project")
    with st.form("new_project"):
        name = st.text_input("Project Name")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Project")
        if submitted and name:
            result = create_project(name, description)
            if result:
                st.success("Project created successfully!")

    st.header("All Projects")
    projects = list_projects()
    if projects:
        for project in projects:
            with st.expander(f"📁 {project['name']}"):
                st.write(f"**Description:** {project['description']}")
                st.write(f"**Tasks:** {project['task_count']}")

elif page == "Tasks":
    st.header("Create a new task")
    with st.form("new_task"):
        projects = list_projects()
        if projects:
            proj_dict = {p['name']: p['id'] for p in projects}
            title = st.text_input("Task Title")
            project = st.selectbox("Project", proj_dict.keys())
            status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
            assigned_to = st.text_input("Assign to (username)")
            
            submitted = st.form_submit_button("Create Task")
            if submitted and title:
                result = create_task(
                    title, status,
                    proj_dict[project], assigned_to
                )
                if result:
                    st.success("Task created successfully!")
        else:
            st.warning("Create a project first before creating tasks.")

elif page == "Kanban Board":
    st.header("📋 Kanban Board")
    
    # Create three columns for the Kanban board
    todo_col, progress_col, done_col = st.columns(3)
    
    # Get all tasks and projects
    tasks = list_tasks()
    projects = list_projects()
    
    if tasks and projects:
        # Organize tasks by status
        todo = [t for t in tasks if t['status'] == 'To Do']
        in_progress = [t for t in tasks if t['status'] == 'In Progress']
        done = [t for t in tasks if t['status'] == 'Done']
        
        # Render columns
        with todo_col:
            st.subheader("📝 To Do")
            for task in todo:
                render_task_card(task, projects)
                
        with progress_col:
            st.subheader("🔄 In Progress")
            for task in in_progress:
                render_task_card(task, projects)
                
        with done_col:
            st.subheader("✅ Done")
            for task in done:
                render_task_card(task, projects)
    else:
        st.info("No tasks found. Create some tasks to see them on the Kanban board.")