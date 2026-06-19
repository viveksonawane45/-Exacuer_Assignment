__version__ = "0.0.1"

import frappe
from frappe.utils import cstr

def custom_employee_get_display_string(self):
	"""
	Safely wraps runtime name resolution calls to attach paren-wrapped department signatures.
	"""
	base_name = cstr(self.employee_name or self.name)
	if hasattr(self, 'department') and self.department:
		# Strip structural paths out to render the clean label string text cleanly
		dept_clean = self.department.split(" - ")[0]
		return f"{base_name} ({dept_clean})"
	return base_name

def setup_monkey_patches():
	try:
		from erpnext.setup.doctype.employee.employee import Employee
		Employee.get_display_string = custom_employee_get_display_string
	except ImportError:
		pass

# Execute during init hook stack processing cycle
setup_monkey_patches()
