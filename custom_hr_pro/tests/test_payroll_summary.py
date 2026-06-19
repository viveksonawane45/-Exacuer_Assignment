import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days
from custom_hr_pro.tasks import send_payroll_summary

class TestPayrollSummary(IntegrationTestCase):
	def setUp(self):
		frappe.db.rollback()
		# Make sure HR Settings employee naming is standard
		frappe.db.set_single_value("HR Settings", "emp_created_by", "Employee Number")

		# Clear existing Leave Applications, Email Queue, and Assignments
		frappe.db.delete("Leave Application", {"employee": ["in", ["EMP-TEST-01", "EMP-MGR-01"]]})
		frappe.db.delete("Email Queue")
		frappe.db.delete("Employee", {"employee_number": ["in", ["EMP-TEST-01", "EMP-MGR-01"]]})
		frappe.db.delete("Holiday List Assignment")
		
		# 1. Setup Holiday List
		if not frappe.db.exists("Holiday List", "Test Holiday List"):
			hl = frappe.get_doc({
				"doctype": "Holiday List",
				"holiday_list_name": "Test Holiday List",
				"from_date": "2026-01-01",
				"to_date": "2026-12-31"
			})
			hl.insert(ignore_permissions=True)

		# 2. Setup Company
		if not frappe.db.exists("Company", "Test Company"):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": "Test Company",
				"abbr": "TC",
				"default_currency": "USD"
			}).insert(ignore_permissions=True)

		# 3. Setup Holiday List Assignment for the Company
		if not frappe.db.exists("Holiday List Assignment", {"assigned_to": "Test Company", "holiday_list": "Test Holiday List"}):
			hla = frappe.get_doc({
				"doctype": "Holiday List Assignment",
				"holiday_list": "Test Holiday List",
				"applicable_for": "Company",
				"assigned_to": "Test Company",
				"from_date": "2026-01-01"
			})
			hla.insert(ignore_permissions=True)
			hla.submit()

		# 4. Setup HR Manager User
		if not frappe.db.exists("User", "test_mgr@example.com"):
			frappe.get_doc({
				"doctype": "User",
				"email": "test_mgr@example.com",
				"first_name": "Manager",
				"roles": [{"role": "HR Manager"}, {"role": "System Manager"}]
			}).insert(ignore_permissions=True)

		# 5. Setup manager Employee
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

		# 6. Setup a test employee
		if not frappe.db.exists("Employee", "EMP-TEST-01"):
			frappe.get_doc({
				"doctype": "Employee",
				"employee_name": "Test Employee 1",
				"first_name": "Test Employee 1",
				"gender": "Male",
				"date_of_birth": "1995-01-01",
				"naming_rule": "Set by Name",
				"name": "EMP-TEST-01",
				"employee_number": "EMP-TEST-01",
				"date_of_joining": "2024-01-01",
				"status": "Active",
				"company": "Test Company",
				"reports_to": "EMP-MGR-01"
			}).insert(ignore_permissions=True)

		# 7. Setup Leave Type
		if not frappe.db.exists("Leave Type", "Leave Without Pay"):
			frappe.get_doc({
				"doctype": "Leave Type",
				"leave_type_name": "Leave Without Pay",
				"is_lwp": 1
			}).insert(ignore_permissions=True)

	def test_lwp_count(self):
		# Create an approved Leave Without Pay application
		la = frappe.get_doc({
			"doctype": "Leave Application",
			"employee": "EMP-TEST-01",
			"leave_type": "Leave Without Pay",
			"from_date": today(),
			"to_date": add_days(today(), 2),
			"company": "Test Company",
			"status": "Approved"
		})
		la.insert(ignore_permissions=True)
		la.submit()

		# Run payroll summary trigger
		send_payroll_summary()

		# Verify email content in queue
		email_queues = frappe.get_all("Email Queue", fields=["message"])
		self.assertGreater(len(email_queues), 0)
		
		# Find the payroll summary email in queue
		payroll_email = None
		for eq in email_queues:
			if "Payroll Preparation Summary" in eq.message:
				payroll_email = eq
				break
				
		self.assertIsNotNone(payroll_email)
		self.assertIn("EMP-TEST-01", payroll_email.message)
		self.assertIn("Employees with LWP : EMP-TEST-01", payroll_email.message)
