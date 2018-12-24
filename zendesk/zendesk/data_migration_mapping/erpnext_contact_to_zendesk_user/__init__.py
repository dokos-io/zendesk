#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(doc):
	if not isinstance(doc, dict):
		doc = doc.as_dict()
	company_name = None
	company_doctype = None
	company = None

	if hasattr(doc, 'links'):
		for link in doc["links"]:
			company_name = link["link_name"]
			company_doctype = link["link_doctype"]

			if company_doctype == "Customer":
				company = frappe.db.get_value(company_doctype, company_name, "zendesk_sync_id")

	if doc["first_name"] and doc["last_name"]:
		name = doc["first_name"] + " " + doc["last_name"]
	else:
		name = doc["first_name"]

	returned_doc = {
		'name': name,
		'email_id': doc["email_id"],
		'phone': doc["phone"],
		'company': company,
		'zendesk_sync_id': doc["zendesk_sync_id"]
	}

	return returned_doc