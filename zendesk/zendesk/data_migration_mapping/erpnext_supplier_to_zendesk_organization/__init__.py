#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(organization):
	if not isinstance(organization, dict):
		organization = organization.as_dict()

	organization["organization_fields"] = {"is_supplier": 1}
	return organization

def post_process(remote_doc=None, local_doc=None, **kwargs):
	pass