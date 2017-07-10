# -*- coding: utf-8 -*-
# Copyright (c) 2017, frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

class TestMeeting(unittest.TestCase):
	def test_sync_todos_add(self):
		""" Test case for testing creation of ToDo when a minutes in meeting Doctype is set. """
		meeting = make_meeting()
		todos = get_todos(meeting)

		self.assertEquals(todos[0].name, meeting.minutes[0].todo)
		self.assertEquals(todos[0].description, meeting.minutes[0].description)

	def test_sync_todos_remove(self):
		""" To test whether a ToDo is deleted or not when Minutes's status is set to 'Closed' """
		meeting = make_meeting()
		
		meeting.minutes[0].status = "Closed"
		meeting.save()

		todos = get_todos(meeting)
		self.assertEquals(len(todos), 0)

	def test_sync_todos_on_close_todo(self):
		""" Testing if ToDo's status set to 'Closed' deletes it or not. """
		meeting = make_meeting()

		todos = get_todos(meeting)
		todo = frappe.get_doc("ToDo", todos[0].name)
		todo.status = "Closed"
		todo.save()

		meeting.reload()
		self.assertEquals(meeting.minutes[0].status, "Closed")
		self.assertFalse(meeting.minutes[0].todo)

		def test_sync_todos_on_delete_todo(self):
			""" Deleting ToDo should set Minutes's status to 'Closed' """
			meeting = make_meeting()

			todos = get_todos(meeting)
			todo = frappe.get_doc("ToDo", todos[0].name)
			todo.delete()

			meeting.reload()
			self.assertEquals(meeting.minutes[0].status, "Closed")
			self.assertFalse(meeting.minutes[0].todo)

def make_meeting():
	""" Generate a new dummy meeting and save it. """
	meeting = frappe.get_doc({
		"doctype": "Meeting",
		"title": "Test Meeitng",
		"status": "Planned",
		"date": "2017-07-20",
		"from_time": "09:00",
		"to_time": "09:30",
		"minutes": [
			{
				"description": "Test minute 1",
				"status": "Open",
				"assigned_to": "test@example.com"
			}
		]
	})
	meeting.insert()
	return meeting

def get_todos(meeting):
	""" Generate a dummy ToDo for a particular Meeting """
	return frappe.get_all("ToDo", 
		filters={
			"reference_type": meeting.doctype, 
			"reference_name": meeting.name, 
			"owner": "test@example.com"
		},
		fields=["name", "description"])