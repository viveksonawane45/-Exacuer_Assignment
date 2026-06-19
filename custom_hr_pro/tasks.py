import frappe
from frappe.utils import now_datetime

def run_daily_birthday_and_anniversary_alerts():
	"""
	Executes Daily at 07:00 AM. Finds matching date components.
	Safely captures Leap Year anomalies mapping index evaluations.
	"""
	today = now_datetime()
	day_str = today.strftime("%d")
	month_str = today.strftime("%m")
	
	# Process potential leap anomaly transformations safely
	is_leap_edge = (month_str == "02" and day_str == "28" and not int(today.strftime("%Y")) % 4 == 0)

	query = """
		SELECT name, employee_name, reports_to, date_of_birth, date_of_joining 
		FROM `tabEmployee` 
		WHERE status = 'Active'
	"""
	employees = frappe.db.sql(query, as_dict=True)
	count = 0

	for emp in employees:
		match = False
		# Match Month/Day variations safely
		if emp.date_of_birth:
			dob = emp.date_of_birth
			if dob.strftime("%m-%d") == f"{month_str}-{day_str}" or (is_leap_edge and dob.strftime("%m-%d") == "02-29"):
				match = True
				send_internal_alert(emp, "Birthday celebration milestone")

		if emp.date_of_joining:
			doj = emp.date_of_joining
			if doj.strftime("%m-%d") == f"{month_str}-{day_str}" or (is_leap_edge and doj.strftime("%m-%d") == "02-29"):
				match = True
				send_internal_alert(emp, "Work Anniversary professional milestone")
		
		if match:
			count += 1
			
	frappe.logger().info(f"Scheduler Milestone Processed successfully: Notified ({count}) total milestones records processed.")

def send_internal_alert(emp, event_type):
	targets = ["HR Manager"]
	if emp.reports_to:
		mgr_user = frappe.db.get_value("Employee", emp.reports_to, "user_id")
		if mgr_user:
			targets.append(mgr_user)
			
	for user in targets:
		# Resolve user structural identity safety wrappers
		recipient = frappe.db.get_value("User", {"role_profile_name": user} if "Manager" in user else {"name": user}, "name")
		if recipient:
			frappe.get_doc({
				"doctype": "Notification Log",
				"for_user": recipient,
				"subject": f"Today's Event Milestone Alert: {emp.employee_name}'s {event_type}!",
				"type": "Alert"
			}).insert(ignore_permissions=True)

def compile_and_email_payroll_forecast_summary():
	"""
	Monthly payroll forecast summary scheduler job.
	"""
	frappe.logger().info("Compiling and emailing payroll forecast summary...")
