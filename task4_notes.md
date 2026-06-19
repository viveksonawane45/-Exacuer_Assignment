# Task 4 — Professional Salary Slip Print Format using Jinja HTML

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** Custom Print Format + Jinja + HTML/CSS + Fixtures + PDF Export

---

# Business Requirement

Employees require a professional printable salary slip instead of the default ERPNext system-generated format.

The payslip should:

- Look professional
- Be suitable for official records
- Clearly display earnings and deductions
- Display net pay prominently
- Include payment method and bank details
- Include confidentiality notice
- Generate correctly in PDF format

The print format should be created using:

```text
Jinja + HTML + CSS
```

and exported as a Fixture.

---

# Objective

Create a custom Salary Slip print format that resembles an official company payslip.

---

# Existing ERPNext Salary Slip Print Formats

Navigation:

```text
Home
→ Payroll
→ Salary Slip
→ Print
→ Menu
→ Customize
→ Print Format
```

ERPNext provides:

### Standard Print Format

Features:

- Employee Information
- Earnings
- Deductions
- Net Pay

Limitations:

- Plain table layout
- Not suitable for official HR records
- Poor visual hierarchy
- No confidentiality notice
- No payment information section

---

# Print Format Requirements

The final payslip should contain:

```text
Company Header
        │
        ├── Employee Information
        ├── Payroll Information
        ├── Earnings
        ├── Deductions
        ├── Gross Pay
        ├── Net Pay
        ├── Payment Details
        └── Confidentiality Notice
```

---

# Salary Slip DocType Structure

```text
Salary Slip
│
├── Employee Details
│
├── Earnings
│     └── Salary Detail Child Table
│
├── Deductions
│     └── Salary Detail Child Table
│
├── Gross Pay
│
├── Total Deduction
│
└── Net Pay
```

---

# Database Tables

```text
tabSalary Slip
tabSalary Detail
tabEmployee
tabCompany
```

---

# Important Jinja Variables

## Main Document

```jinja
{{ doc.name }}
{{ doc.employee }}
{{ doc.employee_name }}
{{ doc.company }}
{{ doc.start_date }}
{{ doc.end_date }}
{{ doc.payment_days }}
{{ doc.gross_pay }}
{{ doc.total_deduction }}
{{ doc.net_pay }}
```

---

## Employee Information

```jinja
{{ doc.designation }}
{{ doc.department }}
{{ doc.branch }}
{{ doc.company }}
```

---

## Payment Information

```jinja
{{ doc.mode_of_payment }}
{{ doc.bank_name }}
{{ doc.bank_account_no }}
```

---

# Salary Detail Child Table

Both:

```text
Earnings
```

and

```text
Deductions
```

come from:

```text
tabSalary Detail
```

and are accessible as:

```jinja
doc.earnings
doc.deductions
```

---

# Iterating Earnings

```jinja
{% for row in doc.earnings %}

<tr>
    <td>{{ row.salary_component }}</td>
    <td style="text-align:right;">
        {{ row.amount }}
    </td>
</tr>

{% endfor %}
```

---

# Iterating Deductions

```jinja
{% for row in doc.deductions %}

<tr>
    <td>{{ row.salary_component }}</td>
    <td style="text-align:right;">
        {{ row.amount }}
    </td>
</tr>

{% endfor %}
```

---

# Print Format Layout

```text
--------------------------------------------------
                 COMPANY HEADER
--------------------------------------------------

Employee Information      Payroll Information

--------------------------------------------------
      Earnings      |      Deductions
--------------------------------------------------

--------------------------------------------------
Gross Pay
Total Deductions
Net Pay
--------------------------------------------------

Payment Details

Confidentiality Notice
--------------------------------------------------
```

---

# Layout Design

## Section 1

### Company Header

Contains:

- Company Logo
- Company Name
- Company Address
- Contact Information

---

# Jinja

```jinja
<h2>{{ doc.company }}</h2>
```

---

# Section 2

## Employee Information

```html
<table width="100%">
<tr>

<td width="50%">

Employee :
{{ doc.employee_name }}

Department :
{{ doc.department }}

Designation :
{{ doc.designation }}

</td>

<td width="50%">

Salary Slip :
{{ doc.name }}

Period :
{{ doc.start_date }}
-
{{ doc.end_date }}

Payment Days :
{{ doc.payment_days }}

</td>

</tr>
</table>
```

---

# Section 3

## Earnings and Deductions

Layout:

```text
------------------------------------
Earnings | Deductions
------------------------------------
```

