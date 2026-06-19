# Task 3 — Complex Script Report (Employee Attendance & Performance Summary)

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** Script Report + SQL + Charts + Filters + Calculated Fields

---

# Business Requirement

The HR Manager requires a report that displays, for a selected date range and department:

- Employee Name
- Department
- Present Days
- Absent Days
- Late Arrivals
- Leaves Taken (By Leave Type)
- Latest Performance Review Score
- Attendance Summary
- High Absenteeism Indicator

Requirements:

- Employees with no attendance records must still appear.
- Report should support filters.
- Report should include a chart.
- Report should include a summary row.
- SQL queries must be parameterized.

---

# Objective

Build a comprehensive HR report combining:

```text
Employee
      +
Attendance
      +
Leave Application
      +
Quarterly Performance Review
      =
Employee Attendance & Performance Dashboard
```

---

# System Overview

```text
Employee
      │
      ├── Attendance
      │      ├── Present
      │      ├── Absent
      │      └── Late Arrival
      │
      ├── Leave Application
      │      ├── Sick Leave
      │      ├── Casual Leave
      │      └── LWP
      │
      └── Performance Review
              └── Latest Score
```

---

# Existing ERPNext Reports Research

Navigation:

```text
Home
→ Human Resources
→ Reports
```

---

# Existing Attendance Reports

### Monthly Attendance Sheet

Displays:

- Present Days
- Absent Days
- Leave Days

Limitations:

- No performance score
- No late arrivals
- No leave type breakdown

---

### Employee Attendance Tool

Displays:

- Daily attendance

Limitations:

- No review score
- No summaries

---

### Leave Ledger

Displays:

- Leave balances
- Leave transactions

Limitations:

- No attendance information
- No performance data

---

# Conclusion

No existing report provides:

```text
Attendance
+
Leave Type Summary
+
Late Arrivals
+
Performance Score
```

A new Script Report is justified.

---

# Required Tables

## Employee

```text
tabEmployee
```

Purpose:

Base table.

---

## Attendance

```text
tabAttendance
```

Purpose:

Present/Absent/Late counts.

---

## Leave Application

```text
tabLeave Application
```

Purpose:

Leave summary.

---

## Performance Review

```text
tabQuarterly Performance Review
```

Purpose:

Latest review score.

---

# Final Relationship

```text
tabEmployee
      │
      ├── tabAttendance
      │
      ├── tabLeave Application
      │
      └── tabQuarterly Performance Review
```

---

# Why LEFT JOIN?

Business Requirement:

Employees without attendance records must still appear.

Therefore:

```sql
LEFT JOIN
```

must be used.

---

# SQL Relationship

```text
Employee
LEFT JOIN Attendance
LEFT JOIN Leave Application
LEFT JOIN Quarterly Performance Review
```

---

# Report Filters

## From Date

```python
{
    "fieldname":"from_date",
    "label":"From Date",
    "fieldtype":"Date",
    "reqd":1
}
```

---

## To Date

```python
{
    "fieldname":"to_date",
    "label":"To Date",
    "fieldtype":"Date",
    "reqd":1
}
```

---

## Department

```python
{
    "fieldname":"department",
    "label":"Department",
    "fieldtype":"Link",
    "options":"Department"
}
```

---

## Employee

```python
{
    "fieldname":"employee",
    "label":"Employee",
    "fieldtype":"Link",
    "options":"Employee"
}
```

---

## Employment Type

```python
{
    "fieldname":"employment_type",
    "label":"Employment Type",
    "fieldtype":"Select"
}
```

---

# Required Columns

| Column | Type |
|--------|------|
| Employee | Link |
| Employee Name | Data |
| Department | Link |
| Present Days | Int |
| Absent Days | Int |
| Late Arrivals | Int |
| Sick Leave | Int |
| Casual Leave | Int |
| LWP | Int |
| Performance Score | Float |

---

# Main Query Design

## Employee Base Query

```sql
FROM
    `tabEmployee` emp
LEFT JOIN
    `tabAttendance` att
ON
    att.employee = emp.name
```

Reason:

Employees with no attendance records still appear.

---

# Counting Present Days

```sql
SUM(
CASE
WHEN att.status='Present'
THEN 1
ELSE 0
END
)
```

---

# Counting Absent Days

```sql
SUM(
CASE
WHEN att.status='Absent'
THEN 1
ELSE 0
END
)
```

---

# Detecting Late Arrivals

Assumption:

Attendance contains:

```text
in_time
shift_start
```

Late Arrival:

```sql
CASE
WHEN att.in_time > att.shift_start
THEN 1
ELSE 0
END
```

