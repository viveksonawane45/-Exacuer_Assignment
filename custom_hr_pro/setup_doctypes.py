import frappe

def run():
    print("Initializing DocType creation inside custom_hr_pro...")

    # 1. Ensure Module Def exists
    if not frappe.db.exists("Module Def", "Custom HR"):
        m = frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Custom HR",
            "app_name": "custom_hr_pro"
        })
        m.insert(ignore_permissions=True)
        print("Created Module Def: Custom HR")
    else:
        print("Module Def: Custom HR already exists")

    # 2. Define Child DocType: Performance Review KPI
    kpi_name = "Performance Review KPI"
    if frappe.db.exists("DocType", kpi_name):
        frappe.delete_doc("DocType", kpi_name)
        print("Deleted existing Performance Review KPI DocType")

    kpi_dt = frappe.get_doc({
        "doctype": "DocType",
        "name": kpi_name,
        "module": "Custom HR",
        "custom": 0,
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {
                "fieldname": "goal",
                "label": "Goal",
                "fieldtype": "Data",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "target_value",
                "label": "Target Value",
                "fieldtype": "Float",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "achieved_value",
                "label": "Achieved Value",
                "fieldtype": "Float",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "score",
                "label": "Score",
                "fieldtype": "Select",
                "options": "1\n2\n3\n4\n5",
                "reqd": 1,
                "in_list_view": 1
            }
        ]
    })
    kpi_dt.insert(ignore_permissions=True)
    print("Created DocType: Performance Review KPI")

    # 3. Define Parent DocType: Performance Review
    parent_name = "Performance Review"
    if frappe.db.exists("DocType", parent_name):
        frappe.delete_doc("DocType", parent_name)
        print("Deleted existing Performance Review DocType")

    parent_dt = frappe.get_doc({
        "doctype": "DocType",
        "name": parent_name,
        "module": "Custom HR",
        "custom": 0,
        "is_submittable": 1,
        "naming_rule": "Expression",
        "autoname": "format:PR-.YYYY.-.#####",
        "fields": [
            {
                "fieldname": "employee",
                "label": "Employee",
                "fieldtype": "Link",
                "options": "Employee",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "employee_name",
                "label": "Employee Name",
                "fieldtype": "Data",
                "read_only": 1,
                "fetch_from": "employee.employee_name",
                "in_list_view": 1
            },
            {
                "fieldname": "manager_name",
                "label": "Manager Name",
                "fieldtype": "Data",
                "read_only": 1
            },
            {
                "fieldname": "department",
                "label": "Department",
                "fieldtype": "Link",
                "options": "Department",
                "read_only": 1,
                "fetch_from": "employee.department"
            },
            {
                "fieldname": "fiscal_year",
                "label": "Fiscal Year",
                "fieldtype": "Link",
                "options": "Fiscal Year",
                "reqd": 1
            },
            {
                "fieldname": "quarter",
                "label": "Quarter",
                "fieldtype": "Select",
                "options": "Q1\nQ2\nQ3\nQ4",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "overall_score",
                "label": "Overall Score",
                "fieldtype": "Float",
                "read_only": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "live_score_badge",
                "label": "Live Score Badge",
                "fieldtype": "HTML"
            },
            {
                "fieldname": "kpis",
                "label": "KPIs",
                "fieldtype": "Table",
                "options": "Performance Review KPI"
            },
            {
                "fieldname": "dashboard_html_view",
                "label": "Dashboard HTML View",
                "fieldtype": "HTML"
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1
            },
            {
                "role": "HR Manager",
                "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1
            },
            {
                "role": "HR User",
                "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1
            }
        ]
    })
    parent_dt.insert(ignore_permissions=True)
    print("Created DocType: Performance Review")

    # 4. Define Custom Fields on Employee DocType
    custom_fields = [
        {
            "dt": "Employee",
            "fieldname": "custom_emergency_contact_name",
            "label": "Emergency Contact Name",
            "fieldtype": "Data",
            "insert_after": "emergency_phone_number"
        },
        {
            "dt": "Employee",
            "fieldname": "custom_t_shirt_size",
            "label": "T-Shirt Size",
            "fieldtype": "Select",
            "options": "XS\nS\nM\nL\nXL\nXXL\nXXXL",
            "insert_after": "blood_group"
        },
        {
            "dt": "Employee",
            "fieldname": "custom_data_privacy_agreement_signed",
            "label": "Data Privacy Agreement Signed",
            "fieldtype": "Check",
            "insert_after": "status"
        },
        {
            "dt": "Employee",
            "fieldname": "custom_privacy_agreement_signed_date",
            "label": "Privacy Agreement Signed Date",
            "fieldtype": "Date",
            "insert_after": "custom_data_privacy_agreement_signed",
            "depends_on": "eval:doc.custom_data_privacy_agreement_signed==1"
        }
    ]
    for cf in custom_fields:
        cf_name = f"{cf['dt']}-{cf['fieldname']}"
        if not frappe.db.exists("Custom Field", cf_name):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": cf["dt"],
                "fieldname": cf["fieldname"],
                "label": cf["label"],
                "fieldtype": cf["fieldtype"],
                "options": cf.get("options"),
                "insert_after": cf["insert_after"],
                "depends_on": cf.get("depends_on")
            }).insert(ignore_permissions=True)
            print(f"Created Custom Field: {cf_name}")
        else:
            # Update existing custom field if needed
            doc = frappe.get_doc("Custom Field", cf_name)
            doc.update({
                "label": cf["label"],
                "fieldtype": cf["fieldtype"],
                "options": cf.get("options"),
                "insert_after": cf["insert_after"],
                "depends_on": cf.get("depends_on")
            })
            doc.save(ignore_permissions=True)
            print(f"Updated Custom Field: {cf_name}")

