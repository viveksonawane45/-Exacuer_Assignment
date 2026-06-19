import frappe

def run():
    print("Creating Print Format: Premium Two-Column Salary Slip")
    name = "Premium Two-Column Salary Slip"
    if frappe.db.exists("Print Format", name):
        frappe.delete_doc("Print Format", name)
        print("Deleted existing print format")
        
    html_content = """<div class="salary-slip-container" style="font-family: 'Helvetica Neue', Arial, sans-serif; padding: 20px; color: #333;">
    <table style="width: 100%; border-bottom: 2px solid #2C3E50; padding-bottom: 15px; margin-bottom: 20px;">
        <tr>
            <td style="width: 50%; vertical-align: top;">
                <h2 style="margin: 0; color: #2C3E50;">{{ doc.company }}</h2>
                <p style="margin: 4px 0; font-size: 12px; color: #7F8C8D;">Official Salary Statement / Payslip</p>
            </td>
            <td style="width: 50%; text-align: right; vertical-align: top; font-size: 13px;">
                <strong>Employee ID:</strong> {{ doc.employee }}<br>
                <strong>Name:</strong> {{ doc.employee_name }}<br>
                <strong>Period:</strong> {{ doc.start_date }} to {{ doc.end_date }}
            </td>
        </tr>
    </table>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
        <thead>
            <tr style="background-color: #F2F4F4; font-size: 13px; text-transform: uppercase;">
                <th style="width: 50%; border: 1px solid #BDC3C7; padding: 8px; text-align: left;">Earnings Components</th>
                <th style="width: 50%; border: 1px solid #BDC3C7; padding: 8px; text-align: left;">Deductions Components</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="vertical-align: top; border: 1px solid #BDC3C7; padding: 0;">
                    <table style="width: 100%; font-size: 13px;">
                        {% for row in doc.earnings %}
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ECF0F1;">{{ row.salary_component }}</td>
                            <td style="padding: 8px; text-align: right; border-bottom: 1px solid #ECF0F1;">{{ frappe.fmt_money(row.amount, currency=doc.currency) }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </td>
                <td style="vertical-align: top; border: 1px solid #BDC3C7; padding: 0;">
                    <table style="width: 100%; font-size: 13px;">
                        {% for row in doc.deductions %}
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ECF0F1;">{{ row.salary_component }}</td>
                            <td style="padding: 8px; text-align: right; border-bottom: 1px solid #ECF0F1;">{{ frappe.fmt_money(row.amount, currency=doc.currency) }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </td>
            </tr>
            <tr style="font-weight: bold; background-color: #EAEDED;">
                <td style="border: 1px solid #BDC3C7; padding: 8px; text-align: right;">Gross Pay: {{ frappe.fmt_money(doc.gross_pay, currency=doc.currency) }}</td>
                <td style="border: 1px solid #BDC3C7; padding: 8px; text-align: right;">Total Deductions: {{ frappe.fmt_money(doc.total_deduction, currency=doc.currency) }}</td>
            </tr>
        </tbody>
    </table>

    <div style="background-color: #2C3E50; color: white; padding: 12px; border-radius: 4px; font-size: 16px; font-weight: bold; text-align: right; margin-bottom: 20px;">
        NET DISBURSED PAY: {{ frappe.fmt_money(doc.net_pay, currency=doc.currency) }}
    </div>

    <div style="border: 1px solid #BDC3C7; padding: 10px; border-radius: 4px; font-size: 12px; margin-bottom: 40px;">
        <strong>Disbursement Mode:</strong> {{ doc.mode_of_payment or "Bank Transfer" }} | 
        <strong>Bank Destination Account Name:</strong> {{ doc.bank_name or "N/A" }} - {{ doc.bank_account_no or "N/A" }}
    </div>

    <div style="text-align: center; font-size: 10px; color: #95A5A6; border-top: 1px dashed #BDC3C7; padding-top: 10px;">
        CONFIDENTIALITY NOTICE: This document is strictly confidential and proprietary to its corporate source. Internal record format valid without ink stamp verification.
    </div>
</div>"""

    pf = frappe.get_doc({
        "doctype": "Print Format",
        "name": name,
        "doc_type": "Salary Slip",
        "module": "Custom HR",
        "standard": "Yes",
        "print_format_type": "Jinja",
        "html": html_content
    })
    pf.insert(ignore_permissions=True)
    print("Created Print Format")
