const color_map = {
    "Programmation": "#F5B041",
    "Privatisation": "#009688",
    "Pôle bien-être": "#85C1E9",
    "Atelier": "#F7DC6F",
    "Travaux": "#848889",
    "Autres": "#bfc4c4",
    "Animation pro": "#2980B9",
    "RDV pro" : "#A2D9CE",
    "Jeune public" : "#D7BDE2",
    "Foodisme" : "#FFECB3",
    "Exposition" : "#de633d",
    "Résidence" : "#da8989",
    "En ligne" : "#000000",
    "Montage/Démontage" :"#6f7071",
    "Médiation" :"#e0d6e5",
    "Réservations Café Tropisme" :"#FFECB3",
    "Animation Pro" :"#A2D9CE"
}


frappe.ui.form.on('Event', {
	onload(frm) {
		frm.set_query('project', function(doc) {
			return {
				filters: {
					"status": "Open"
				}
			};
		});
		
		frm.set_query('employe', 'equipe_technique', function(doc) {
			return {
				filters: {
					"employment_type": "Intermittent"
				}
			};
		});
		
		frm.set_value("color", color_map[frm.doc.event_category] || '');
		
	},
	refresh(frm) {
	  if (!frm.is_new()) {
		    frm.add_custom_button(__("Créer un devis"), () => {
		        frm.trigger("make_quotation")
		    })
		}
		
		frm.trigger("check_bookings_and_assignments")
	},
	before_save(frm) {
	   if (frm.is_new() && frm.doc.status == "Validated") {
	       frm.trigger('show_technical_team_dialog')
	   }
	},
	event_category(frm) {
	    frm.set_value("color", color_map[frm.doc.event_category] || '');
	},
	status(frm) {
	    if (frm.doc.status == "Validated") {
	        frm.trigger('show_technical_team_dialog')
	    }
	},
	
	show_technical_team_dialog(frm) {
	    const dialog = new frappe.ui.Dialog({
	        title: __("L'équipe"),
			fields: [
				{
					fieldname: "technical_team_required",
					label: "Avez-vous besoin d'une équipe technique ?",
					fieldtype: "Check",
					default: frm.doc.technical_team_required
				},
				{
					fieldname: "security_team_required",
					label: "Avez-vous besoin d'une équipe de sécurité ?",
					fieldtype: "Check",
					default: frm.doc.security_team_required
				},
				{
					fieldname: "cleaning_team_required",
					label: "Avez-vous besoin d'une équipe de ménage ?",
					fieldtype: "Check",
					default: frm.doc.cleaning_team_required
				},
			],
			primary_action_label: "Valider",
			primary_action: (data) => {
			    frm.set_value("technical_team_required", data.technical_team_required);
			    frm.set_value("security_team_required", data.security_team_required);
			    frm.set_value("cleaning_team_required", data.cleaning_team_required);
			    dialog.hide()
			}
	    })
	    
	    dialog.show()
	},
	
	make_quotation(frm) {
	    frappe.prompt(
			{
				fieldtype: "Link",
				label: "Code Analytique",
				fieldname: "cost_center",
				reqd: 1,
				options: "Cost Center"
			},
			function(data) {
			   return frappe.call({
        			method: "tropisme.api.quotation.get_quotation_from_event",
        			args: {
        				"name": frm.doc.name,
        				"doc": frm.doc,
        				"cost_center": data.cost_center
        			}
        		}).then(r => {
        		    console.log(r.message)
        		    r.message.__islocal = 1
        			const doclist = frappe.model.sync(r.message);
        			frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
        		}); 
			});
	},
	
	check_bookings_and_assignments(frm) {
	    if (frm.is_new()) {
	        return
	    }

	    frappe.call({
	       method: "tropisme.api.event.get_bookings_and_assignee",
	       args: {
	           "event": frm.doc.name
	       }
	   }).then(r => {
	       if (!r.message.bookings.length) {
	           frappe.show_alert({
	               message: "Veuillez réserver au moins une salle pour cet événement",
	               indicator: "orange"
	           })
	       }
	       
	       if (!r.message.assignees.length) {
	           frappe.show_alert({
	               message: "Veuillez attribuer ce ticket à au moins une personne",
	               indicator: "orange"
	           })
	       }
	   })
	}
})

frappe.ui.form.on('Equipe Securite', {
	arrivee(frm, cdt, cdn) {
		calculate_hours(frm, cdt, cdn)
	},
	depart(frm, cdt, cdn) {
		calculate_hours(frm, cdt, cdn)
	},
	change(frm, cdt, cdn) {
		const row = locals[cdt][cdn]
		if (!row.debut) {
		    frappe.model.set_value(cdt, cdn, "arrivee", frm.doc.starts_on)
		}

		if (!row.fin) {
		    frappe.model.set_value(cdt, cdn, "depart", frm.doc.ends_on)
		}
	},
	
	equipe_securite_add(frm, cdt, cdn) {
	    const row = locals[cdt][cdn]
		if (!row.debut) {
		    frappe.model.set_value(cdt, cdn, "arrivee", frm.doc.starts_on)
		}

		if (!row.fin) {
		    frappe.model.set_value(cdt, cdn, "depart", frm.doc.ends_on)
		}
	}
})


frappe.ui.form.on('Equipe Menage', {
	change(frm, cdt, cdn) {
		const row = locals[cdt][cdn]
		if (!row.debut) {
		    frappe.model.set_value(cdt, cdn, "debut", frm.doc.starts_on)
		}

		if (!row.fin) {
		    frappe.model.set_value(cdt, cdn, "fin", frm.doc.ends_on)
		}
	},
	
	equipe_menage_add(frm, cdt, cdn) {
	    const row = locals[cdt][cdn]
		if (!row.debut) {
		    frappe.model.set_value(cdt, cdn, "debut", frm.doc.starts_on)
		}

		if (!row.fin) {
		    frappe.model.set_value(cdt, cdn, "fin", frm.doc.ends_on)
		}
	}
})

frappe.ui.form.on('Equipe Technique', {
    equipe_technique_add(frm, cdt, cdn) {
	    const row = locals[cdt][cdn]
		if (!row.jour) {
		    frappe.model.set_value(cdt, cdn, "jour", frm.doc.starts_on)
		}
	}
})

const calculate_hours = (frm, cdt, cdn) => {
    const row = locals[cdt][cdn]
    if (row.arrivee && row.depart) {
        frappe.model.set_value(cdt, cdn, "nombre_dheures", flt(frappe.datetime.get_minute_diff(row.depart, row.arrivee) / 60, 2))
    }
}