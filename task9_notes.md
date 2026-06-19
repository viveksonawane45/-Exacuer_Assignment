# Task 9 — Doppio React Frontend with Frappe APIs (HR Analytics Dashboard)

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** Doppio React App + Frappe REST API + Dashboard + Authentication + Charts + Error Handling

---

# Business Requirement

The CEO requires a separate dashboard outside ERPNext for monitoring HR KPIs.

The dashboard should display:

1. Total Employees
2. Active Employees
3. Employees on Leave Today
4. Employees with Upcoming Birthdays
5. Average Performance Score
6. Department-wise Employee Distribution
7. Top Performers
8. Employees with High Absenteeism

Requirements:

- Build using Doppio React.
- Data should come from Frappe APIs.
- No direct database access from React.
- Handle authentication.
- Handle API failures gracefully.
- Support loading states.

---

# Objective

Build a modern HR Analytics Dashboard using:

```text
React (Doppio)
        +
Frappe REST APIs
        +
Charts
        +
Cards
        +
Authentication
```

---

# System Architecture

```text
React Dashboard
        │
        ├── Employee Cards
        ├── Charts
        ├── Tables
        └── Filters
               │
               ▼
        Frappe REST APIs
               │
               ▼
        ERPNext Database
```

---

# Why Use React Instead of ERPNext Pages?

Advantages:

- Better UI/UX
- Faster interactions
- Component-based architecture
- Mobile responsive
- Easier charting
- Separate frontend deployment

---

# Dashboard Overview

```text
HR Dashboard
│
├── KPI Cards
│      ├── Total Employees
│      ├── Active Employees
│      ├── On Leave Today
│      └── Average Score
│
├── Charts
│      ├── Department Distribution
│      └── Attendance Trend
│
└── Tables
       ├── Top Performers
       └── High Absenteeism
```

---

# Folder Structure

```text
hr-dashboard/
│
├── src/
│
├── components/
│      ├── KPIWidget.jsx
│      ├── EmployeeTable.jsx
│      ├── DepartmentChart.jsx
│      └── LoadingSpinner.jsx
│
├── pages/
│      └── Dashboard.jsx
│
├── services/
│      └── api.js
│
├── hooks/
│      └── useDashboard.js
│
├── context/
│      └── AuthContext.jsx
│
├── App.jsx
└── package.json
```

---

# Backend Architecture

```text
ERPNext
│
├── Employee APIs
├── Attendance APIs
├── Leave APIs
├── Performance APIs
└── Dashboard APIs
```

---

# Recommended APIs

## Total Employees

```python
@frappe.whitelist()
def get_total_employees():

    return frappe.db.count(
        "Employee"
    )
```

---

## Active Employees

```python
@frappe.whitelist()
def get_active_employees():

    return frappe.db.count(
        "Employee",
        {
            "status": "Active"
        }
    )
```

---

## Employees on Leave Today

```python
@frappe.whitelist()
def get_employees_on_leave():

    return frappe.db.count(
        "Leave Application",
        {
            "from_date": ["<=", frappe.utils.today()],
            "to_date": [">=", frappe.utils.today()],
            "status": "Approved"
        }
    )
```

---

## Average Performance Score

```python
@frappe.whitelist()
def get_average_performance():

    result = frappe.db.sql(
        """
        SELECT
            AVG(overall_score)
        FROM
            `tabQuarterly Performance Review`
        """,
        as_list=True
    )

    return result[0][0]
```

---

# Department Distribution API

```python
@frappe.whitelist()
def get_department_distribution():

    return frappe.db.sql(
        """
        SELECT
            department,
            COUNT(*) AS total
        FROM
            `tabEmployee`
        WHERE
            status='Active'
        GROUP BY
            department
        """,
        as_dict=True
    )
```

---

# Top Performers API

```python
@frappe.whitelist()
def get_top_performers():

    return frappe.db.sql(
        """
        SELECT
            employee,
            employee_name,
            overall_score
        FROM
            `tabQuarterly Performance Review`
        ORDER BY
            overall_score DESC
        LIMIT 10
        """,
        as_dict=True
    )
```

---

# High Absenteeism API

```python
@frappe.whitelist()
def get_high_absenteeism():

    return frappe.db.sql(
        """
        SELECT
            employee,
            COUNT(*) AS absent_days
        FROM
            `tabAttendance`
        WHERE
            status='Absent'
        GROUP BY
            employee
        HAVING
            COUNT(*) > 5
        """,
        as_dict=True
    )
```

---

# API Architecture

```text
Dashboard
      │
      ├── Total Employees API
      ├── Active Employees API
      ├── Leave API
      ├── Performance API
      ├── Department API
      └── Absenteeism API
```

---

# Authentication

React should never directly access MariaDB.

Use:

```text
Login
      ↓
Session Cookie
      ↓
Authenticated API Requests
```

---

# Login API

```javascript
POST

/api/method/login
```

Body:

```json
{
  "usr": "administrator",
  "pwd": "password"
}
```

---

# API Service

## services/api.js

```javascript
import axios from "axios";

const api = axios.create({
  baseURL:
    "http://localhost:8000/api/method/",
  withCredentials: true
});

export default api;
```

---

# Get Total Employees

