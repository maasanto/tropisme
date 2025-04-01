import frappe
from frappe.utils.verified_command import get_signed_params

def update_publication(doc, method):
	doc.published = 1 if doc.status =="Validated" else 0

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