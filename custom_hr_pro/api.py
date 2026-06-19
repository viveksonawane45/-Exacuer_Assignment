import frappe

@frappe.whitelist()
def get_department_summary():
	"""
	Returns high-level metric summaries matching caller operational validation bounds.
	"""
	# Enforce strict standard role validation profiles checks
	if not ("HR User" in frappe.get_roles() or "HR Manager" in frappe.get_roles() or "System Manager" in frappe.get_roles()):
		frappe.throw("Access Restricted: Unauthorized operational profile matrix configuration.", frappe.PermissionError)

	return frappe.db.sql("""
		SELECT 
			d.name as department,
			COUNT(e.name) as headcount,
			(SELECT IFNULL(AVG(overall_score), 0) FROM `tabPerformance Review` WHERE department = d.name AND docstatus = 1) as avg_review_score
		FROM 
			`tabDepartment` d
		LEFT JOIN 
			`tabEmployee` e ON e.department = d.name AND e.status = 'Active'
		GROUP BY 
			d.name
	""", as_dict=True)
