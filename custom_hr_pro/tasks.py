# Copyright (c) 2026, DeepMind Pair Programmer and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe.utils import today
from datetime import datetime

def send_birthday_notifications():
	"""
	Daily Birthday & Work Anniversary Notifications.
	Finds active employees whose birthday or work anniversary is today,
	creates Notification Logs for HR Team and Employee's Direct Manager,
	and logs the summary.
	"""
	today_str = today()
	today_dt = datetime.strptime(today_str, "%Y-%m-%d")
	
	is_leap = calendar.isleap(today_dt.year)
	is_feb28_non_leap = (today_dt.month == 2 and today_dt.day == 28 and not is_leap)
	
	# Fetch Birthdays
	if is_feb28_non_leap:
		birthdays = frappe.db.sql("""
			SELECT name, employee_name, reports_to, date_of_birth
			FROM `tabEmployee`
			WHERE MONTH(date_of_birth) = 2
			  AND DAY(date_of_birth) IN (28, 29)
			  AND status = 'Active'
		""", as_dict=True)
	else:
		birthdays = frappe.db.sql("""
			SELECT name, employee_name, reports_to, date_of_birth
			FROM `tabEmployee`
			WHERE MONTH(date_of_birth) = %s
			  AND DAY(date_of_birth) = %s
			  AND status = 'Active'
		""", (today_dt.month, today_dt.day), as_dict=True)
		
	# Fetch Anniversaries
	if is_feb28_non_leap:
		anniversaries = frappe.db.sql("""
			SELECT name, employee_name, reports_to, date_of_joining
			FROM `tabEmployee`
			WHERE MONTH(date_of_joining) = 2
			  AND DAY(date_of_joining) IN (28, 29)
			  AND status = 'Active'
		""", as_dict=True)
	else:
		anniversaries = frappe.db.sql("""
			SELECT name, employee_name, reports_to, date_of_joining
			FROM `tabEmployee`
			WHERE MONTH(date_of_joining) = %s
			  AND DAY(date_of_joining) = %s
			  AND status = 'Active'
		""", (today_dt.month, today_dt.day), as_dict=True)
		
	# Get HR Users and verify they exist in User doctype
	has_role = frappe.get_all("Has Role", filters={"role": ["in", ["HR User", "HR Manager"]]}, fields=["parent"])
	hr_users = []
	for r in has_role:
		if r.parent and frappe.db.exists("User", r.parent):
			hr_users.append(r.parent)
	hr_users = list(set(hr_users))
	
	birthday_count = len(birthdays)
	anniversary_count = len(anniversaries)
	
	# Send Birthday Notifications
	for emp in birthdays:
		subject = f"Today is {emp.employee_name}'s birthday."
		targets = list(hr_users)
		
		if emp.reports_to:
			mgr_user = frappe.db.get_value("Employee", emp.reports_to, "user_id")
			if mgr_user and frappe.db.exists("User", mgr_user) and mgr_user not in targets:
				targets.append(mgr_user)
				
		for user in targets:
			if not frappe.db.exists("Notification Log", {"for_user": user, "subject": subject}):
				frappe.get_doc({
					"doctype": "Notification Log",
					"for_user": user,
					"type": "Alert",
					"subject": subject
				}).insert(ignore_permissions=True)
				
	# Send Anniversary Notifications
	for emp in anniversaries:
		subject = f"Today is {emp.employee_name}'s work anniversary."
		targets = list(hr_users)
		
		if emp.reports_to:
			mgr_user = frappe.db.get_value("Employee", emp.reports_to, "user_id")
			if mgr_user and frappe.db.exists("User", mgr_user) and mgr_user not in targets:
				targets.append(mgr_user)
				
		for user in targets:
			if not frappe.db.exists("Notification Log", {"for_user": user, "subject": subject}):
				frappe.get_doc({
					"doctype": "Notification Log",
					"for_user": user,
					"type": "Alert",
					"subject": subject
				}).insert(ignore_permissions=True)
				
	frappe.logger().info(
		f"""
    Birthdays Found:
    {birthday_count}

    Anniversaries Found:
    {anniversary_count}
    """
	)

def send_payroll_summary():
	"""
	Payroll Preparation Summary.
	Count active employees, count employees with Leave Without Pay,
	prepare summary report, and email all HR Managers.
	"""
	active_count = frappe.db.count("Employee", {"status": "Active"})
	
	lwp_employees = frappe.db.sql("""
		SELECT DISTINCT employee FROM `tabLeave Application`
		WHERE leave_type = 'Leave Without Pay' AND docstatus = 1
	""", as_dict=True)
	
	lwp_count = len(lwp_employees)
	lwp_list_str = ", ".join([d.employee for d in lwp_employees]) if lwp_count > 0 else "None"
	
	message = f"""
Payroll Preparation Summary

Active Employees : {active_count}

Employees with LWP : {lwp_list_str}

Payroll may be affected for
{lwp_count} employees.
"""
	
	hr_managers = frappe.get_all("Has Role", filters={"role": "HR Manager"}, fields=["parent"])
	emails = []
	for r in hr_managers:
		if r.parent and frappe.db.exists("User", r.parent):
			emails.append(r.parent)
	emails = list(set(emails))
	
	if emails:
		frappe.sendmail(
			recipients=emails,
			subject="Upcoming Payroll Summary",
			message=message
		)

# For backward compatibility
def run_daily_birthday_and_anniversary_alerts():
	send_birthday_notifications()

def compile_and_email_payroll_forecast_summary():
	send_payroll_summary()
