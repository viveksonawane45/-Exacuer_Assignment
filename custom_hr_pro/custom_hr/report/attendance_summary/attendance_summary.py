import frappe
from frappe.utils import add_months, today

def execute(filters=None):
	if not filters:
		filters = {}

	from_date = filters.get("from_date") or add_months(today(), -1)
	to_date = filters.get("to_date") or today()

	columns = [
		{"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
		{"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
		{"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 140},
		{"label": "Present Days", "fieldname": "present_days", "fieldtype": "Int", "width": 100},
		{"label": "Absent Days", "fieldname": "absent_days", "fieldtype": "Int", "width": 100},
		{"label": "Late Arrivals", "fieldname": "late_arrivals", "fieldtype": "Int", "width": 100},
		{"label": "Casual Leave", "fieldname": "casual_leave", "fieldtype": "Float", "width": 110},
		{"label": "Sick Leave", "fieldname": "sick_leave", "fieldtype": "Float", "width": 110},
		{"label": "Latest Review Score", "fieldname": "latest_score", "fieldtype": "Float", "width": 140}
	]

	conditions = ""
	query_args = {
		"from_date": from_date,
		"to_date": to_date
	}

	if filters.get("department"):
		conditions += " AND emp.department = %(department)s"
		query_args["department"] = filters.get("department")

	# Fetch explicit data rows mapping aggregates safely
	data = frappe.db.sql(f"""
		SELECT 
			emp.name as employee,
			emp.employee_name,
			emp.department,
			COUNT(CASE WHEN att.status = 'Present' THEN 1 END) as present_days,
			COUNT(CASE WHEN att.status = 'Absent' THEN 1 END) as absent_days,
			COUNT(CASE WHEN att.status = 'Present' AND att.late_entry = 1 THEN 1 END) as late_arrivals,
			(SELECT IFNULL(SUM(total_leave_days), 0) FROM `tabLeave Application` WHERE employee = emp.name AND docstatus = 1 AND leave_type = 'Casual Leave' AND from_date >= %(from_date)s AND to_date <= %(to_date)s) as casual_leave,
			(SELECT IFNULL(SUM(total_leave_days), 0) FROM `tabLeave Application` WHERE employee = emp.name AND docstatus = 1 AND leave_type = 'Sick Leave' AND from_date >= %(from_date)s AND to_date <= %(to_date)s) as sick_leave,
			(SELECT overall_score FROM `tabPerformance Review` WHERE employee = emp.name AND docstatus = 1 ORDER BY creation DESC LIMIT 1) as latest_score
		FROM 
			`tabEmployee` emp
		LEFT JOIN 
			`tabAttendance` att ON att.employee = emp.name AND att.attendance_date BETWEEN %(from_date)s AND %(to_date)s
		WHERE 
			emp.status = 'Active' {conditions}
		GROUP BY 
			emp.name, emp.employee_name, emp.department
	""", query_args, as_dict=1)

	# Compile the operational dashboard KPIs for data grid summary rendering
	summary = [
		{"value": sum(d.get("present_days", 0) for d in data), "indicator": "Green", "label": "Total Present Headcount"},
		{"value": sum(d.get("absent_days", 0) for d in data), "indicator": "Red", "label": "Total Absent Headcount"}
	]

	# Render Native Chart Configuration Arrays
	chart = {
		"data": {
			"labels": [d["employee_name"] for d in data],
			"datasets": [
				{"name": "Present Days", "values": [d["present_days"] for d in data]},
				{"name": "Absent Days", "values": [d["absent_days"] for d in data]}
			]
		},
		"type": "bar",
		"colors": ["#42A5F5", "#E57373"]
	}

	return columns, data, None, chart, summary
