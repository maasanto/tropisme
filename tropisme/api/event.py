import frappe
from frappe.utils.verified_command import verify_request, get_signed_params

@frappe.whitelist()
def technical_team_assignment():
	if not verify_request():
		return
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

@frappe.whitelist()
def get_bookings_and_assignee():
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw(_("You are not authorized to access this resource"), frappe.PermissionError)

	event = frappe.form_dict.get("event")
	doc = frappe.get_doc("Event", event)

	frappe.response['message'] = {
		"bookings": frappe.get_all("Item Booking", filters={"event": doc.name}, fields=["name", "status"]),
		"assignees": doc.get_assigned_users()
	}

@frappe.whitelist()
def email_technical_team():

	email_template = """
	<p>Bonjour,</p>

	<p>Vous avez été proposé au poste de {{ row.position }} de l'événement {{ doc.subject }} du {{ frappe.utils.format_date(row.jour) }}.</p>
	{% if row.horaires %}
	<p>Horaires: {{ row.horaires }}</p>
	{% endif %}

	<p>Souhaitez-vous effectuer cette mission ?</p>

	<table>
	<tbody>
	<tr>
	<td>
	<a class="btn btn-primary" href={{ url_yes }}>Oui</a>
	</td>

	<td>
	<a class="btn btn-default" href={{ url_no }}>Non</a>
	</td>
	</tr>
	</tbody>
	</table>

	"""
	doc = frappe.get_doc("Event", frappe.form_dict.name)
	if doc.technical_team_required:
		for line in doc.equipe_technique:
			if line.jour and doc.starts_on and doc.ends_on and not (frappe.utils.getdate(doc.ends_on) >= frappe.utils.getdate(line.jour) >= frappe.utils.getdate(doc.starts_on)):
				frappe.throw(f"La date saisie à la ligne {line.idx} du tableau Equipe Technique n'est pas comprise dans les dates de l'événement")

			if line.position and line.utilisateur and line.statut == "Notification à envoyer":
				message = frappe.render_template(email_template, {
					"doc": doc,
					"row": line,
					"url_yes" : generate_url_affectation_page(line.name, doc.name, "1"),
					"url_no": generate_url_affectation_page(line.name, doc.name, "0"),
				})
				frappe.sendmail(
					recipients=line.utilisateur,
					subject=f"Proposition d'événement le { frappe.utils.format_date(line.jour) }",
					message=message,
					reference_doctype=doc.doctype,
					reference_name=doc.name,
					expose_recipients="header",
				)
				
				line.statut = "Option"
		doc.save(ignore_permissions=True)

def generate_url_affectation_page(position_row_name, event_name, ans):
	# build attendance confirmation URL
	api_endpoint = frappe.utils.get_url("/affectation-evenement")
	signed_params = get_signed_params({"id": position_row_name, "event": event_name, "ans": ans})
	return f"{api_endpoint}?{signed_params}"