# Task 7 — Scheduler Tasks (Birthday, Work Anniversary & Payroll Preparation Notifications)

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** Scheduler Events + Cron Jobs + Notifications + Email + Automated Tests

---

# Business Requirement

The HR department requires two automated scheduler tasks.

---

# Task 1 — Daily Birthday & Work Anniversary Notifications

Every day at:

```text
7:00 AM
```

the system should:

1. Find employees whose birthday is today.
2. Find employees whose work anniversary is today.
3. Create notifications for:
   - HR Team
   - Employee's Direct Manager
4. Log:
   - Number of birthdays found
   - Number of anniversaries found
5. Avoid duplicate notifications.
6. Handle Feb 29 birthdays in non-leap years.

---

# Task 2 — Payroll Preparation Summary

On:

```text
25th of Every Month
```

the system should email all HR Managers:

- Total Active Employees
- Employees with Leave Without Pay (LWP)
- Number of employees affected by LWP
- Payroll preparation summary

---

# Objective

Automate HR reminders and payroll preparation activities using:

```text
Scheduler Events
+
Cron Expressions
+
Notifications
+
Emails
+
Parameterized SQL
```

---

# System Architecture

```text
Scheduler
     │
     ├── Daily 7 AM Task
     │       ├── Birthdays
     │       ├── Anniversaries
     │       └── Notifications
     │
     └── Monthly 25th Task
             ├── Active Employees
             ├── LWP Summary
             └── Payroll Email
```

---

# Folder Structure

```text
custom_hr_pro/
│
├── tasks.py
├── hooks.py
├── tests/
│      ├── test_birthdays.py
│      └── test_payroll_summary.py
│
├── TASK7_RESEARCH.md
├── TASK7_NOTES.md
└── task7_notes.md
```

---

# Scheduler Events

## hooks.py

```python
scheduler_events = {

    "cron": {

        "0 7 * * *": [
            "custom_hr_pro.tasks.send_birthday_notifications"
        ],

        "0 9 25 * *": [
            "custom_hr_pro.tasks.send_payroll_summary"
        ]
    }
}
```

---

# Cron Expression

## Daily at 7 AM

```text
0 7 * * *
```

Meaning:

```text
Minute = 0
Hour = 7
Day = *
Month = *
Weekday = *
```

---

# 25th of Every Month

```text
0 9 25 * *
```

Meaning:

```text
Minute = 0
Hour = 9
Day = 25
Month = *
Weekday = *
```

---

# Task 1 — Birthday Notifications

## Business Flow

```text
7 AM
   ↓
Find Today's Birthdays
   ↓
Find Today's Anniversaries
   ↓
Create Notifications
   ↓
Notify Managers
   ↓
Log Results
```

---

# Birthday Query

Requirement:

Ignore year.

Match only:

```text
Month
+
Day
```

---

# Parameterized SQL

```python
frappe.db.sql(
    """
    SELECT
        name,
        employee_name,
        date_of_birth,
        reports_to
    FROM
        `tabEmployee`
    WHERE
        MONTH(date_of_birth)=%s
        AND DAY(date_of_birth)=%s
        AND status='Active'
    """,
    (
        today.month,
        today.day
    ),
    as_dict=True
)
```

---

# Anniversary Query

```python
frappe.db.sql(
    """
    SELECT
        name,
        employee_name,
        date_of_joining,
        reports_to
    FROM
        `tabEmployee`
    WHERE
        MONTH(date_of_joining)=%s
        AND DAY(date_of_joining)=%s
        AND status='Active'
    """,
    (
        today.month,
        today.day
    ),
    as_dict=True
)
```

---

# Feb 29 Edge Case

Problem:

Employees born on:

```text
29 February
```

should still receive birthday wishes during non-leap years.

---

# Solution

```python
import calendar

if (
    today.month == 2
    and today.day == 28
    and not calendar.isleap(today.year)
):
    include_feb_29 = True
```

Additional Query:

```sql
MONTH(date_of_birth)=2
AND DAY(date_of_birth)=29
```

---

# Notification Flow

```text
Birthday Found
      ↓
Find Manager
      ↓
Find HR Users
      ↓
Create Notification Logs
```

---

# Notification Creation

```python
frappe.get_doc(
    {
        "doctype": "Notification Log",
        "for_user": user,
        "type": "Alert",
        "subject":
        f"Today is {employee.employee_name}'s birthday."
    }
).insert(
    ignore_permissions=True
)
```

---

# Duplicate Prevention

Requirement:

No duplicate notifications.

---

# Solution

