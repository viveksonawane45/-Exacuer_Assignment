import frappe
from frappe.tests import IntegrationTestCase
from custom_hr_pro.custom_hr.report.attendance_summary.attendance_summary import execute as execute_attendance_report

class TestReportsAndFormats(IntegrationTestCase):
	def setUp(self):
		frappe.db.rollback()

	def test_attendance_summary_report(self):
		# Verify that the report returns columns and a valid list of records
		columns, data, message, chart, summary = execute_attendance_report()
		self.assertGreater(len(columns), 0)
		self.assertEqual(type(data), list)
		self.assertIsNotNone(chart)
		self.assertGreater(len(summary), 0)

	def test_print_format_exists(self):
		# Verify that the print format exists and is standard
		self.assertTrue(frappe.db.exists("Print Format", "Premium Two-Column Salary Slip"))
		pf = frappe.get_doc("Print Format", "Premium Two-Column Salary Slip")
		self.assertEqual(pf.doc_type, "Salary Slip")
		self.assertEqual(pf.print_format_type, "Jinja")
