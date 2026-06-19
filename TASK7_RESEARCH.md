# Task 7 - Scheduler Tasks Research

## Cron Expressions & Scheduler Events
The scheduler events are mapped inside `hooks.py` to trigger tasks at specific periodic frequencies:
1. `send_birthday_notifications` -> runs daily at 7:00 AM (`0 7 * * *`)
2. `send_payroll_summary` -> runs monthly on the 25th at 9:00 AM (`0 9 25 * *`)

## Date Logic & Leap Anomaly (Feb 29)
- Leap day occurs once every four years. On non-leap years, employees born on February 29 will not have their birthdays matched.
- Protection mechanism: On February 28 of any non-leap year (checked via python `calendar.isleap(year)`), the query expands to fetch employees with birth dates/joining dates on either the 28th or 29th of February.

## Duplicate Alert Prevention
- Before creating a Notification Log, the system runs `frappe.db.exists` matching both target recipient (`for_user`) and subject text to guarantee no redundant alerts.
- Log notifications are routed to direct managers (Employee `reports_to` link user_id) and all active users with the roles "HR User" or "HR Manager".

## Payroll Summary Criteria
- Count of active employees matching status "Active".
- Count of employees with approved and submitted (`docstatus = 1`) "Leave Without Pay" leave types.
- Generated message matches the standard template and is emailed to all "HR Manager" role users.
