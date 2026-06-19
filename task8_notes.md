# Task 8 — HTML Field Dashboard in Performance Review DocType

**Author:** Vivek Sonawane  
**Project:** Custom HR Pro (ERPNext/Frappe)  
**Task Type:** HTML Field + Client Script + Server Method + Live Dashboard + Historical Comparison

---

# Business Requirement

The Quarterly Performance Review DocType (created in Task 2) requires a visual KPI Dashboard panel.

The dashboard must display:

1. Each KPI with a progress bar
2. Overall Performance Score
3. Descriptive Label:
   - Excellent
   - Good
   - Average
   - Poor
4. Color Coding:
   - Green
   - Orange
   - Red
5. Previous Review Score Comparison
6. Live Updates while editing child table rows
7. No server call for live calculations
8. Only one server call for historical comparison

Use:

```text
HTML Field
+
Client Script
+
Inline CSS
```

---

# Objective

Build an interactive dashboard inside the Performance Review form.

---

# System Overview

```text
Quarterly Performance Review
        │
        ├── KPI Child Table
        │       ├── Goal
        │       ├── Target Value
        │       ├── Achieved Value
        │       └── Score
        │
        └── KPI Dashboard (HTML Field)
                │
                ├── Progress Bars
                ├── Overall Score
                ├── Rating Label
                └── Previous Score Comparison
```

---

# What is an HTML Field?

HTML Field:

```text
Field Type = HTML
```

Purpose:

Displays:

- HTML
- CSS
- JavaScript-generated UI
- Dashboards
- Cards
- Progress Bars
- Reports

HTML fields:

```text
Store No Data
```

They are:

```text
Read Only
```

and their content is generated dynamically.

---

# Creating the HTML Field

DocType:

```text
Quarterly Performance Review
```

Field:

| Property | Value |
|----------|--------|
| Label | KPI Dashboard |
| Fieldname | kpi_dashboard |
| Field Type | HTML |

---

# Final Layout

```text
Performance Review
│
├── Employee
├── Quarter
├── Year
├── Overall Score
│
├── KPI Child Table
│
└── KPI Dashboard
      │
      ├── KPI Progress Bars
      ├── Overall Score
      ├── Score Label
      └── Previous Review Comparison
```

---

# Dashboard Architecture

```text
KPI Rows
     ↓
Client Script
     ↓
Calculate Progress
     ↓
Calculate Score
     ↓
Generate HTML
     ↓
Set HTML Field
```

---

# Setting HTML Content

Use:

```javascript
frm.fields_dict
    .kpi_dashboard
    .$wrapper
    .html(html);
```

---

# Form Load Flow

```text
Open Form
      ↓
Load Employee
      ↓
Server Call
      ↓
Get Previous Review
      ↓
Store Previous Score
      ↓
Build Dashboard
```

---

# Live Update Flow

```text
User Changes Achieved Value
             ↓
Child Table Event Fires
             ↓
Recalculate Progress
             ↓
Recalculate Score
             ↓
Update HTML
```

No server call required.

---

# Child Table Events

Events:

```javascript
frappe.ui.form.on(
    "Performance KPI",
    {
        achieved_value(frm, cdt, cdn)
        {
            update_dashboard(frm);
        },

        score(frm, cdt, cdn)
        {
            update_dashboard(frm);
        },

        target_value(frm, cdt, cdn)
        {
            update_dashboard(frm);
        }
    }
);
```

---

# Is the Event Same for All Fields?

No.

Each field triggers:

```javascript
fieldname(frm, cdt, cdn)
```

Examples:

```javascript
score()
target_value()
achieved_value()
goal()
```

There is no universal:

```javascript
on_change()
```

event.

---

# Reading Child Table Rows

Use:

```javascript
frm.doc.kpi_table
```

Example:

```javascript
frm.doc.kpi_table.forEach(
    row => {

        console.log(
            row.goal
        );

        console.log(
            row.target_value
        );

        console.log(
            row.achieved_value
        );
    }
);
```

---

# Child Table Structure

```text
frm.doc.kpi_table
      │
      ├── goal
      ├── target_value
      ├── achieved_value
      └── score
```

---

# Calculate Progress

Formula:

```text
Achieved
---------
Target
× 100
```

---

# Example

```text
Target = 100
Achieved = 80

Progress = 80%
```

---

# Progress Bar Builder

```javascript
function get_progress_bar(
    percentage
)
{
    return `
        <div
            style="
                width:100%;
                background:#eee;
                border-radius:10px;
                height:20px;
            "
        >

            <div
                style="
                    width:${percentage}%;
                    background:#4caf50;
                    height:20px;
                    border-radius:10px;
                    text-align:center;
                    color:white;
                "
            >

                ${percentage.toFixed(0)}%

            </div>

        </div>
    `;
}
```

---

# Overall Score Calculation

