import frappe

def update_publication(doc):
	doc.published = 1 if doc.status =="Validated" else 0

def email_technical_team(doc):
	email_template = """
	<p>Bonjour,</p>

	<p>Vous avez été proposé au poste de {{ row.type }} de l'événement {{ doc.subject }} du {{ frappe.utils.format_date(row.jour) }}, à la Halle Tropisme.</p>
	{% if row.horaires %}
	<p>Horaires: {{ row.horaires }}</p>
	{% endif %}

	<p>Souhaitez-vous effectuer cette mission ?</p>

	<table>
	<tbody>
	<tr>
	<td>
	{% set link = "https://tropisme.dokos.cloud/affectation-evenement?id=" + row.name + "&event=" + doc.name + "&ans=" %}
	{% set yes = link + "1" %}
	<a class="btn btn-primary" href={{ yes }}>Oui</a>
	</td>

	<td>
	{% set no = link + "0" %}
	<a class="btn btn-default" href={{ no }}>Non</a>
	</td>
	</tr>
	</tbody>
	</table>

	"""

	if doc.technical_team_required:
		for line in doc.equipe_technique:
			if line.jour and doc.starts_on and doc.ends_on and not (frappe.utils.getdate(doc.ends_on) >= frappe.utils.getdate(line.jour) >= frappe.utils.getdate(doc.starts_on)):
				frappe.throw(f"La date saisie à la ligne {line.idx} du tableau Equipe Technique n'est pas comprise dans les dates de l'événement")

			if line.type and line.utilisateur and line.statut == "Notification à envoyer":
				message = frappe.render_template(email_template, {
					"doc": doc,
					"row": line
				})
				frappe.sendmail(
					recipients=line.utilisateur,
					subject="TROPISME // Proposition d'événement le {{ frappe.utils.format_date(line.jour) }}",
					message=message,
					reference_doctype=doc.doctype,
					reference_name=doc.name,
					expose_recipients="header"
				)
				line.statut = "Option"

def sync_item_booking(doc):
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

def technical_team_no_reply(doc):
	# 72h by default; a setting could be added to change this
	for line in frappe.get_all("Equipe Technique", filters={"statut": "Option"}, fields=["name", "parenttype", "creation"]):
		if line.parenttype == "Event" and frappe.utils.time_diff_in_hours(frappe.utils.now_datetime(), line.creation) > 72:
			frappe.db.set_value("Equipe Technique", line.name, "statut", "Aucune réponse")