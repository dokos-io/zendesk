#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe
import phonenumbers
from zendesk.zendesk.connector.zendesk_connector import ZendeskConnector
from frappe.data_migration.doctype.data_migration_connector.connectors.base import BaseConnection

def format_phone_number(doc, method):
	if doc.phone:
		try:
			x = phonenumbers.parse(doc.phone, "FR")
			doc.phone = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
		except Exception as e:
			frappe.throw(str(e))

	if doc.mobile_no:
		try:
			y = phonenumbers.parse(doc.mobile_no, "FR")
			doc.phone = phonenumbers.format_number(y, phonenumbers.PhoneNumberFormat.E164)
		except Exception as e:
			frappe.throw(str(e))


def update_zendesk_phonenumbers():
	connector = ZendeskConnector(BaseConnection)
	users = connector.zenpy_client.users()

	for user in users:
		if user.phone is not None:
			try:
				old_phone =phonenumbers.parse(user.phone, "FR")
				new_phone = phonenumbers.format_number(old_phone, phonenumbers.PhoneNumberFormat.E164)
				user.phone = new_phone

				try:
					response = connector.zenpy_client.users.update(user)
					print(response)
				except Exception as e:
					frappe.log_error(e, "Zendesk Phonenumber update error")
			except phonenumbers.phonenumberutil.NumberParseException:
				continue

def merge_zendesk_users():
	connector = ZendeskConnector(BaseConnection)
	users = connector.zenpy_client.users()

	for user in users:
		if user.name.startswith("Caller +"): 
			for existing_user in connector.zenpy_client.search(type='user', phone=user.phone):
				if existing_user.name != user.name:
					try:
						response = connector.zenpy_client.users.merge(source_user=user, dest_user=existing_user)
						print(response)
					except Exception as e:
						frappe.log_error(e, "Zendesk Phonenumber update error")

			for existing_user in connector.zenpy_client.search(type='user', shared_phone_number=user.phone):
				if existing_user.name != user.name:
					try:
						response = connector.zenpy_client.users.merge(source_user=user, dest_user=existing_user)
						print(response)
					except Exception as e:
						frappe.log_error(e, "Zendesk Phonenumber update error")

def update_all_contact_numbers():
	contacts = frappe.get_all("Contact")

	for contact in contacts:
		c = frappe.get_doc("Contact", contact.name)
		try:
			c.save()
		except Exception as e:
			print(c.name)
			print(e)