```javascript
export const getTotalEmployees =
  () =>
    api.get(
      "custom_hr_pro.api.dashboard.get_total_employees"
    );
```

---

# Dashboard Flow

```text
Dashboard Opens
       ↓
Multiple API Calls
       ↓
Receive Data
       ↓
Update State
       ↓
Render Cards
       ↓
Render Charts
       ↓
Render Tables
```

---

# Dashboard State

```javascript
const [
  dashboard,
  setDashboard
] = useState({});
```

---

# Loading State

```javascript
const [
  loading,
  setLoading
] = useState(true);
```

---

# Error State

```javascript
const [
  error,
  setError
] = useState(null);
```

---

# Fetch Dashboard

```javascript
useEffect(() => {
  loadDashboard();
}, []);
```

---

# Example

```javascript
async function loadDashboard() {

  try {

    setLoading(true);

    const total =
      await getTotalEmployees();

    setDashboard({
      total:
      total.data.message
    });

  }
  catch (err) {

    setError(
      "Unable to load dashboard."
    );
  }
  finally {

    setLoading(false);
  }
}
```

---

# Why Loading States Matter

Without:

```text
Blank Screen
```

With:

```text
Loading Spinner
```

Better UX.

---

# Loading Component

```jsx
function LoadingSpinner() {
  return (
    <div>
      Loading Dashboard...
    </div>
  );
}
```

---

# Error Component

```jsx
{
  error &&
  (
    <div>
      {error}
    </div>
  )
}
```

---

# KPI Cards

```text
---------------------------------
| Total Employees : 145         |
---------------------------------
| Active Employees : 140        |
---------------------------------
| On Leave Today : 6            |
---------------------------------
| Avg Performance : 4.1         |
---------------------------------
```

---

# KPI Component

```jsx
function KPIWidget(
{
  title,
  value
}
)
{
  return (
    <div className="card">
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}
```

---

# Department Chart

Recommended:

```text
Pie Chart
```

or

```text
Bar Chart
```

---

# Data Flow

```text
Department API
      ↓
React State
      ↓
Chart Component
      ↓
Pie Chart
```

---

# Top Performers Table

```text
Employee Name
Overall Score
Department
```

---

# High Absenteeism Table

```text
Employee Name
Absent Days
```

---

# Dashboard Layout

```text
-----------------------------------------
 KPI CARDS
-----------------------------------------

-----------------------------------------
 Department Chart
-----------------------------------------

-----------------------------------------
 Top Performers
-----------------------------------------

-----------------------------------------
 High Absenteeism
-----------------------------------------
```

---

# API Security

Never:

```javascript
SELECT *
FROM tabEmployee
```

inside React.

Reason:

```text
Database credentials exposed.
```

Always:

```text
React
     ↓
Frappe APIs
     ↓
MariaDB
```

---

# Error Handling Strategy

## API Failure

Show:

```text
Unable to load dashboard.
Please try again.
```

---

## Empty Data

Show:

```text
No records available.
```

---

## Authentication Failure

Redirect:

```text
Login Page
```

---

# Performance Optimization

Use:

```javascript
Promise.all()
```

Example:

```javascript
await Promise.all([
  getTotalEmployees(),
  getActiveEmployees(),
  getAveragePerformance()
]);
```

Benefits:

- Faster loading
- Parallel requests
- Better user experience

---

# Automated Tests

## Backend Tests

### Total Employee API

Expected:

```text
Returns employee count.
```

---

### Department API

Expected:

```text
Returns grouped department data.
```

---

### Performance API

Expected:

```text
Returns average score.
```

---

## Frontend Tests

### Dashboard Loading

Expected:

```text
Spinner shown.
```

---

### Error Handling

Expected:

```text
Error message shown.
```

---

### Table Rendering

Expected:

```text
Rows displayed.
```

---

# Suggested Screenshots

```text
screenshots/
├── 01_dashboard_home.png
├── 02_kpi_cards.png
├── 03_department_chart.png
├── 04_top_performers.png
├── 05_high_absenteeism.png
├── 06_loading_state.png
├── 07_error_state.png
├── 08_api_response.png
```

---

# Add Screenshots

```markdown
![Dashboard](screenshots/01_dashboard_home.png)

![KPI Cards](screenshots/02_kpi_cards.png)

![Department Chart](screenshots/03_department_chart.png)

![Top Performers](screenshots/04_top_performers.png)
```

---

# Final Folder Structure

```text
custom_hr_pro/
│
├── task9_notes.md
│
├── api/
│      └── dashboard.py
│
├── hr-dashboard/
│      ├── src/
│      ├── components/
│      ├── pages/
│      ├── hooks/
│      ├── services/
│      ├── context/
│      ├── App.jsx
│      └── package.json
│
├── TASK9_RESEARCH.md
└── TASK9_NOTES.md
```

---

# End-to-End Architecture

```text
React Dashboard
        ↓
Login
        ↓
Session Cookie
        ↓
API Requests
        ↓
Frappe Whitelisted Methods
        ↓
MariaDB
        ↓
Response JSON
        ↓
React State
        ↓
Cards
Charts
Tables
Dashboard
```

This implementation builds a modern HR Analytics Dashboard using Doppio React and Frappe APIs, providing executives with real-time workforce insights while maintaining security, scalability, and separation between frontend and backend responsibilities.