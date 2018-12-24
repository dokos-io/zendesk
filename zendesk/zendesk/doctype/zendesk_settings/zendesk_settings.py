# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dokos and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ZendeskSettings(Document):
	def validate(self):
		if self.enabled == 1:
			self.create_zendesk_connector()
			self.create_zendesk_plan()

	def sync(self):
		"""Create and execute Data Migration Run for Zendesk Sync plan"""
		frappe.has_permission('Zendesk Settings', throw=True)

		exists = frappe.db.exists('Data Migration Run', dict(status=('in', ['Fail', 'Error']),	name=('!=', self.name)))
		if exists:
			failed_run = frappe.get_doc("Data Migration Run", dict(status=('in', ['Fail', 'Error'])))
			failed_run.delete()

		started = frappe.db.exists('Data Migration Run', dict(status=('in', ['Started']),	name=('!=', self.name)))
		if started:
			print("Break")
			return

		try:
			doc = frappe.get_doc({
				'doctype': 'Data Migration Run',
				'data_migration_plan': 'Zendesk Sync',
				'data_migration_connector': 'Zendesk Connector'
			}).insert()

			try:
				doc.run()
			except Exception:
					frappe.log_error(frappe.get_traceback())
		except Exception as e:
			frappe.logger().debug({"Zendesk Error: "}, e)

	def create_zendesk_connector(self):
		if frappe.db.exists('Data Migration Connector', 'Zendesk Connector'):
			zendesk_connector = frappe.get_doc('Data Migration Connector', 'Zendesk Connector')
			zendesk_connector.connector_type = 'Custom'
			zendesk_connector.python_module = 'zendesk.zendesk.connector.zendesk_connector'
			zendesk_connector.save()
			return

		frappe.get_doc({
			'doctype': 'Data Migration Connector',
			'connector_type': 'Custom',
			'connector_name': 'Zendesk Connector',
			'python_module': 'zendesk.zendesk.connector.zendesk_connector',
		}).insert()

	def create_zendesk_plan(self):
		if frappe.db.exists('Data Migration Plan', 'Zendesk Sync'):
			zendesk_sync = frappe.get_doc('Data Migration Plan', 'Zendesk Sync')
			zendesk_sync.module = "Zendesk"
			zendesk_sync.update({"mappings":[]})

			mappings = ["Zendesk Organization to ERPNext Customer", "Zendesk User to ERPNext Contact"]

			for mapping in mappings:
				zendesk_sync.append("mappings", {
					"mapping": mapping,
					"enabled": 1
				})
			zendesk_sync.save()
			frappe.db.commit()
			return

		else:
			zendesk_sync = frappe.get_doc('Data Migration Plan', 'Zendesk Sync')
			zendesk_sync.module = "Zendesk"

			mappings = ["Zendesk Organization to ERPNext Customer", "Zendesk User to ERPNext Contact"]

			for mapping in mappings:
				zendesk_sync.append("mappings", {
					"mapping": mapping,
					"enabled": 1
				})
			zendesk_sync.insert()

@frappe.whitelist()
def sync(force=False):
	zendesk_settings = frappe.get_doc('Zendesk Settings')
	if zendesk_settings.enabled == 1 and (zendesk_settings.auto_sync == 1 or force == "True"):
		if not frappe.db.exists('Data Migration Connector', 'Zendesk Connector'):
			zendesk_settings.create_zendesk_connector()
		if not frappe.db.exists('Data Migration Plan', 'Zendesk Sync'):
			zendesk_settings.create_zendesk_plan()
		try:
			zendesk_settings.sync()
		except Exception:
			frappe.log_error(frappe.get_traceback())