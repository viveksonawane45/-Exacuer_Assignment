import frappe
import calendar
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days
from custom_hr_pro.tasks import send_birthday_notifications
from unittest.mock import patch

class TestBirthdayTasks(IntegrationTestCase):
	def setUp(self):
		frappe.db.rollback()
		# Clear existing notification logs and test employees to avoid contamination
		frappe.db.delete("Notification Log")
		frappe.db.delete("Employee", {"employee_number": ["in", ["EMP-BDAY-01", "EMP-BDAY-FEB29", "EMP-MGR-01"]]})
		
		# Make sure HR Settings employee naming is standard
		frappe.db.set_single_value("HR Settings", "emp_created_by", "Employee Number")
		
		# 1. Setup Company
		if not frappe.db.exists("Company", "Test Company"):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": "Test Company",
				"abbr": "TC",
				"default_currency": "USD"
			}).insert(ignore_permissions=True)

		# 2. Setup HR Manager User
		if not frappe.db.exists("User", "test_mgr@example.com"):
			frappe.get_doc({
				"doctype": "User",
				"email": "test_mgr@example.com",
				"first_name": "Manager",
				"roles": [{"role": "HR Manager"}, {"role": "System Manager"}]
			}).insert(ignore_permissions=True)

		# 3. Setup HR User
		if not frappe.db.exists("User", "test_hr_user@example.com"):
			frappe.get_doc({
				"doctype": "User",
				"email": "test_hr_user@example.com",
				"first_name": "HR User",
				"roles": [{"role": "HR User"}]
			}).insert(ignore_permissions=True)

		# 4. Setup manager Employee
		if not frappe.db.exists("Employee", "EMP-MGR-01"):
			frappe.get_doc({
				"doctype": "Employee",
				"employee_name": "Manager Employee",
				"first_name": "Manager Employee",
				"gender": "Male",
				"date_of_birth": "1990-01-01",
				"naming_rule": "Set by Name",
				"name": "EMP-MGR-01",
				"employee_number": "EMP-MGR-01",
				"date_of_joining": "2020-01-01",
				"status": "Active",
				"company": "Test Company",
				"user_id": "test_mgr@example.com"
			}).insert(ignore_permissions=True)

	def test_notification_created(self):
		# Create an employee whose birthday is today
		today_str = today()
		
		emp = frappe.get_doc({
			"doctype": "Employee",
			"employee_name": "Birthday Emp 1",
			"first_name": "Birthday Emp 1",
			"naming_rule": "Set by Name",
			"name": "EMP-BDAY-01",
			"employee_number": "EMP-BDAY-01",
			"gender": "Female",
			"date_of_birth": today_str,
			"date_of_joining": today_str,
			"status": "Active",
			"company": "Test Company",
			"reports_to": "EMP-MGR-01"
		})
		emp.insert(ignore_permissions=True)
		
		# Run daily notification trigger
		send_birthday_notifications()
		
		# Check if Notification Log was created for the manager and HR User
		manager_notif = frappe.db.exists("Notification Log", {
			"for_user": "test_mgr@example.com",
			"subject": "Today is Birthday Emp 1's birthday."
		})
		hr_notif = frappe.db.exists("Notification Log", {
			"for_user": "test_hr_user@example.com",
			"subject": "Today is Birthday Emp 1's birthday."
		})
		
		self.assertTrue(manager_notif)
		self.assertTrue(hr_notif)

	def test_feb29_logic(self):
		emp = frappe.get_doc({
			"doctype": "Employee",
			"employee_name": "Birthday Emp 2",
			"first_name": "Birthday Emp 2",
			"naming_rule": "Set by Name",
			"name": "EMP-BDAY-FEB29",
			"employee_number": "EMP-BDAY-FEB29",
			"gender": "Male",
			"date_of_birth": "2000-02-29",  # Born on Leap Day
			"date_of_joining": "2024-01-01",
			"status": "Active",
			"company": "Test Company",
			"reports_to": "EMP-MGR-01"
		})
		emp.insert(ignore_permissions=True)
		
		# Mock today() to return Feb 28 of a non-leap year (e.g. 2025-02-28)
		with patch("custom_hr_pro.tasks.today", return_value="2025-02-28"):
			send_birthday_notifications()
			
		# In a non-leap year on Feb 28, Feb 29 birthday should be notified
		manager_notif = frappe.db.exists("Notification Log", {
			"for_user": "test_mgr@example.com",
			"subject": "Today is Birthday Emp 2's birthday."
		})
		self.assertTrue(manager_notif)