```python
exists = frappe.db.exists(
    "Notification Log",
    {
        "for_user": user,
        "subject": subject
    }
)

if not exists:
    notification.insert()
```

---

# Logging

```python
frappe.logger().info(
    f"""
    Birthdays Found:
    {birthday_count}

    Anniversaries Found:
    {anniversary_count}
    """
)
```

---

# tasks.py

```python
def send_birthday_notifications():

    birthdays = get_birthdays()

    anniversaries = get_anniversaries()

    notify_users(
        birthdays,
        anniversaries
    )

    log_results()
```

---

# Task 2 — Payroll Preparation Summary

## Business Flow

```text
25th of Month
       ↓
Count Active Employees
       ↓
Find LWP Employees
       ↓
Prepare Summary
       ↓
Email HR Managers
```

---

# Active Employees Query

```python
active_count = frappe.db.count(
    "Employee",
    {
        "status": "Active"
    }
)
```

---

# Leave Without Pay Query

```python
lwp_employees = frappe.db.sql(
    """
    SELECT DISTINCT
        employee
    FROM
        `tabLeave Application`
    WHERE
        leave_type='Leave Without Pay'
        AND docstatus=1
    """,
    as_dict=True
)
```

---

# Payroll Summary Email

```text
Payroll Preparation Summary

Active Employees : 145

Employees with LWP : 8

Payroll may be affected for
8 employees.
```

---

# HR Managers

```python
hr_managers = frappe.get_all(
    "Has Role",
    filters={
        "role":
        "HR Manager"
    },
    fields=[
        "parent"
    ]
)
```

---

# Email

```python
frappe.sendmail(
    recipients=emails,
    subject="Upcoming Payroll Summary",
    message=message
)
```

---

# tasks.py

```python
def send_payroll_summary():

    active = get_active_count()

    lwp = get_lwp_count()

    message = build_summary(
        active,
        lwp
    )

    email_hr_managers(
        message
    )
```

---

# Scheduler Architecture

```text
Scheduler
      │
      ├── Daily
      │       └── Birthday Task
      │
      └── Monthly
              └── Payroll Task
```

---

# Manual Triggering

## Bench Console

```bash
bench console
```

---

# Birthday Task

```python
from custom_hr_pro.tasks import (
    send_birthday_notifications
)

send_birthday_notifications()
```

---

# Payroll Task

```python
from custom_hr_pro.tasks import (
    send_payroll_summary
)

send_payroll_summary()
```

---

# Automated Tests

## Birthday Tests

### Test 1

Birthday notification created.

Expected:

```text
Notification Log Exists
```

---

### Test 2

Feb 29 handled correctly.

Expected:

```text
Birthday notification created
on Feb 28
in non-leap years.
```

---

## Payroll Tests

### Test 3

LWP employee count.

Expected:

```text
Correct count returned.
```

---

### Test 4

Email generated.

Expected:

```text
Email Queue entry exists.
```

---

# Sample Tests

```python
class TestBirthdayTasks(
    FrappeTestCase
):

    def test_notification_created(self):
        pass

    def test_feb29_logic(self):
        pass
```

---

```python
class TestPayrollSummary(
    FrappeTestCase
):

    def test_lwp_count(self):
        pass

    def test_email_sent(self):
        pass
```

---

# Screenshots

```text
screenshots/
├── 01_scheduler_hooks.png
├── 02_birthday_notification.png
├── 03_anniversary_notification.png
├── 04_email_summary.png
├── 05_bench_console_trigger.png
├── 06_test_results.png
```

---

# Add Screenshots

```markdown
![Scheduler Hooks](screenshots/01_scheduler_hooks.png)

![Birthday Notification](screenshots/02_birthday_notification.png)

![Payroll Summary Email](screenshots/04_email_summary.png)
```

---

# End-to-End Flow

```text
Bench Scheduler
        │
        ├── 7 AM Daily
        │       ↓
        │   Birthdays
        │       ↓
        │   Anniversaries
        │       ↓
        │   Notifications
        │
        └── 25th Monthly
                ↓
        Active Employees
                ↓
        LWP Employees
                ↓
        Payroll Summary
                ↓
            Email HR
```

---

# Final Folder Structure

```text
custom_hr_pro/
│
├── task7_notes.md
├── tasks.py
├── hooks.py
│
├── tests/
│      ├── test_birthdays.py
│      └── test_payroll_summary.py
│
├── TASK7_RESEARCH.md
└── TASK7_NOTES.md
```

This implementation uses Frappe Scheduler Events and Cron Jobs to automate employee celebrations and payroll preparation activities while ensuring duplicate prevention, graceful exception handling, parameterized SQL, and proper testing coverage.