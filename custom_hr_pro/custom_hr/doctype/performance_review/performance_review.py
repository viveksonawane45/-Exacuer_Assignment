# Copyright (c) 2026, DeepMind Pair Programmer and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class PerformanceReview(Document):
	def validate(self):
		self.calculate_overall_score()
		self.validate_uniqueness()
		self.set_manager_name()

	def calculate_overall_score(self):
		if self.kpis:
			total_score = 0.0
			count = 0
			for kpi in self.kpis:
				if kpi.score:
					total_score += float(kpi.score)
					count += 1
			if count > 0:
				self.overall_score = total_score / count
			else:
				self.overall_score = 0.0
		else:
			self.overall_score = None

	def validate_uniqueness(self):
		duplicate = frappe.db.exists(
			"Performance Review",
			{
				"employee": self.employee,
				"fiscal_year": self.fiscal_year,
				"quarter": self.quarter,
				"name": ["!=", self.name]
			}
		)
		if duplicate:
			frappe.throw(
				_("Performance Review already exists for Employee {0} for {1} {2}").format(
					self.employee, self.quarter, self.fiscal_year
				),
				frappe.ValidationError
			)

	def set_manager_name(self):
		reports_to = frappe.db.get_value("Employee", self.employee, "reports_to")
		if reports_to:
			self.manager_name = frappe.db.get_value("Employee", reports_to, "employee_name")
		else:
			self.manager_name = None

	def on_submit(self):
		if self.overall_score is not None:
			if self.overall_score < 2.0:
				self.create_pip_todo()
			elif self.overall_score > 4.0:
				self.create_high_performer_comment()

	def create_pip_todo(self):
		reports_to = frappe.db.get_value("Employee", self.employee, "reports_to")
		if reports_to:
			manager_user_id = frappe.db.get_value("Employee", reports_to, "user_id")
			if manager_user_id:
				todo = frappe.get_doc({
					"doctype": "ToDo",
					"allocated_to": manager_user_id,
					"description": _("PIP Action Required: Low performance score ({0}) for employee {1}").format(
						self.overall_score, self.employee_name or self.employee
					),
					"reference_type": "Performance Review",
					"reference_name": self.name
				})
				todo.insert(ignore_permissions=True)

	def create_high_performer_comment(self):
		comment = frappe.get_doc({
			"doctype": "Comment",
			"comment_type": "Comment",
			"reference_doctype": "Employee",
			"reference_name": self.employee,
			"content": _("High Performer: Achieved overall score of {0} in {1} {2}").format(
				self.overall_score, self.quarter, self.fiscal_year
			)
		})
		comment.insert(ignore_permissions=True)

@frappe.whitelist()
def get_historical_score(employee):
	reviews = frappe.get_all(
		"Performance Review",
		filters={"employee": employee, "docstatus": 1},
		fields=["overall_score"],
		order_by="creation desc",
		limit=1
	)
	if reviews:
		return reviews[0].overall_score
	return 0.0