Formula:

```text
Sum of KPI Scores
        ÷
Number of KPI Rows
```

---

# Example

```text
4
5
4
3

Average:

4.0
```

---

# Rating Labels

## Excellent

```text
Score ≥ 4.5
```

Color:

```text
Green
```

---

## Good

```text
Score ≥ 3
```

Color:

```text
Orange
```

---

## Average

```text
Score ≥ 2
```

Color:

```text
Orange
```

---

## Poor

```text
Score < 2
```

Color:

```text
Red
```

---

# Build Score Card

```javascript
function get_score_card(
    score
)
{
    let label =
        "Poor";

    let color =
        "#f44336";

    if (score >= 2)
    {
        label =
            "Average";

        color =
            "#ff9800";
    }

    if (score >= 3)
    {
        label =
            "Good";

        color =
            "#03a9f4";
    }

    if (score >= 4.5)
    {
        label =
            "Excellent";

        color =
            "#4caf50";
    }

    return `
        <div
            style="
                background:${color};
                padding:20px;
                border-radius:12px;
                color:white;
                text-align:center;
            "
        >

            <h1>${score.toFixed(2)}</h1>

            <h3>${label}</h3>

        </div>
    `;
}
```

---

# Previous Review Comparison

Requirement:

Only one server call.

---

# Form Load

```javascript
frappe.ui.form.on(
    "Quarterly Performance Review",
    {
        onload(frm)
        {
            get_previous_score(
                frm
            );
        }
    }
);
```

---

# Server Method

```python
@frappe.whitelist()
def get_previous_review_score(
    employee
):

    review = frappe.db.sql(
        """
        SELECT
            overall_score
        FROM
            `tabQuarterly Performance Review`
        WHERE
            employee=%s
        ORDER BY
            review_year DESC,
            modified DESC
        LIMIT 1
        """,
        employee,
        as_dict=True
    )

    return review
```

---

# Client Call

```javascript
frappe.call({
    method:
    "custom_hr_pro.api.review.get_previous_review_score",

    args:
    {
        employee:
        frm.doc.employee
    },

    callback(r)
    {
        frm.previous_score =
            r.message;
    }
});
```

---

# Comparison Section

```text
Current Score
      ↓
4.2

Previous Score
      ↓
3.5

Difference
      ↓
+0.7
```

---

# Dashboard Layout

```text
KPI Dashboard
│
├── Score Card
├── Previous Review Card
│
└── KPI Rows
        │
        ├── Goal
        ├── Progress Bar
        └── Percentage
```

---

# Complete Flow

```text
Form Loads
      ↓
Server Call
      ↓
Previous Score
      ↓
Store Result
      ↓
User Edits KPI
      ↓
Child Event Fires
      ↓
Calculate Progress
      ↓
Calculate Score
      ↓
Generate HTML
      ↓
Render Dashboard
```

---

# Client vs Server Calculations

## Client Side

Use when:

- Instant calculations
- Form data already available
- Progress bars
- Totals
- Averages
- UI rendering

Benefits:

```text
Fast
No Network Calls
Better UX
```

---

## Server Side

Use when:

- Database queries required
- Historical records
- Security checks
- Permission checks
- Large datasets

Benefits:

```text
Secure
Reliable
Centralized
```

---

# Automated Tests

## Test 1

Dashboard renders.

Expected:

```text
HTML generated.
```

---

## Test 2

Progress bar updates.

Expected:

```text
Percentage changes instantly.
```

---

## Test 3

Previous score loads.

Expected:

```text
Previous score returned.
```

---

# Suggested Screenshots

```text
screenshots/
├── 01_html_field.png
├── 02_dashboard.png
├── 03_progress_bars.png
├── 04_score_card.png
├── 05_previous_comparison.png
├── 06_live_update.gif
```

---

# Add Screenshots

```markdown
![Dashboard](screenshots/02_dashboard.png)

![Progress Bars](screenshots/03_progress_bars.png)

![Comparison](screenshots/05_previous_comparison.png)
```

---

# Folder Structure

```text
custom_hr_pro/
│
├── task8_notes.md
│
├── doctype/
│      └── quarterly_performance_review/
│
├── public/
│      └── js/
│              └── quarterly_performance_review.js
│
├── api/
│      └── review.py
│
├── fixtures/
│      └── custom_field.json
│
├── TASK8_RESEARCH.md
└── TASK8_NOTES.md
```

---

# End-to-End Architecture

```text
Performance KPI Rows
          ↓
Child Table Events
          ↓
Client Calculation
          ↓
Progress Bars
          ↓
Score Card
          ↓
Previous Score Comparison
          ↓
Live Dashboard
```

This implementation creates an interactive KPI Dashboard entirely inside the Frappe form using an HTML field, inline CSS, client-side calculations, and a single server call for historical comparison, resulting in a fast and responsive user experience.