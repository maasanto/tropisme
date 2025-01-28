frappe.ui.form.on('Project', {
	setup: function(frm) {
		frm.dashboard.add_transactions([
			{
				'items': ['Event'],
				'label': __('Events')
			}
		])
	},
})