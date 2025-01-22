import frappe
import json

@frappe.whitelist()
def get_quotation_from_event():
	event_name = frappe.form_dict.name
	event = json.loads(frappe.form_dict.doc)
	cost_center = frappe.form_dict.cost_center

	items = []

	# Réservations d'articles
	for booking in frappe.get_all("Item Booking", filters={"event": event_name, "status": ("in", ("Confirmed", "Not Confirmed"))}, pluck="item"):
		items.append({
			"item_code": booking,
			"qty": 1,
			"event": event_name,
			"cost_center": cost_center
		})
		
	# Equipe technique
	for agent in event.get("equipe_technique", []):
		if frappe.db.get_value("Item", agent.get("type")):
			items.append({
				"item_code": agent.get("type"),
				"qty": 1,
				"event": event_name,
				"cost_center": cost_center
			})
		else:
			frappe.throw(f"Veuillez créer un article pour le type d'agent technique: {agent.get('type')}")

	# Equipe technique
	for agent in event.get("equipe_securite", []):
		if frappe.db.get_value("Item", agent.get("type_agent")):
			items.append({
				"item_code": agent.get("type_agent"),
				"qty": agent.get("nombre_dheures") * agent.get("unites"),
				"uom": agent.get("tarif"),
				"event": event_name,
				"cost_center": cost_center
			})
		else:
			frappe.throw(f"Veuillez créer un article pour le type d'agent de sécurité: {agent.get('type_agent')}")

	if event.get("besoins_ménage"):
		items.append({
			"item_code": "Forfait Ménage",
			"qty": 1,
			"event": event_name,
			"cost_center": cost_center
		})

	if not items:
		frappe.throw("Aucun article à facturer n'a été trouvé dans cet événement.")

	quotation = frappe.new_doc("Quotation")
	quotation.update({
		"items": items,
		"quotation_to": "Customer",
		"party_name": event.get("customer"),
		"cost_center": cost_center,
		"company": frappe.db.get_value("Cost Center", cost_center, "company"),
		"event": event_name,
		"taxes_and_charges": "TVA 20% - HT"
	})
	quotation.set_missing_values()

	frappe.response["message"] = quotation