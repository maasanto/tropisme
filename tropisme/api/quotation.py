import frappe
import json

@frappe.whitelist()
def get_quotation_from_event():
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw(_("You are not authorized to access this resource"), frappe.PermissionError)

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
		if frappe.db.get_value("Event Post Category", agent["position"], "item"):
			items.append({
				"item_code": frappe.db.get_value("Event Post Category", agent["position"], "item"),
				"qty": 1,
				"event": event_name,
				"cost_center": cost_center
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
		"event": event_name
	})
	quotation.set_missing_values()

	frappe.response["message"] = quotation