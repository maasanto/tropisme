import frappe
import json

def add_supporting_documents():
	for filename in ["web_page", "event_post_category", "role", "employment_type"]:
		insert_docs_from_json(filename)


def insert_docs_from_json(filename, display_obj_name=False):
	try:
		path_use_case = frappe.get_app_path("tropisme", "setup", f"{filename}.json")
		with open(path_use_case) as f:
			documents = json.load(f)
	except FileNotFoundError:
		return
	if display_obj_name:
		for doc in documents:
			doc = frappe.get_doc(doc)
			print(doc.name)
			doc.insert(ignore_if_duplicate=True)
	else:
		for doc in documents:
			doc = frappe.get_doc(doc)
			doc.insert(ignore_if_duplicate=True)
