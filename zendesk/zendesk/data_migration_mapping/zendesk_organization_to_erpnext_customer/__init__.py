#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(organization):
	customers = frappe.db.sql("""
		SELECT
			name
		FROM
			tabCustomer
		WHERE
			name = '%s'
		AND
			(zendesk_sync_id != '%s' OR zendesk_sync_id IS NULL)
	""" % (frappe.db.escape(organization.name), organization.id), as_dict=True)

	for customer in customers:
		try:
			frappe.db.set_value("Customer", frappe.safe_decode(customer.name), "zendesk_sync_id", organization.id)
		except Exception as e:
			frappe.log_error(e, organization.name)

	organization.customer_group = frappe.db.get_value("Selling Settings", None, "customer_group")

	return organization

def post_process(remote_doc=None, local_doc=None, **kwargs):
	pass