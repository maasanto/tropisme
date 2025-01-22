# Copyright (c) 2024, Dokos SAS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class FicheTechnique(Document):
	def link_attachment(doc):
		if doc.owner == "Guest":
			for file in doc.fiches_techniques:
				piece_jointe = frappe.db.get_value("File", dict(file_url=file.piece_jointe))
				frappe.db.set_value("File", piece_jointe, "attached_to_doctype", doc.doctype)
				frappe.db.set_value("File", piece_jointe, "attached_to_name", doc.name)

