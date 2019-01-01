from __future__ import unicode_literals
import frappe
from frappe.data_migration.doctype.data_migration_connector.connectors.base import BaseConnection
from frappe.utils.response import json_handler
import json
from frappe.utils import now_datetime, get_datetime
from frappe.utils.error import make_error_snapshot
from zenpy import Zenpy
from zenpy.lib.api_objects import User, Organization, OrganizationField

class ZendeskConnector(BaseConnection):
	def __init__(self, connector):
		self.connector = connector
		self.settings = frappe.get_doc("Zendesk Settings", None)
		if not self.settings.last_sync:
			frappe.db.set_value("Zendesk Settings", None, last_sync, now_datetime())

		self.name_field = 'id'

		try:
			self.zenpy_client = Zenpy(**{
				'email' : self.settings.email,
				'token' : self.settings.get_password(fieldname='api_token',raise_exception=False),
				'subdomain': self.settings.subdomain
			})
		except Exception as e:
			frappe.log_error(e, 'Zendesk Connection Error')

		try:
			found = False
			if self.settings.org_type_id:
				for field in self.zenpy_client.organization_fields():
					if field.id == self.settings.org_type_id:
						found = True

				if found == False:
					for field in self.zenpy_client.organization_fields():
						if field.key == 'is_supplier' and field.type == 'checkbox':
							frappe.db.set_value("Zendesk Settings", "Zendesk Settings", "org_type_id", field.id)
							found = True

				if found == False:
					self.create_custom_field()
			else:
				for field in self.zenpy_client.organization_fields():
					if field.key == 'is_supplier' and field.type == 'checkbox':
						frappe.db.set_value("Zendesk Settings", "Zendesk Settings", "org_type_id", field.id)
						found = True
				if found == False:
					self.create_custom_field()
		except Exception as e:
			frappe.log_error(e, 'Zendesk Setup Error')

	def create_custom_field(self, id=None):
		custom_field = OrganizationField(type="checkbox", title="Is a supplier", key="is_supplier", raw_title="Is a supplier")
		try:
			self.zenpy_client.organization_fields.create(custom_field)
		except Exception as e:
			frappe.log_error(e, 'Zendesk custom field creation error')

	def get(self, remote_objectname, fields=None, filters=None, start=0, page_length=10):
		search = filters.get('search')
		organization_type = filters.get('organization_type')
		export_type = filters.get('export_type')

		if remote_objectname == 'User':
			if export_type == "incremental":
				try:
					return self.get_users(search, start, page_length)
				except Exception as e:
					frappe.log_error(e, 'Zendesk Contact Get Error')

			else:
				try:
					return self.get_incremental_users(search, start, page_length)
				except Exception as e:
					frappe.log_error(e, 'Zendesk Contact Get Error')

		if remote_objectname == 'Organization':
			try:
				return self.get_organizations(search, organization_type, start, page_length)
			except Exception as e:
				frappe.log_error(e, 'Zendesk Company Get Error')

	def insert(self, doctype, doc):
		if doctype == 'User':
			try:
				return self.insert_users(doc)
			except Exception as e:
				frappe.log_error("Doc {0}: {1}".format(doc, e), 'Zendesk Contact Insert Error')

		frappe.log_error(doc, "Insert")
		if doctype == 'Organization':
			try:
				return self.insert_organizations(doc)
			except Exception as e:
				frappe.log_error("Doc {0}: {1}".format(doc, e), 'Zendesk Organization Insert Error')

	def update(self, doctype, doc, migration_id):
		if doctype == 'User':
			try:
				return self.update_users(doc, migration_id)
			except Exception as e:
				frappe.log_error("Doc {0}: {1}".format(doc, e), 'Zendesk Contact Update Error')

		if doctype == 'Organization':
			try:
				return self.update_organizations(doc, migration_id)
			except Exception as e:
				frappe.log_error("Doc {0}: {1}".format(doc, e), 'Zendesk Company Update Error')

	def delete(self, doctype, migration_id):
		pass

	def get_users(self, search, start=0, page_length=100):
		users = self.zenpy_client.users()

		result = []
		for user in users:
			result.append(user)
		return list(result)

	def get_incremental_users(self, search, start=0, page_length=100):
		users = self.zenpy_client.users.incremental(start_time=get_datetime(self.settings.last_sync))

		result = []
		for user in users:
			result.append(user)

		frappe.db.set_value("Zendesk Settings", None, last_sync, now_datetime())
		return list(result)

	def get_organizations(self, search, organization_type, start=0, page_length=100):
		organizations = self.zenpy_client.organizations()

		result = []
		for org in organizations:
			if organization_type == "customer":
				if not org.organization_fields["is_supplier"] or org.organization_fields["is_supplier"] == False:
					result.append(org)
			else:
				if org.organization_fields["is_supplier"] == True:
					result.append(org)

		return list(result)

	def insert_users(self, doc):
		user = User(
			id=doc.id,
			name=doc.name,
			email=doc.email,
			phone=doc.phone,
			organization_id=doc.organization_id
		)
		created_user = self.zenpy_client.users.create(user)

		if hasattr(created_user, "error"):
			frappe.log_error("Doc {0}: {1}".format(doc, created_user.description), "Zendesk Contact Insert Response Error")
		else:
			return {self.name_field: created_user.id}

	def insert_organizations(self, doc):
		if hasattr(doc, "organization_fields"):
			organization = Organization(name=doc.name, organization_fields=doc.organization_fields)
		else:
			organization = Organization(name=doc.name)
		created_organization = self.zenpy_client.organizations.create(organization)

		if hasattr(created_organization, "error"):
			frappe.log_error("Doc {0}: {1}".format(doc, created_organization.description), "Zendesk Companies Insert Error")
		else:
			return {self.name_field: created_organization.id}

	def update_users(self, doc, migration_id):
		user = User(
			id=doc.id,
			name=doc.name,
			email=doc.email,
			phone=doc.name,
			organization_id=doc.organization_id
		)
		updated_user = self.zenpy_client.users.create_or_update(user)

		if hasattr(updated_user, "error"):
			frappe.log_error("Id {0}: {1}".format(migration_id, updated_user.description), "Zendesk Contact Update Error")
		else:
			return {self.name_field: updated_user.id}

	def update_organizations(self, doc, migration_id):
		organization = Organization(id=doc.id, name=doc.name, organization_fields=doc.organization_fields)
		updated_organization = self.zenpy_client.organizations.update(organization)

		if hasattr(updated_organization, "error"):
			frappe.log_error("Id {0}: {1}".format(migration_id, updated_organization.description), "Zendesk Company Update Error")
		else:
			return {self.name_field: updated_organization.id}
