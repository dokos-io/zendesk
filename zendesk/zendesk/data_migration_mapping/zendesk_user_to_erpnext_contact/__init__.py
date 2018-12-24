#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(user):
	name = frappe.safe_decode(user.name)
	if "," in name:
		firstname = name.split(',')[-1]
		lastname = name.split(',')[0]
	else:
		firstname = name.split()[0]
		lastname = name.split()[-1]

	phone = frappe.safe_decode(user.phone) if user.phone is not None else user.phone

	if user.email is not None and phone is not None:
		condition = "(email_id = '{0}' OR phone = '{1}') AND (zendesk_sync_id != '{2}' OR zendesk_sync_id IS NULL)".format(user.email, frappe.safe_encode(phone), user.id)
	elif user.email is not None:
		condition = "email_id = '{0}' AND (zendesk_sync_id != '{1}' OR zendesk_sync_id IS NULL)".format(user.email, user.id)
	elif phone is not None:
		condition = "phone = '{0}' AND (zendesk_sync_id != '{1}' OR zendesk_sync_id IS NULL)".format(frappe.safe_encode(phone), user.id)

	contacts = frappe.db.sql("""
		SELECT
			name
		FROM
			tabContact
		WHERE
			%s
	""" % condition, as_dict=True)
	for contact in contacts:
		try:
			frappe.db.set_value("Contact", frappe.safe_decode(contact.name), "zendesk_sync_id", user.id)
		except Exception as e:
			frappe.log_error(e, user.name)

	return {
		'id': user.id,
		'firstname': firstname,
		'lastname': lastname,
		'email': user.email,
		'phone': phone
	}

def post_process(remote_doc=None, local_doc=None, **kwargs):
	if not local_doc:
		return

	user = remote_doc
	erpnext_contact = local_doc

	if user:
		organization = user.organization_id
		if organization:
			if frappe.db.exists("Supplier", dict(zendesk_sync_id=organization)):
				supplier = frappe.get_doc("Supplier", dict(zendesk_sync_id=organization))
				erpnext_contact.append("links",{"link_doctype": "Supplier", "link_name": supplier.name})
				erpnext_contact.save()
				frappe.db.commit()

			elif frappe.db.exists("Customer", dict(zendesk_sync_id=organization)):
				customer = frappe.get_doc("Customer", dict(zendesk_sync_id=organization))
				erpnext_contact.append("links",{"link_doctype": "Customer", "link_name": customer.name})
				erpnext_contact.save()
				frappe.db.commit()

			elif frappe.db.exists("Lead", dict(zendesk_sync_id=organization)):
				leadorg = frappe.get_doc("Lead", dict(zendesk_sync_id=organization))
				leadorg.status = "Converted"
				erpnext_contact.append("links",{"link_doctype": "Lead", "link_name": leadorg.name})
				erpnext_contact.save()
				frappe.db.commit()

			else:
				return