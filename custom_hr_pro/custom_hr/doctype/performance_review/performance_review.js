// Copyright (c) 2026, DeepMind Pair Programmer and contributors
// For license information, please see license.txt

frappe.ui.form.on("Performance Review", {
	onload(frm) {
		get_previous_score(frm);
	},
	refresh(frm) {
		calculate_live_score(frm);
	},
	employee(frm) {
		if (frm.doc.employee) {
			get_previous_score(frm);
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
			frm.previous_score = null;
			calculate_live_score(frm);
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

function get_previous_score(frm) {
	if (!frm.doc.employee) return;
	frappe.call({
		method: "custom_hr_pro.api.review.get_previous_review_score",
		args: {
			employee: frm.doc.employee
		},
		callback(r) {
			if (r.message && r.message.length > 0) {
				frm.previous_score = parseFloat(r.message[0].overall_score || 0);
			} else {
				frm.previous_score = 0.0;
			}
			calculate_live_score(frm);
		}
	});
}

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
	let avg = count > 0 ? (total / count) : 0.0;
	frm.set_value("overall_score", avg);

	render_kpi_dashboard(frm, avg);
}

function render_kpi_dashboard(frm, score) {
	if (!frm.fields_dict.kpi_dashboard) return;

	let rating_label = "Poor";
	let badge_color = "#dc3545"; // Red

	if (score >= 2.0) {
		rating_label = "Average";
		badge_color = "#fd7e14"; // Orange
	}
	if (score >= 3.0) {
		rating_label = "Good";
		badge_color = "#007bff"; // Blue
	}
	if (score >= 4.5) {
		rating_label = "Excellent";
		badge_color = "#28a745"; // Green
	}

	// Calculate difference comparison
	let comparison_html = "";
	if (frm.previous_score !== undefined && frm.previous_score !== null) {
		let diff = score - frm.previous_score;
		let diff_symbol = "";
		let diff_color = "#6c757d";

		if (diff > 0) {
			diff_symbol = "+";
			diff_color = "#28a745"; // Green
		} else if (diff < 0) {
			diff_color = "#dc3545"; // Red
		}

		comparison_html = `
			<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 12px; padding: 20px; text-align: center; flex: 1;">
				<h4 style="margin: 0 0 10px 0; color: #6c757d; font-size: 0.9em; text-transform: uppercase;">Previous Review Comparison</h4>
				<h2 style="margin: 0; font-size: 1.8em; color: #495057;">${frm.previous_score.toFixed(2)}</h2>
				<p style="margin: 5px 0 0 0; font-weight: bold; color: ${diff_color}; font-size: 0.95em;">
					Difference: ${diff_symbol}${diff.toFixed(2)}
				</p>
			</div>
		`;
	} else {
		comparison_html = `
			<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 12px; padding: 20px; text-align: center; flex: 1;">
				<h4 style="margin: 0 0 10px 0; color: #6c757d; font-size: 0.9em; text-transform: uppercase;">Previous Review</h4>
				<h2 style="margin: 0; font-size: 1.2em; color: #6c757d; font-weight: 500; min-height: 44px; display: flex; align-items: center; justify-content: center;">No history found</h2>
			</div>
		`;
	}

	let kpis_html = "";
	if (frm.doc.kpis && frm.doc.kpis.length > 0) {
		frm.doc.kpis.forEach((kpi, idx) => {
			let target = kpi.target_value || 0;
			let achieved = kpi.achieved_value || 0;
			let percentage = target > 0 ? Math.min(100, (achieved / target) * 100) : 0;
			let bar_color = "#007bff"; // Blue

			if (percentage >= 100) bar_color = "#28a745"; // Green
			else if (percentage >= 75) bar_color = "#17a2b8"; // Cyan
			else if (percentage >= 50) bar_color = "#ff9800"; // Orange
			else if (percentage > 0) bar_color = "#dc3545"; // Red

			kpis_html += `
				<div style="padding: 12px 0; border-bottom: 1px solid #eee;">
					<div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.95em; font-weight: 500;">
						<span style="color: #333;">${kpi.goal || `Goal #${idx + 1}`}</span>
						<span style="color: #666;">${achieved} / ${target} (${percentage.toFixed(0)}%)</span>
					</div>
					<div style="width:100%; background:#f1f1f1; border-radius:10px; height:16px; overflow:hidden;">
						<div style="width:${percentage}%; background:${bar_color}; height:16px; border-radius:10px; text-align:center; color:white; font-size: 0.75em; line-height: 16px; transition: width 0.3s ease;">
							${percentage > 10 ? `${percentage.toFixed(0)}%` : ""}
						</div>
					</div>
				</div>
			`;
		});
	} else {
		kpis_html = `
			<div style="text-align: center; color: #999; padding: 20px 0;">
				No KPIs added yet. Build the KPI rows to populate progress.
			</div>
		`;
	}

	let html = `
		<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 5px 0;">
			<div style="display: flex; gap: 20px; margin-bottom: 25px; flex-wrap: wrap;">
				<!-- Overall Score Card -->
				<div style="background:${badge_color}; padding:20px; border-radius:12px; color:white; text-align:center; flex: 1; min-width: 150px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
					<h4 style="margin: 0 0 10px 0; color: rgba(255,255,255,0.85); font-size: 0.9em; text-transform: uppercase; font-weight: 600;">Overall Score</h4>
					<h1 style="margin: 0; font-size: 2.5em; line-height: 1; font-weight: 800;">${score.toFixed(2)}</h1>
					<h3 style="margin: 5px 0 0 0; font-weight: 700; font-size: 1.1em;">${rating_label}</h3>
				</div>
				<!-- Comparison Card -->
				${comparison_html}
			</div>
			
			<div style="background: white; border: 1px solid #dee2e6; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
				<h3 style="margin-top: 0; margin-bottom: 15px; font-size: 1.1em; font-weight: 600; color: #333;">KPI Goal Progress Bars</h3>
				<div style="display: flex; flex-direction: column; gap: 5px;">
					${kpis_html}
				</div>
			</div>
		</div>
	`;

	frm.fields_dict.kpi_dashboard.$wrapper.html(html);

	if (frm.fields_dict.dashboard_html_view) {
		frm.fields_dict.dashboard_html_view.$wrapper.html(html);
	}
}
