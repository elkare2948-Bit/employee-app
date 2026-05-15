import streamlit as st

st.set_page_config(page_title="Employee Management System", page_icon="👔", layout="wide")

# Employee Class
class Employee:
    def __init__(self, name: str, department: str, salary: float):
        self.name = name
        self.department = department
        self.salary = salary

    def give_raise(self, amount: float):
        self.salary += amount
        return f"New salary for {self.name}: {self.salary}"

    def transfer(self, new_department: str):
        self.department = new_department
        return f"{self.name} transferred to {new_department}."

    def details(self):
        return {"name": self.name, "department": self.department, "salary": self.salary}


# Initialize session state
if "employees" not in st.session_state:
    st.session_state.employees = {}
if "logs" not in st.session_state:
    st.session_state.logs = []

st.title("👔 Employee Management System")
st.markdown("---")

# Sidebar - Add Employee
with st.sidebar:
    st.header("➕ Add New Employee")
    emp_name = st.text_input("Name")
    emp_dept = st.text_input("Department")
    emp_salary = st.number_input("Salary", min_value=0.0, step=500.0)

    if st.button("Add Employee", use_container_width=True):
        if emp_name and emp_dept and emp_salary > 0:
            if emp_name in st.session_state.employees:
                st.error("Employee already exists!")
            else:
                st.session_state.employees[emp_name] = Employee(emp_name, emp_dept, emp_salary)
                st.session_state.logs.append(f"✅ Added employee: {emp_name}")
                st.success(f"Employee {emp_name} added!")
        else:
            st.warning("Please fill in all fields.")

# Main Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Give Raise")
    if st.session_state.employees:
        raise_emp = st.selectbox("Select Employee", list(st.session_state.employees.keys()), key="raise_select")
        raise_amount = st.number_input("Raise Amount", min_value=0.0, step=100.0, key="raise_amt")
        if st.button("Give Raise", use_container_width=True):
            msg = st.session_state.employees[raise_emp].give_raise(raise_amount)
            st.session_state.logs.append(f"💰 {msg}")
            st.success(msg)
    else:
        st.info("No employees added yet.")

with col2:
    st.subheader("🔄 Transfer Employee")
    if st.session_state.employees:
        transfer_emp = st.selectbox("Select Employee", list(st.session_state.employees.keys()), key="transfer_select")
        new_dept = st.text_input("New Department", key="new_dept")
        if st.button("Transfer", use_container_width=True):
            if new_dept:
                msg = st.session_state.employees[transfer_emp].transfer(new_dept)
                st.session_state.logs.append(f"🔄 {msg}")
                st.success(msg)
            else:
                st.warning("Please enter a new department.")
    else:
        st.info("No employees added yet.")

st.markdown("---")

# Employee Details
st.subheader("📋 Employee Details")
if st.session_state.employees:
    cols = st.columns(len(st.session_state.employees))
    for i, (name, emp) in enumerate(st.session_state.employees.items()):
        with cols[i]:
            details = emp.details()
            st.markdown(f"""
            <div style='background-color:#1e2a3a;padding:20px;border-radius:10px;border:1px solid #3a5a8a;'>
                <h4 style='color:#4fc3f7;margin:0 0 10px 0;'>👤 {details['name']}</h4>
                <p style='color:#b0c4de;margin:5px 0;'>🏢 <b>Dept:</b> {details['department']}</p>
                <p style='color:#b0c4de;margin:5px 0;'>💵 <b>Salary:</b> ${details['salary']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No employees to display. Add employees from the sidebar.")

st.markdown("---")

# Logs
st.subheader("📝 Activity Log")
if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.write(log)
    if st.button("Clear Logs"):
        st.session_state.logs = []
        st.rerun()
else:
    st.info("No activity yet.")