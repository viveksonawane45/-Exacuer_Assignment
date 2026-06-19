import frappe

def before_tests():
	print("Clearing conflicting test fiscal years before starting test suite...")
	frappe.db.delete("Fiscal Year", {"name": ["in", ["_Test Fiscal Year 2026", "2026-2027"]]})
	frappe.db.commit()

	# Disable mandatory flag on custom fields in Quotation to allow standard test records to load
	print("Disabling mandatory flag on custom_resource_matrix in Quotation...")
	frappe.db.sql("""
		UPDATE `tabCustom Field` 
		SET reqd = 0 
		WHERE dt = 'Quotation' AND fieldname = 'custom_resource_matrix'
	""")
	frappe.db.commit()
	frappe.clear_cache(doctype="Quotation")

	# Create temporary Payment Gateway DocType to bypass missing payments app dependency in standard tests
	if not frappe.db.exists("DocType", "Payment Gateway"):
		print("Mocking Payment Gateway DocType for tests...")
		frappe.get_doc({
			"doctype": "DocType",
			"name": "Payment Gateway",
			"module": "Core",
			"custom": 1,
			"fields": [
				{"fieldname": "gateway_name", "label": "Gateway Name", "fieldtype": "Data"}
			]
		}).insert(ignore_permissions=True)
		frappe.db.commit()
