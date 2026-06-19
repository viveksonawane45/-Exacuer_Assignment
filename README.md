# Custom HR Pro

Custom Enterprise HR Performance & Analytics Extension Suite. This custom app extends standard ERPNext HRMS and Frappe Framework with features including employee data validations, a submittable performance review, script reports, custom print formats, and a React-based analytics dashboard SPA.

## Key Features

1. **Employee Customization**: Added custom fields to the standard Employee record (t-shirt size, blood group, privacy agreement status) with automated warnings for unsigned agreements (>30 days tenure).
2. **Submittable Performance Review**:
   - Custom `Performance Review` DocType and `Performance Review KPI` child table.
   - Dynamic naming series formatted as `PR-{YYYY}-{#####}`.
   - Real-time client-side live average score calculations and visual goal progression dashboard.
   - Automated submit triggers creating ToDos for manager PIP assignments (< 2.0 score) or inserting praise Comments on Employee records (> 4.0 score).
3. **Leave Application Overrides**:
   - Restricted leaves longer than 5 consecutive days unless a reason is supplied.
   - Dynamic balance checks inside the form view.
4. **Attendance Summary Script Report**:
   - Compiles headcount, late entry, and appraisal score metrics.
5. **Scheduler Milestones Alert**:
   - Runs daily to calculate active employee birthdays/work anniversaries with Feb 29 leap-year protection.
6. **Executive Dashboard React SPA**:
   - Built with Vite, Tailwind CSS v4, TypeScript, Recharts, and `frappe-react-sdk`.
   - Served statically inside the custom app assets directory.

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd /your-bench-directory
bench get-app https://github.com/viveksonawane45/-Exacuer_Assignment.git custom_hr_pro --branch version-16
bench --site your-site-name install-app custom_hr_pro
bench --site your-site-name migrate
```

## Running Unit Tests

Run the custom integration test suite using:

```bash
bench --site your-site-name run-tests --app custom_hr_pro
```

---

## Contributing

This app uses `pre-commit` for code formatting and linting. Enable it:

```bash
cd apps/custom_hr_pro
pre-commit install
```

## License

MIT
