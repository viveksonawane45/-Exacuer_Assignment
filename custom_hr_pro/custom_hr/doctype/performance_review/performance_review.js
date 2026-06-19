// Copyright (c) 2026, DeepMind Pair Programmer and contributors
// For license information, please see license.txt

frappe.ui.form.on("Performance Review", {
	refresh(frm) {
		calculate_live_score(frm);
	},
	employee(frm) {
		if (frm.doc.employee) {
			frappe.db.get_value("Employee", frm.doc.employee, "reports_to")
				.then(r => {
					let reports_to = r.message.reports_to;
					if (reports_to) {
						frappe.db.get_value("Employee", reports_to, "employee_name")
							.then(mgr_name_res => {
								frm.set_value("manager_name", mgr_name_res.message.employee_name);
							});
					} else {
						frm.set_value("manager_name", "");
					}
				});
		} else {
			frm.set_value("manager_name", "");
		}
	}
});

frappe.ui.form.on("Performance Review KPI", {
	target_value(frm, cdt, cdn) {
		calculate_live_score(frm);
	},
	achieved_value(frm, cdt, cdn) {
		calculate_live_score(frm);
	},
	score(frm, cdt, cdn) {
		calculate_live_score(frm);
	},
	kpis_remove(frm, cdt, cdn) {
		calculate_live_score(frm);
	},
	kpis_add(frm, cdt, cdn) {
		calculate_live_score(frm);
	}
});

function calculate_live_score(frm) {
	let total = 0;
	let count = 0;
	if (frm.doc.kpis) {
		frm.doc.kpis.forEach(kpi => {
			if (kpi.score) {
				total += parseFloat(kpi.score);
				count++;
			}
		});
	}
	let avg = count > 0 ? (total / count).toFixed(2) : "0.00";
	frm.set_value("overall_score", count > 0 ? total / count : 0);

	let badge_color = "gray";
	if (parseFloat(avg) >= 4.0) badge_color = "green";
	else if (parseFloat(avg) >= 3.0) badge_color = "blue";
	else if (parseFloat(avg) >= 2.0) badge_color = "orange";
	else if (parseFloat(avg) > 0) badge_color = "red";

	if (frm.fields_dict.live_score_badge) {
		frm.fields_dict.live_score_badge.$wrapper.html(`
			<div style="padding: 12px 18px; border-radius: 6px; background-color: var(--bg-${badge_color}-light, #f4f4f4); border-left: 5px solid var(--border-${badge_color}, #007bff); display: inline-block; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
				<span style="font-weight: 600; font-size: 1.15em; color: var(--text-${badge_color}, #333);">Live Average Score: ${avg}</span>
			</div>
		`);
	}

	render_dashboard(frm);
}

function render_dashboard(frm) {
	if (!frm.fields_dict.dashboard_html_view) return;

	if (!frm.doc.kpis || frm.doc.kpis.length === 0) {
		frm.fields_dict.dashboard_html_view.$wrapper.html(`
			<div style="padding: 20px; text-align: center; color: var(--text-muted); border: 1px dashed var(--border-color); border-radius: 6px; background-color: var(--bg-light-gray, #fafafa);">
				No KPIs added yet. Add items to the KPIs grid to view progression chart.
			</div>
		`);
		return;
	}

	let html = `
		<div style="font-family: var(--font-stack-sans); padding: 18px; border: 1px solid var(--border-color); border-radius: 6px; background: var(--card-bg, #fff); box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 10px;">
			<h4 style="margin-top: 0; margin-bottom: 18px; font-weight: 600; color: var(--text-color, #1f2937); font-size: 1.1em;">KPI Progression Dashboard</h4>
			<div style="display: grid; grid-template-columns: 1fr; gap: 16px;">
	`;

	frm.doc.kpis.forEach((kpi, idx) => {
		let target = kpi.target_value || 0;
		let achieved = kpi.achieved_value || 0;
		let percentage = target > 0 ? Math.min(100, Math.round((achieved / target) * 100)) : 0;

		let bar_color = "var(--primary, #007bff)";
		if (percentage >= 100) bar_color = "var(--green, #28a745)";
		else if (percentage >= 75) bar_color = "var(--blue, #17a2b8)";
		else if (percentage >= 50) bar_color = "var(--orange, #fd7e14)";
		else if (percentage > 0) bar_color = "var(--red, #dc3545)";

		html += `
			<div style="padding-bottom: 12px; border-bottom: 1px solid var(--border-color, #eaeaea);">
				<div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
					<span style="font-weight: 500; color: var(--text-color, #374151); font-size: 0.95em;">${kpi.goal || `Goal #${idx + 1}`}</span>
					<span style="font-size: 0.88em; color: var(--text-muted, #6b7280); font-weight: 500;">${achieved} / ${target} (${percentage}%)</span>
				</div>
				<div style="width: 100%; background: var(--bg-light-gray, #f3f4f6); height: 8px; border-radius: 4px; overflow: hidden;">
					<div style="width: ${percentage}%; background: ${bar_color}; height: 100%; border-radius: 4px; transition: width 0.3s ease;"></div>
				</div>
			</div>
		`;
	});

	html += `
			</div>
		</div>
	`;
	frm.fields_dict.dashboard_html_view.$wrapper.html(html);
}
