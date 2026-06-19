# Task 5 — Monkey Patching in Frappe/ERPNext

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** Runtime Monkey Patching + Employee Display Name Customization + Automated Tests

---

# Business Requirement

Whenever an Employee's full name is displayed anywhere in the system, it should also display their department in parentheses.

Example:

```text
Before:
Priya Mehta

After:
Priya Mehta (Engineering)
```

Requirements:

- Must work without modifying Frappe source code.
- Must work without modifying ERPNext source code.
- Handle all edge cases.
- Never crash the application.
- Implement using Monkey Patching.

---

# Objective

Override the Employee display name generation at runtime so that:

```text
Employee Name
+
Department
=
Enhanced Display Name
```

Example:

```text
Rahul Sharma (IT)
Priya Mehta (Engineering)
Anita Patil (Finance)
```

If department is empty:

```text
Rahul Sharma
```

---

# What is Monkey Patching?

Monkey Patching is:

```text
Replacing or modifying a class,
function, or method at runtime
without modifying its original source code.
```

Python allows:

```python
module.function = custom_function
```

during application startup.

---

# Simple Example

Original:

```python
def greet():
    return "Hello"
```

Patch:

```python
def custom_greet():
    return "Hello Vivek"

greet = custom_greet
```

Result:

```text
Hello Vivek
```

without modifying the original function.

---

# Why Use Monkey Patching?

Advantages:

- No changes to ERPNext source code
- Upgrade-safe
- Easy rollback
- Isolated inside custom app

---

# System Overview

```text
Employee Display Request
          ↓
Original Function
          ↓
Monkey Patch
          ↓
Append Department
          ↓
Return Modified Name
```

---

# Research

Potential functions:

## Frappe

```python
frappe.utils.user.get_fullname()
```

Purpose:

Returns User Full Name.

Limitation:

Works for User records, not Employee names.

---

## ERPNext HR

Employee display names are generated from:

```text
Employee.employee_name
```

and various helper methods.

Many HR reports and Link Fields use:

```python
frappe.get_cached_value()
```

to retrieve employee names.

---

# Existing ERPNext Behavior

Current:

```text
EMP-0001
Rahul Sharma
```

Desired:

```text
EMP-0001
Rahul Sharma (IT)
```

---

# Final Architecture

```text
System Request
      ↓
Employee Name
      ↓
Monkey Patch
      ↓
Fetch Department
      ↓
Append Department
      ↓
Return Display Name
```

---

# Why Not Modify ERPNext Source?

Never:

```python
apps/erpnext/erpnext/setup/doctype/employee/employee.py
```

because:

- Upgrades overwrite changes
- Difficult maintenance
- Merge conflicts
- Violates Frappe best practices

---

# Patch Location

Recommended:

```text
custom_hr_pro/
│
├── __init__.py
├── patches/
│      └── employee_display.py
```

---

# Runtime Flow

```text
Bench Start
      ↓
Custom App Loaded
      ↓
__init__.py Executes
      ↓
Patch Registered
      ↓
All Requests Use Patched Function
```

---

# employee_display.py

```python
import frappe


def get_employee_display_name(employee):

    if not employee:
        return ""

    employee_doc = frappe.get_cached_value(
        "Employee",
        employee,
        [
            "employee_name",
            "department"
        ],
        as_dict=True
    )

    if not employee_doc:
        return employee

    name = employee_doc.employee_name or employee

    department = employee_doc.department

    if department:
        return f"{name} ({department})"

    return name
```

---

# __init__.py

```python
import frappe
import custom_hr_pro.patches.employee_display as patch


def apply_monkey_patch():

    try:
        frappe.get_employee_display_name = (
            patch.get_employee_display_name
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Employee Display Patch Failed"
        )


apply_monkey_patch()
```

---

# Edge Cases

## Employee does not exist

Input:

```text
EMP-9999
```

Output:

```text
EMP-9999
```

