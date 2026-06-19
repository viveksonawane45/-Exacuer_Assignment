# Task 1 — Add Fields to an Existing DocType + Fixtures

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** Employee DocType Customization + Fixtures + Validation Hook

---

# Business Requirement

The HR team requires additional information on the Employee DocType:

1. Emergency Contact Name
2. Emergency Contact Phone Number
3. Blood Group
4. T-Shirt Size
5. Data Privacy Agreement Signed
6. Date of Data Privacy Agreement Signature

Requirements:

- Never modify ERPNext source files.
- Use Customize Form only.
- Add only fields that do not already exist.
- Export customizations as Fixtures.
- Show a warning if an employee has not signed the privacy agreement after 30 days of joining.

---

# Objective

Study the Employee DocType and determine which fields already exist and which require customization.

---

# Standard Employee Structure

```text
Employee
│
├── Basic Information
├── Employment Details
├── Personal Details
├── Contact Details
├── Attendance Details
├── Payroll Details
└── Exit Information
```

---

# Existing Fields Research

## Personal Details

Available Fields:

- Gender
- Date of Birth
- Marital Status
- Nationality
- Blood Group
- Passport Details

### Finding

```text
Blood Group already exists.
```

No customization required.

---

## Contact Details

Available Fields:

- Personal Email
- Company Email
- Cell Number
- Emergency Phone Number
- Current Address
- Permanent Address

### Finding

```text
Emergency Phone Number already exists.
Emergency Contact Name is missing.
```

---

# Requirement Analysis

| Requirement | Exists | Action |
|-------------|---------|---------|
| Emergency Contact Name | ❌ | Create |
| Emergency Phone Number | ✅ | Reuse |
| Blood Group | ✅ | Reuse |
| T-Shirt Size | ❌ | Create |
| Data Privacy Agreement Signed | ❌ | Create |
| Privacy Agreement Signed Date | ❌ | Create |

---

# Custom Field Design

## Section: Emergency Contact Information

### Field 1

| Property | Value |
|----------|--------|
| Label | Emergency Contact Name |
| Fieldname | custom_emergency_contact_name |
| Type | Data |

Purpose:

Stores the emergency contact person's name.

---

## Section: Employee Merchandise

### Field 2

| Property | Value |
|----------|--------|
| Label | T-Shirt Size |
| Fieldname | custom_t_shirt_size |
| Type | Select |

Options:

```text
XS
S
M
L
XL
XXL
XXXL
```

Purpose:

Stores company merchandise size.

---

## Section: Data Privacy Agreement

### Field 3

| Property | Value |
|----------|--------|
| Label | Data Privacy Agreement Signed |
| Fieldname | custom_data_privacy_agreement_signed |
| Type | Check |

Purpose:

Stores whether the employee signed the agreement.

---

### Field 4

| Property | Value |
|----------|--------|
| Label | Privacy Agreement Signed Date |
| Fieldname | custom_privacy_agreement_signed_date |
| Type | Date |

Depends On:

```javascript
eval:doc.custom_data_privacy_agreement_signed==1
```

Purpose:

Display date only when agreement is signed.

---

# Final Layout

```text
Employee
│
├── Contact Information
│      ├── Emergency Phone Number
│      └── Emergency Contact Name
│
├── Personal Information
│      └── Blood Group
│
├── Merchandise Information
│      └── T-Shirt Size
│
└── Data Privacy Agreement
       ├── Agreement Signed
       └── Agreement Signed Date
```

---

# Validation Requirement

Business Rule:

If:

```text
Current Date
-
Date of Joining
>
30 Days

AND

Agreement Signed = False
```

Then:

```text
Show Warning
Allow Save
```

---

# Doc Event Flow

```text
Employee Save
      ↓
Validate
      ↓
Joined > 30 Days?
      ↓
Agreement Signed?
      ↓
No
      ↓
Show Warning
      ↓
Continue Save
```

---

# hooks.py

```python
doc_events = {
    "Employee": {
        "validate":
        "custom_hr_pro.employee_customization.validate_privacy_agreement"
    }
}
```

---

# employee_customization.py

```python
import frappe
from frappe.utils import nowdate, date_diff


def validate_privacy_agreement(doc, method):

    if (
        doc.date_of_joining
        and not doc.custom_data_privacy_agreement_signed
        and date_diff(nowdate(), doc.date_of_joining) > 30
    ):

        frappe.msgprint(
            "Warning: Employee has completed more than 30 days of employment and has not signed the Data Privacy Agreement.",
            indicator="orange",
            title="Privacy Agreement Pending"
        )
```

---

# Why Use Customize Form?

## Upgrade Safety

Core JSON files may be overwritten during upgrades.

---

## Maintainability

Customizations remain separate from ERPNext source code.

---

## Version Control

Changes can be exported as Fixtures and tracked in Git.

---

# Fixtures

## hooks.py

```python
fixtures = [
    "Custom Field",
    "Property Setter"
]
```

---

# Export Fixtures

```bash
bench --site site1.local export-fixtures
```

Generated:

```text
custom_hr_pro/
│
├── fixtures/
│      ├── custom_field.json
│      └── property_setter.json
```

---

# Deploy Fixtures

```bash
bench --site site1.local migrate
```

or

```bash
bench migrate
```

---

# frappe.msgprint() vs frappe.throw()

| Feature | frappe.msgprint() | frappe.throw() |
|---------|-------------------|----------------|
| Warning | ✅ | ❌ |
| Error | ❌ | ✅ |
| Stops Save | ❌ | ✅ |
| Raises Exception | ❌ | ✅ |
| Rollback Transaction | ❌ | ✅ |

---

# Screenshot Folder

```text
screenshots/
├── 01_employee_standard_fields.png
├── 02_contact_details.png
├── 03_customize_form.png
├── 04_custom_fields.png
├── 05_privacy_section.png
├── 06_fixture_files.png
```

---

# Add Screenshots

```markdown
![Employee Fields](screenshots/01_employee_standard_fields.png)

![Customize Form](screenshots/03_customize_form.png)

![Privacy Section](screenshots/05_privacy_section.png)
```

---

# End-to-End Flow

```text
Study Employee
        ↓
Identify Missing Fields
        ↓
Create Custom Fields
        ↓
Add Conditional Visibility
        ↓
Add Validation Hook
        ↓
Export Fixtures
        ↓
Commit to Git
        ↓
Deploy with bench migrate
```

---

# Folder Structure

```text
custom_hr_pro/
│
├── task1_notes.md
├── fixtures/
│      ├── custom_field.json
│      └── property_setter.json
├── hooks.py
└── employee_customization.py
```