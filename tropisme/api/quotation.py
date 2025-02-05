import frappe
import json

@frappe.whitelist()
def get_quotation_from_event():
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw(_("You are not authorized to access this resource"), frappe.PermissionError)

	event_name = frappe.form_dict.name
	event = json.loads(frappe.form_dict.doc)

	items = []

	# Réservations d'articles
	for booking in frappe.get_all("Item Booking", filters={"event": event_name, "status": ("in", ("Confirmed", "Not Confirmed"))}, pluck="item"):
		items.append({
			"item_code": booking,
			"qty": 1,
			"event": event_name,
		})
		
	# Equipe technique
	for agent in event.get("equipe_technique", []):
		if frappe.db.get_value("Event Post Category", agent["position"], "item"):
			items.append({
				"item_code": frappe.db.get_value("Event Post Category", agent["position"], "item"),
				"qty": 1,
				"event": event_name,
			})
		else:
			frappe.throw(f"Veuillez créer un article pour le poste : {agent.get('position')}")

	# Equipe technique
	for agent in event.get("equipe_securite", []):
		if frappe.db.get_value("Event Post Category", agent["type"], "item"):
			items.append({
				"item_code": frappe.db.get_value("Event Post Category", agent["type"], "item"),
				"qty": agent.get("nombre_dheures") * agent.get("unites"),
				"uom": agent.get("tarif"),
				"event": event_name,
			})
		else:
			frappe.throw(f"Veuillez créer un article pour le type d'agent de sécurité: {agent.get('type_agent')}")

	if event.get("besoins_ménage"):
		items.append({
			"item_code": "Forfait Ménage",
			"qty": 1,
			"event": event_name,
		})

	if not items:
		frappe.throw("Aucun article à facturer n'a été trouvé dans cet événement.")

	quotation = frappe.new_doc("Quotation")
	quotation.update({
		"items": items,
		"quotation_to": "Customer",
		"party_name": event.get("customer"),
		"event": event_name,
		"objet": event.get("subject"),
	})
	quotation.set_missing_values()
	quotation.save()

	frappe.response["message"] = quotation