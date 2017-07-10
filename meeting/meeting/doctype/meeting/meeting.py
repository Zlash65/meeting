# -*- coding: utf-8 -*-
# Copyright (c) 2017, frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Meeting(Document):
	def validate(self):
		""" Reflect changes when Doctypes are being updated or created or so """
		self.validate_attendees()

	def validate_attendees(self):
		""" Set missing names and avoid duplication """
		for attendee in self.attendees:
			if not attendee.full_name:
				attendee.full_name = get_full_name(attendee.attendee)

	def on_update(self):
		""" Sync ToDos appropraitely """
		self.sync_todos()

	def sync_todos(self):
		""" Sync ToDos for assignments """
		# todos_added = [minute.todo for minute in self.minutes if minute.todo]
		# todos_added = frappe.get_all("ToDo")
		todos_added = [todo.name for todo in 
			frappe.get_all("ToDo",
				filters={
					"reference_type": self.doctype,
					"reference_name": self.name,
					"assigned_by": ""
				})
			]

		# print todos_added

		for minute in self.minutes:
			if minute.assigned_to and minute.status=="Open":
				# print self.name
				if not minute.todo:
					todo = frappe.get_doc({
						"doctype": "ToDo",
						"description": minute.description,
						"reference_type": self.doctype,
						"reference_name": self.name,
						"owner": minute.assigned_to
					})
					todo.insert()
					# print todo.description
					minute.db_set("todo", todo.name, update_modified=False)	
					# minute.todo = todo.name

				else:
					todos_added.remove(minute.todo)
			else:
				minute.db_set("todo", None, update_modified=False)

		for todo in todos_added:
			todo = frappe.get_doc("ToDo", todo)
			todo.flags.from_meeting	= True
			# frappe.delete_doc("ToDo", todo)
			todo.delete()

@frappe.whitelist()
def get_full_name(attendee):
	""" Fetch the full name of the User from 'User Doctype' """
	user =  frappe.get_doc("User", attendee)
	# Filter and add First name / Last name
	return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))