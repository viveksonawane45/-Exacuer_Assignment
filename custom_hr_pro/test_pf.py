import frappe

def run():
    pf = frappe.get_doc("Print Format", "Premium Two-Column Salary Slip")
    print("Print Format:", pf.name)
    print("Module:", pf.module)
    print("Is Standard:", pf.is_standard)
    
    mod = frappe.get_doc("Module Def", pf.module)
    print("Module Def App Name:", mod.app_name)
    print("Is Developer Mode on site?:", frappe.conf.developer_mode)
