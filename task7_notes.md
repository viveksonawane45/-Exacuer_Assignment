# Task 7 - Scheduler Tasks Implementation Notes

## Query Design & Security
- Leveraged parameterized SQL queries for birthdays and anniversaries to defend against injection vectors.
- Used `frappe.db.count` and standard SQL DISTINCT groupings to capture active heads and LWP summaries.

## Target Audience Verification
- Dynamically resolved manager user profiles using the employee database records.
- Discovered and filtered HR Team recipients by querying `Has Role` for HR roles, preventing incorrect notifications to standard employees.

## Verification & Test Mocking
- Mapped unit tests using `unittest.mock.patch` to override `today()` to return "2025-02-28", proving the Feb 29 non-leap year mapping logic works seamlessly.
- Asserted `Email Queue` entries to verify payroll emails were queued properly.
