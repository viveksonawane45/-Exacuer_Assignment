# Task 9 - HR Analytics Dashboard Notes

This file details the operational notes and characteristics of the HR Analytics Dashboard built using React (Vite) and Frappe APIs.

## Setup Architecture
- **Backend API**: Exposes whitelisted endpoints under `custom_hr_pro/custom_hr_pro/api/dashboard.py`.
- **Frontend SPA**: Placed inside `custom_hr_pro/hr-dashboard/` and built using React. Output directory is set dynamically to compile to `custom_hr_pro/custom_hr_pro/public/hr-dashboard/`.

## Key Features
- Parallelized requests using `Promise.all()` to pull dashboard metrics.
- Custom styled components for KPIs, charts, and tables without bloated peer dependencies.
- Handles standard `/api/method/login` session cookie auth redirects.
