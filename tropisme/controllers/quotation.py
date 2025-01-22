import frappe

def update_project_event(doc):
	for item in doc.items:
		for field in ["project", "event"]:
			if not item.get(field):
				item.update({field: doc.get(field)})