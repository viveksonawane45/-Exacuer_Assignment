# Copyright (c) 2026, DeepMind Pair Programmer and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today

@frappe.whitelist()
def get_total_employees():
	return frappe.db.count("Employee")

@frappe.whitelist()
def get_active_employees():
	return frappe.db.count("Employee", {"status": "Active"})

@frappe.whitelist()
def get_employees_on_leave():
	return frappe.db.count(
		"Leave Application",
		{
			"from_date": ["<=", today()],
			"to_date": [">=", today()],
			"status": "Approved"
		}
	)

@frappe.whitelist()
def get_average_performance():
	# Use Performance Review doctype as defined in custom_hr
	result = frappe.db.sql(
		"""
		SELECT
			AVG(overall_score)
		FROM
			`tabPerformance Review`
		WHERE
			docstatus = 1
		""",
		as_list=True
	)
	return result[0][0] or 0.0

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

@frappe.whitelist()
def get_top_performers():
	return frappe.db.sql(
		"""
		SELECT
			employee,
			employee_name,
			overall_score
		FROM
			`tabPerformance Review`
		WHERE
			docstatus = 1
		ORDER BY
			overall_score DESC
		LIMIT 10
		""",
		as_dict=True
	)

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