---

# HTML Structure

```html
<table width="100%">

<tr>

<th width="50%">
Earnings
</th>

<th width="50%">
Deductions
</th>

</tr>

<tr>

<td>

<table width="100%">
......
</table>

</td>

<td>

<table width="100%">
......
</table>

</td>

</tr>

</table>
```

---

# Section 4

## Salary Summary

```html
<table width="100%">

<tr>

<td>
Gross Pay
</td>

<td align="right">
{{ doc.gross_pay }}
</td>

</tr>

<tr>

<td>
Total Deductions
</td>

<td align="right">
{{ doc.total_deduction }}
</td>

</tr>

<tr>

<td>

<b>Net Pay</b>

</td>

<td align="right">

<b>

{{ doc.net_pay }}

</b>

</td>

</tr>

</table>
```

---

# Highlight Net Pay

```html
<div
style="
background:#f0f8ff;
padding:15px;
border:2px solid #007bff;
font-size:20px;
font-weight:bold;
text-align:center;
">

Net Pay :
{{ doc.net_pay }}

</div>
```

---

# Section 5

## Payment Details

```html
<table width="100%">

<tr>

<td>

Payment Mode :

{{ doc.mode_of_payment }}

</td>

</tr>

<tr>

<td>

Bank :

{{ doc.bank_name }}

</td>

</tr>

<tr>

<td>

Account Number :

{{ doc.bank_account_no }}

</td>

</tr>

</table>
```

---

# Section 6

## Confidentiality Notice

```html
<div
style="
margin-top:20px;
font-size:11px;
border-top:1px solid #ccc;
padding-top:10px;
">

This salary slip is confidential and intended solely
for the employee named above. Unauthorized disclosure,
copying, or distribution is prohibited.

</div>
```

---

# Currency Formatting

Use:

```jinja
{{ frappe.format_value(
    row.amount,
    {
        "fieldtype":"Currency"
    }
)}}
```

or

```jinja
{{ frappe.utils.fmt_money(
    row.amount,
    currency=doc.currency
)}}
```

Benefits:

- Currency Symbol
- Decimal Places
- Localization

---

# Two Column Alignment for Printing

Recommended:

```html
<table width="100%">
```

Avoid:

```html
display:flex
```

because:

```text
wkhtmltopdf
may render flex layouts inconsistently.
```

---

# Why Tables?

Benefits:

- Predictable PDF rendering
- Better page breaks
- Works correctly with wkhtmltopdf
- Better alignment

---

# Print Format Architecture

```text
Company Header
       ↓
Employee Details
       ↓
Payroll Information
       ↓
Earnings Table
       ↓
Deductions Table
       ↓
Salary Summary
       ↓
Payment Details
       ↓
Confidentiality Notice
```

---

# Export as Fixture

## hooks.py

```python
fixtures = [
    "Print Format"
]
```

---

# Export Command

```bash
bench --site site1.local export-fixtures
```

---

# Fixture Structure

```text
custom_hr_pro/
│
├── fixtures/
│      └── print_format.json
```

---

# PDF Sample Folder

```text
samples/
│
└── salary_slip_sample.pdf
```

---

# Suggested Screenshots

```text
screenshots/
├── 01_standard_print.png
├── 02_custom_layout.png
├── 03_earnings_deductions.png
├── 04_net_pay_highlight.png
├── 05_payment_details.png
├── 06_pdf_output.png
```

---

# Add Screenshots

```markdown
![Custom Layout](screenshots/02_custom_layout.png)

![Net Pay](screenshots/04_net_pay_highlight.png)

![PDF Output](screenshots/06_pdf_output.png)
```

---

# Folder Structure

```text
custom_hr_pro/
│
├── fixtures/
│      └── print_format.json
│
├── samples/
│      └── salary_slip_sample.pdf
│
├── TASK4_RESEARCH.md
├── TASK4_NOTES.md
└── task4_notes.md
```

---

# End-to-End Flow

```text
Study Existing Print Formats
            ↓
Study Jinja Variables
            ↓
Design Payslip Layout
            ↓
Create HTML + CSS
            ↓
Iterate Earnings
            ↓
Iterate Deductions
            ↓
Highlight Net Pay
            ↓
Add Payment Details
            ↓
Add Confidentiality Notice
            ↓
Export Fixture
            ↓
Generate PDF
```

This implementation produces an official, professional, and printable Salary Slip that is suitable for company records, employee communication, and PDF generation while remaining completely upgrade-safe through Fixtures.