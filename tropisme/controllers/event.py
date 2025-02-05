import frappe
from frappe.utils.verified_command import get_signed_params

def update_publication(doc, method):
	doc.published = 1 if doc.status =="Validated" else 0

def email_technical_team(doc, method):

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
					subject="Proposition d'événement le {{ frappe.utils.format_date(line.jour) }}",
					message=message,
					reference_doctype=doc.doctype,
					reference_name=doc.name,
					expose_recipients="header",
				)
				line.statut = "Option"

def generate_url_affectation_page(position_row_name, event_name, ans):
	# build attendance confirmation URL
	api_endpoint = frappe.utils.get_url("/affectation-evenement")
	signed_params = get_signed_params({"id": position_row_name, "event": event_name, "ans": ans})
	return f"{api_endpoint}?{signed_params}"

def sync_item_booking(doc, method):
	STATUS_MAP = {
		"Option": "Not confirmed",
		"Validated": "Confirmed",
		"Cancelled": "Cancelled"
	}

	bookings = frappe.get_all("Item Booking", filters={"event": doc.name}, fields=["name", "status"])

	for booking in bookings:
		if booking.status != STATUS_MAP.get(doc.status):
			frappe.db.set_value("Item Booking", booking.name, "status", STATUS_MAP.get(doc.status))
		ib = frappe.get_doc("Item Booking", booking.name)
		ib.starts_on = doc.starts_on
		ib.ends_on = doc.ends_on
		ib.save()

def technical_team_no_reply(doc, method):
	# 72h by default; a setting could be added to change this
	for line in frappe.get_all("Equipe Technique", filters={"statut": "Option"}, fields=["name", "parenttype", "creation"]):
		if line.parenttype == "Event" and frappe.utils.time_diff_in_hours(frappe.utils.now_datetime(), line.creation) > 72:
			frappe.db.set_value("Equipe Technique", line.name, "statut", "Aucune réponse")