import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today

class IntegrationTestPerformanceReview(IntegrationTestCase):
	def setUp(self):
		frappe.db.rollback()
		# Ensure employee naming is set to Employee Number so we can force IDs
		frappe.db.set_single_value("HR Settings", "emp_created_by", "Employee Number")

		# 1. Setup Fiscal Year
		existing_fy = frappe.db.get_value("Fiscal Year", {}, "name")
		if existing_fy:
			self.fiscal_year = existing_fy
		else:
			self.fiscal_year = "2026"
			frappe.get_doc({
				"doctype": "Fiscal Year",
				"year": "2026",
				"year_start_date": "2026-01-01",
				"year_end_date": "2026-12-31"
			}).insert(ignore_permissions=True)

		# 2. Setup Company
		if not frappe.db.exists("Company", "Test Company"):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": "Test Company",
				"abbr": "TC",
				"default_currency": "USD"
			}).insert(ignore_permissions=True)

		# 3. Setup Department
		if not frappe.db.exists("Department", "Test Dept 1 - TC"):
			frappe.get_doc({
				"doctype": "Department",
				"department_name": "Test Dept 1",
				"company": "Test Company"
			}).insert(ignore_permissions=True)

		# 4. Setup Manager Employee
		if not frappe.db.exists("Employee", "EMP-MGR-01"):
			mgr = frappe.get_doc({
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
			})
			# Make sure User exists for the manager
			if not frappe.db.exists("User", "test_mgr@example.com"):
				frappe.get_doc({
					"doctype": "User",
					"email": "test_mgr@example.com",
					"first_name": "Manager",
					"roles": [{"role": "HR Manager"}, {"role": "System Manager"}]
				}).insert(ignore_permissions=True)
			mgr.insert(ignore_permissions=True)

		# 5. Setup Test Employee
		if not frappe.db.exists("Employee", "EMP-TEST-01"):
			emp = frappe.get_doc({
				"doctype": "Employee",
				"employee_name": "Test Employee 1",
				"first_name": "Test Employee 1",
				"gender": "Male",
				"date_of_birth": "1995-01-01",
				"naming_rule": "Set by Name",
				"name": "EMP-TEST-01",
				"employee_number": "EMP-TEST-01",
				"date_of_joining": add_days(today(), -35), # More than 30 days
				"status": "Active",
				"company": "Test Company",
				"reports_to": "EMP-MGR-01",
				"department": "Test Dept 1 - TC",
				"custom_data_privacy_agreement_signed": 0
			})
			emp.insert(ignore_permissions=True)

		# 5. Clear messages log
		frappe.local.message_log = []

	def test_employee_privacy_agreement_warning(self):
		emp = frappe.get_doc("Employee", "EMP-TEST-01")
		emp.custom_data_privacy_agreement_signed = 0
		emp.date_of_joining = add_days(today(), -35)
		
		frappe.local.message_log = []
		emp.save(ignore_permissions=True)
		
		# Assert a warning message was shown
		warnings = [str(msg) for msg in frappe.local.message_log]
		self.assertTrue(any("Data Privacy Agreement" in w for w in warnings), f"Warning not found in: {warnings}")

		# Mark signed and check warning disappears
		emp.custom_data_privacy_agreement_signed = 1
		emp.custom_privacy_agreement_signed_date = today()
		frappe.local.message_log = []
		emp.save(ignore_permissions=True)
		
		warnings = [str(msg) for msg in frappe.local.message_log]
		self.assertFalse(any("Data Privacy Agreement" in w for w in warnings))

	def test_performance_review_uniqueness_and_calculations(self):
		# Create clean Performance Review
		# Cleanup existing
		frappe.db.delete("Performance Review KPI")
		frappe.db.delete("Performance Review")

		pr = frappe.get_doc({
			"doctype": "Performance Review",
			"employee": "EMP-TEST-01",
			"fiscal_year": self.fiscal_year,
			"quarter": "Q1",
			"kpis": [
				{
					"goal": "Goal 1",
					"target_value": 10,
					"achieved_value": 8,
					"score": "4"
				},
				{
					"goal": "Goal 2",
					"target_value": 100,
					"achieved_value": 20,
					"score": "2"
				}
			]
		})
		pr.insert(ignore_permissions=True)
		
		# Assert overall score is average: (4 + 2) / 2 = 3.0
		self.assertEqual(pr.overall_score, 3.0)

		# Try to create a duplicate review for same Q1
		pr_dup = frappe.get_doc({
			"doctype": "Performance Review",
			"employee": "EMP-TEST-01",
			"fiscal_year": self.fiscal_year,
			"quarter": "Q1",
			"kpis": []
		})
		self.assertRaises(frappe.ValidationError, pr_dup.insert)

	def test_performance_review_low_score_todo(self):
		frappe.db.delete("ToDo", {"reference_type": "Performance Review"})
		
		pr = frappe.get_doc({
			"doctype": "Performance Review",
			"employee": "EMP-TEST-01",
			"fiscal_year": self.fiscal_year,
			"quarter": "Q2",
			"kpis": [
				{
					"goal": "Goal Low",
					"target_value": 10,
					"achieved_value": 1,
					"score": "1"
				}
			]
		})
		pr.insert(ignore_permissions=True)
		pr.submit()

		# Todo should be created for manager test_mgr@example.com
		todos = frappe.get_all("ToDo", filters={
			"reference_type": "Performance Review",
			"reference_name": pr.name
		}, fields=["allocated_to", "description"])
		self.assertEqual(len(todos), 1)
		self.assertEqual(todos[0].allocated_to, "test_mgr@example.com")
		self.assertIn("PIP", todos[0].description)

	def test_performance_review_high_score_comment(self):
		frappe.db.delete("Comment", {"reference_doctype": "Employee", "reference_name": "EMP-TEST-01"})
		
		pr = frappe.get_doc({
			"doctype": "Performance Review",
			"employee": "EMP-TEST-01",
			"fiscal_year": self.fiscal_year,
			"quarter": "Q3",
			"kpis": [
				{
					"goal": "Goal High",
					"target_value": 10,
					"achieved_value": 10,
					"score": "5"
				}
			]
		})
		pr.insert(ignore_permissions=True)
		pr.submit()

		# Comment should be created on Employee
		comments = frappe.get_all("Comment", filters={
			"reference_doctype": "Employee",
			"reference_name": "EMP-TEST-01"
		}, fields=["content"])
		self.assertEqual(len(comments), 1)
		self.assertIn("High Performer", comments[0].content)

	def test_leave_application_reason_requirement(self):
		# Setup Leave Type
		if not frappe.db.exists("Leave Type", "Casual Leave"):
			frappe.get_doc({
				"doctype": "Leave Type",
				"leave_type_name": "Casual Leave",
				"max_continuous_days_allowed": 0
			}).insert(ignore_permissions=True)
		else:
			frappe.db.set_value("Leave Type", "Casual Leave", "max_continuous_days_allowed", 0)

		# Setup Leave Allocation to avoid validation errors
		if not frappe.db.exists("Leave Allocation", {"employee": "EMP-TEST-01", "leave_type": "Casual Leave", "from_date": "2026-01-01"}):
			alloc = frappe.get_doc({
				"doctype": "Leave Allocation",
				"employee": "EMP-TEST-01",
				"leave_type": "Casual Leave",
				"from_date": "2026-01-01",
				"to_date": "2026-12-31",
				"new_leaves_allocated": 15,
				"company": "Test Company"
			})
			alloc.insert(ignore_permissions=True)
			alloc.submit()

		# Make sure leave application doesn't exist
		frappe.db.delete("Leave Application", {"employee": "EMP-TEST-01"})

		# Create Leave Application > 5 days with no reason
		la = frappe.get_doc({
			"doctype": "Leave Application",
			"employee": "EMP-TEST-01",
			"leave_type": "Casual Leave",
			"from_date": "2026-06-01",
			"to_date": "2026-06-07", # 7 days
			"company": "Test Company",
			"reason": ""
		})
		
		# Validation should throw because total days is 7 > 5 and reason is empty
		self.assertRaises(frappe.ValidationError, la.insert)

		# Add reason and it should pass
		la.reason = "Vacation"
		la.insert(ignore_permissions=True)
		self.assertIsNotNone(la.name)
