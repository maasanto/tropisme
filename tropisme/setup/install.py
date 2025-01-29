import frappe
import json

def add_webpage():
	insert_docs_from_json("web_page")

def add_notifications():
	insert_docs_from_json("notification")


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
