frappe.ui.form.on('Customer', {
	setup: function(frm) {
	    frm.trigger("hide_dashboard")
		frm.dashboard.add_transactions([
			{
				'items': ['Event'],
				'label': __('Events')
			}
		])
	},
	refresh: function(frm) {
	    frm.trigger("hide_dashboard")
	},
	hide_dashboard: function(frm) {
	    frm.dashboard.heatmap_area.hide()
		frm.dashboard.wrapper.find(".custom").hide()
	}
})