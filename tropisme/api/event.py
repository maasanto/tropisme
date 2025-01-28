import frappe

@frappe.whitelist()
def technical_team_assignment():
	if frappe.form_dict.get("event"):
		if frappe.form_dict.get("id"):
			status = "Validé" if frappe.form_dict.get("ans") == "1" else "Refusé"
			frappe.db.set_value("Equipe Technique", frappe.form_dict.get("id"), "statut", status)

			# event = frappe.get_doc("Event", frappe.form_dict.get("event"))
			# assigned_users = event.get_assigned_users()

			doc = frappe.new_doc("Validation Equipe Technique")
			doc.evenement = frappe.form_dict.get("event")
			doc.line_id = frappe.form_dict.get("id")
			doc.reponse = status
			doc.employee = frappe.db.get_value("Equipe Technique", frappe.form_dict.get("id"), "employe")
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			
			# doc = frappe.get_doc("Event", frappe.form_dict.get("event"))
			# doc.run_notifications("validation_equipe_technique")

			frappe.response['type'] = 'redirect'
			frappe.response.location = "/message?title=Merci&message=Votre réponse a bien été enregistrée"
			
		else:
			frappe.response['type'] = 'redirect'
			frappe.response.location = "/message?title=Erreur&message=Votre réponse n'a pas pu être enregistrée correctement"
			
	else:
		frappe.response['type'] = 'redirect'
		frappe.response.location = "/message?title=Erreur&message=Votre réponse n'a pas pu être enregistrée correctement"

def get_bookings_and_assignee():
	event = frappe.form_dict.get("event")
	doc = frappe.get_doc("Event", event)

	frappe.response['message'] = {
		"bookings": frappe.get_all("Item Booking", filters={"event": doc.name}, fields=["name", "status"]),
		"assignees": doc.get_assigned_users()
	}