# Task 9 - HR Analytics Dashboard Research

## Backend APIs design
Whitelisted endpoints are registered at `custom_hr_pro.api.dashboard.*`:
1. `get_total_employees` - count of all employees.
2. `get_active_employees` - active employees count.
3. `get_employees_on_leave` - active approved leave applications today.
4. `get_average_performance` - average performance score from `Performance Review` records.
5. `get_department_distribution` - count of active employees grouped by department.
6. `get_top_performers` - top 10 submitted reviews.
7. `get_high_absenteeism` - count of absent days > 5.

## Authentication Flow
- Session cookies (`sid`) are managed by Frappe upon hitting `/api/method/login`.
- Axios uses `withCredentials: true` to authenticate subsequent calls.
