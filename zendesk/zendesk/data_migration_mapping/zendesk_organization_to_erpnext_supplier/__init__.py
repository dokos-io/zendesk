#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(organization):
	suppliers = frappe.db.sql("""
		SELECT
			name
		FROM
			tabSupplier
		WHERE
			name = '%s'
		AND
			(zendesk_sync_id != '%s' OR zendesk_sync_id IS NULL)
	""" % (frappe.db.escape(organization.name), organization.id), as_dict=True)

	for supplier in suppliers:
		try:
			frappe.db.set_value("Supplier", frappe.safe_decode(supplier.name), "zendesk_sync_id", organization.id)
		except Exception as e:
			frappe.log_error(e, organization.name)

	organization.supplier_group = frappe.db.get_value("Buying Settings", None, "supplier_group")

	return organization

def post_process(remote_doc=None, local_doc=None, **kwargs):
	pass