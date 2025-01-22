# Copyright (c) 2024, Dokos SAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FicheCommunication(Document):
	def before_save(self):
		self.update_event_info()

	def after_insert(self):
		self.link_attachment()

	def update_event_info(self):
		if self.evenement:
			event = frappe.get_doc("Event", self.evenement)
			if not event.repeat_this_event:
				if self.sous_titre_evenement and self.sous_titre_evenement != event.courte_description:
					frappe.db.set_value("Event", self.evenement, "courte_description", self.sous_titre_evenement)
					
				if self.date_et_heure_de_début and self.date_et_heure_de_début != event.starts_on:
					frappe.db.set_value("Event", self.evenement, "starts_on", self.date_et_heure_de_début)
					
				if self.date_et_heure_de_fin and self.date_et_heure_de_fin != event.ends_on:
					frappe.db.set_value("Event", self.evenement, "ends_on", self.date_et_heure_de_fin)

	def link_attachment(self):
		if self.owner == "Guest":
			for file in self.pieces_jointes:
				piece_jointe = frappe.db.get_value("File", dict(file_url=file.piece_jointe))
				frappe.db.set_value("File", piece_jointe, "attached_to_doctype", self.doctype)
				frappe.db.set_value("File", piece_jointe, "attached_to_name", self.name)