Count:

```sql
SUM(
CASE
WHEN att.late_entry = 1
THEN 1
ELSE 0
END
)
```

---

# Counting Leave Types

## Sick Leave

```sql
SUM(
CASE
WHEN la.leave_type='Sick Leave'
THEN la.total_leave_days
ELSE 0
END
)
```

---

## Casual Leave

```sql
SUM(
CASE
WHEN la.leave_type='Casual Leave'
THEN la.total_leave_days
ELSE 0
END
)
```

---

## Leave Without Pay

```sql
SUM(
CASE
WHEN la.leave_type='Leave Without Pay'
THEN la.total_leave_days
ELSE 0
END
)
```

---

# Getting Latest Performance Score

```sql
SELECT
overall_score
FROM
`tabQuarterly Performance Review`
WHERE
employee = emp.name
ORDER BY
review_year DESC,
modified DESC
LIMIT 1
```

---

# Report Architecture

```text
Employee
      │
      ├── Attendance Summary
      │
      ├── Leave Summary
      │
      └── Performance Summary
```

---

# Script Report Structure

```text
custom_hr_pro/
│
├── report/
│
└── employee_attendance_summary/
        ├── employee_attendance_summary.json
        ├── employee_attendance_summary.py
        └── employee_attendance_summary.js
```

---

# Report Flow

```text
User Opens Report
        ↓
Apply Filters
        ↓
Execute SQL
        ↓
Calculate Fields
        ↓
Generate Summary
        ↓
Generate Chart
        ↓
Display Report
```

---

# execute()

```python
def execute(filters=None):

    columns = get_columns()

    data = get_data(filters)

    chart = get_chart(data)

    summary = get_summary(data)

    return columns, data, None, chart, summary
```

---

# Summary Row

```python
summary = [
    {
        "label":"Present Days",
        "value":total_present,
        "indicator":"Green"
    },
    {
        "label":"Absent Days",
        "value":total_absent,
        "indicator":"Red"
    }
]
```

---

# High Absenteeism Color Coding

Condition:

```text
Absent Days > 5
```

Indicator:

```python
if row.absent_days > 5:
    row.indicator = "Red"
```

---

# Chart Design

## Present vs Absent Distribution

```python
chart = {
    "data": {
        "labels": [
            "Present",
            "Absent"
        ],
        "datasets": [
            {
                "values": [
                    total_present,
                    total_absent
                ]
            }
        ]
    },
    "type": "pie"
}
```

---

# Report Diagram

```text
          Employee Report
                  │
      ┌───────────┼───────────┐
      │           │           │
Attendance      Leaves     Reviews
      │           │           │
Present      Leave Types    Score
Absent
Late
```

---

# SQL Safety

Always use:

```python
frappe.db.sql(
    query,
    filters,
    as_dict=True
)
```

Never:

```python
query = f"""
SELECT *
FROM tabEmployee
WHERE department =
'{department}'
"""
```

because:

```text
SQL Injection Risk
```

---

# Performance Considerations

Indexes:

```text
tabAttendance.employee
tabAttendance.attendance_date

tabLeave Application.employee

tabQuarterly Performance Review.employee

tabEmployee.department
```

Benefits:

- Faster filtering
- Reduced query time
- Better report performance

---

# Suggested Screenshots

```text
screenshots/
├── 01_report_filters.png
├── 02_report_output.png
├── 03_summary_row.png
├── 04_absenteeism_color.png
├── 05_chart.png
```

---

# Add Screenshots

```markdown
![Filters](screenshots/01_report_filters.png)

![Report](screenshots/02_report_output.png)

![Chart](screenshots/05_chart.png)
```

---

# End-to-End Flow

```text
Select Date Range
        ↓
Select Department
        ↓
Fetch Employees
        ↓
LEFT JOIN Attendance
        ↓
LEFT JOIN Leave Application
        ↓
LEFT JOIN Performance Reviews
        ↓
Calculate Metrics
        ↓
Generate Summary
        ↓
Generate Chart
        ↓
Display Report
```

---

# Final Folder Structure

```text
custom_hr_pro/
│
├── report/
│
└── employee_attendance_summary/
        ├── employee_attendance_summary.json
        ├── employee_attendance_summary.py
        ├── employee_attendance_summary.js
        ├── TASK3_RESEARCH.md
        ├── TASK3_DESIGN.md
        └── task3_notes.md
```

This report provides a single dashboard combining employee attendance, leave behavior, and performance evaluation while ensuring employees without attendance records are still visible and all SQL queries remain secure and parameterized.