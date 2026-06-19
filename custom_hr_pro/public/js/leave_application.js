frappe.ui.form.on('Leave Application', {
	refresh: function(frm) {
		frm.add_custom_button(__('Check Remaining Allocation Balances'), function() {
			if (!frm.doc.employee || !frm.doc.posting_date) {
				frappe.msgprint(__('Please assign an employee target along with a processing posting date window boundary execution baseline.'));
				return;
			}
			
			frappe.call({
				method: "hrms.hr.doctype.leave_application.leave_application.get_leave_details",
				args: {
					employee: frm.doc.employee,
					date: frm.doc.posting_date
				},
				callback: function(r) {
					if (r.message && r.message.leave_allocation) {
						let content = `<table class="table table-bordered font-sm">
							<thead><tr><th>Leave Allocation Type</th><th>Remaining Count Days Available</th></tr></thead><tbody>`;
						for (let type in r.message.leave_allocation) {
							let alloc = r.message.leave_allocation[type];
							content += `<tr><td><strong>${type}</strong></td><td>${alloc.remaining_leaves}</td></tr>`;
						}
						content += `</tbody></table>`;
						
						frappe.msgprint({
							title: __('Dynamic Allocation Balance Ledger Overview'),
							message: content,
							indicator: 'blue'
                        });
                    }
                }
            });
        }, __("Actions"));
    }
});
