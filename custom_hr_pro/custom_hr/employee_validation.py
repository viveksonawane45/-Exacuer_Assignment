import frappe
from frappe.utils import date_diff, today

def validate_privacy_agreement(doc, method):
	if doc.date_of_joining:
		days_of_employment = date_diff(today(), doc.date_of_joining)
		if days_of_employment > 30 and not doc.custom_data_privacy_agreement_signed:
			frappe.msgprint(
				msg="Warning: Employee has completed more than 30 days of employment but has not signed the Data Privacy Agreement.",
				title="Privacy Agreement Warning",
				indicator="orange"
			)
