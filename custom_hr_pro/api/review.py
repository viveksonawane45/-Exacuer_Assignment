# Copyright (c) 2026, DeepMind Pair Programmer and contributors
# For license information, please see license.txt

import frappe

@frappe.whitelist()
def get_previous_review_score(employee):
	review = frappe.db.sql(
		"""
		SELECT
			overall_score
		FROM
			`tabPerformance Review`
		WHERE
			employee=%s AND docstatus=1
		ORDER BY
			creation DESC,
			modified DESC
		LIMIT 1
		""",
		employee,
		as_dict=True
	)
	return review