---

## Department Missing

Input:

```text
Rahul Sharma
Department = None
```

Output:

```text
Rahul Sharma
```

---

## Employee Name Missing

Input:

```text
employee_name = None
```

Output:

```text
EMP-0001
```

---

# Error Handling

Never:

```python
raise Exception()
```

Always:

```python
frappe.log_error()
```

because:

```text
Patch failure should never crash ERPNext.
```

---

# Why Direct Imports Bypass Patches?

Example:

## Module Level Import

```python
from employee import get_name
```

creates:

```text
Local Reference
```

Later:

```python
employee.get_name = custom_function
```

does not update:

```text
Local Reference
```

because:

```text
Imported Function
≠
Module Function
```

---

# Diagram

```text
Module A
      ↓
from module import func
      ↓
Local Copy Created
      ↓
Patch Module.func
      ↓
Local Copy Unchanged
```

---

# After Every Bench Update Verify

## Verification Checklist

### Bench Migration

```bash
bench migrate
```

---

### Restart

```bash
bench restart
```

---

### Test Patch

```bash
bench console
```

```python
frappe.get_employee_display_name(
    "EMP-0001"
)
```

Expected:

```text
Rahul Sharma (IT)
```

---

### Check Logs

```bash
bench --site site1.local logs
```

---

# Alternatives Considered

## Option 1

Custom Script

Rejected:

```text
Client-side only.
```

---

## Option 2

Property Setter

Rejected:

```text
Cannot modify Python behavior.
```

---

## Option 3

Override Doctype Class

Rejected:

```text
Changes Employee logic,
not display function globally.
```

---

## Option 4

Monkey Patch

Selected:

```text
Global
Upgrade-safe
Minimal Code
No Core Changes
```

---

# Automated Tests

File:

```text
test_employee_display_patch.py
```

---

# Test 1

Department Exists.

Expected:

```text
Rahul Sharma (IT)
```

---

# Test 2

Department Missing.

Expected:

```text
Rahul Sharma
```

---

# Test 3

Employee Missing.

Expected:

```text
EMP-9999
```

---

# Test Flow

```text
Create Employee
       ↓
Apply Patch
       ↓
Call Display Function
       ↓
Verify Output
```

---

# Sample Tests

```python
class TestEmployeePatch(FrappeTestCase):

    def test_department_appended(self):
        pass

    def test_department_missing(self):
        pass

    def test_employee_missing(self):
        pass
```

---

# Suggested Screenshots

```text
screenshots/
├── 01_original_display.png
├── 02_monkey_patch_code.png
├── 03_patched_output.png
├── 04_bench_console_test.png
├── 05_test_results.png
```

---

# Add Screenshots

```markdown
![Original Display](screenshots/01_original_display.png)

![Monkey Patch Code](screenshots/02_monkey_patch_code.png)

![Patched Output](screenshots/03_patched_output.png)
```

---

# Folder Structure

```text
custom_hr_pro/
│
├── task5_notes.md
│
├── __init__.py
│
├── patches/
│      └── employee_display.py
│
├── tests/
│      └── test_employee_display_patch.py
│
├── TASK5_RESEARCH.md
└── TASK5_NOTES.md
```

---

# End-to-End Flow

```text
Bench Starts
      ↓
Custom App Loads
      ↓
Monkey Patch Registered
      ↓
Employee Name Requested
      ↓
Fetch Department
      ↓
Append Department
      ↓
Return Modified Display Name
      ↓
Display:
Rahul Sharma (IT)
```

---

# Final Output Examples

```text
Priya Mehta (Engineering)
Rahul Sharma (IT)
Amit Kulkarni (Finance)
Sneha Patil (HR)
```

If Department is missing:

```text
Priya Mehta
```

This implementation achieves a global Employee display enhancement using runtime Monkey Patching while remaining upgrade-safe, isolated from ERPNext core code, and resilient to failures.