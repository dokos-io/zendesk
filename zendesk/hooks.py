# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "zendesk"
app_title = "Zendesk"
app_publisher = "Dokos"
app_description = "Zendesk Connector"
app_icon = "fas fa-desktop"
app_color = "#78a300"
app_email = "hello@dokos.io"
app_license = "GNU General Public License v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zendesk/css/zendesk.css"
# app_include_js = "/assets/zendesk/js/zendesk.js"

# include js, css files in header of web template
# web_include_css = "/assets/zendesk/css/zendesk.css"
# web_include_js = "/assets/zendesk/js/zendesk.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

docs_app = "zendesk"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "zendesk.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "zendesk.install.before_install"
# after_install = "zendesk.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zendesk.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Contact": {
		"on_update": "zendesk.zendesk.utils.format_phone_number"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"zendesk.zendesk.doctype.zendesk_settings.zendesk_settings.sync"
	]
}

# Testing
# -------

# before_tests = "zendesk.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "zendesk.event.get_events"
# }

