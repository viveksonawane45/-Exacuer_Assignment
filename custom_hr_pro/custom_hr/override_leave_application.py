import frappe
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication

class CustomLeaveApplication(LeaveApplication):
	def validate(self):
		super().validate()
		self.enforce_long_leave_reason()

	def on_submit(self):
		super().on_submit()
		self.notify_manager_on_submission()

	def enforce_long_leave_reason(self):
		if self.total_leave_days > 5 and not self.reason:
			frappe.throw("Leave applications spanning more than 5 consecutive working days strictly require an explicit textual reason statement prior to validation submission.")

	def notify_manager_on_submission(self):
		if self.leave_approver:
			user_id = frappe.db.get_value("Employee", {"name": self.leave_approver}, "user_id") or self.leave_approver
			frappe.get_doc({
				"doctype": "Notification Log",
				"for_user": user_id,
				"subject": f"Leave Application Submitted for Approval: {self.employee_name} ({self.total_leave_days} Days)",
				"type": "Alert",
				"document_type": "Leave Application",
				"document_name": self.name
			}).insert(ignore_permissions=True)
