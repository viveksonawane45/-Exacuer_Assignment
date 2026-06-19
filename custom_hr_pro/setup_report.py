import frappe

def run():
    print("Creating Script Report: Attendance Summary")
    report_name = "Attendance Summary"
    if frappe.db.exists("Report", report_name):
        frappe.delete_doc("Report", report_name)
        print("Deleted existing report")
        
    r = frappe.get_doc({
        "doctype": "Report",
        "report_name": report_name,
        "ref_doctype": "Employee",
        "report_type": "Script Report",
        "module": "Custom HR",
        "is_standard": "Yes"
    })
    r.insert(ignore_permissions=True)
    print("Created Report")
