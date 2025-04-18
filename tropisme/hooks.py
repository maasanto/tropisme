app_name = "tropisme"
app_title = "Tropisme"
app_publisher = "Dokos SAS"
app_description = "Personnalisations pour la Halle Tropisme"
app_email = "hello@dokos.io"
app_license = "gpl-3.0"
source_link = "https://gitlab.com/dokos/tropisme"
required_apps = ["hrms"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tropisme/css/tropisme.css"
# app_include_js = "/assets/tropisme/js/tropisme.js"

# include js, css files in header of web template
# web_include_css = "/assets/tropisme/css/tropisme.css"
# web_include_js = "/assets/tropisme/js/tropisme.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tropisme/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Event": "public/js/event.js",
	"Project": "public/js/project.js",
	"Customer": "public/js/customer.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tropisme/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

fixtures = [
	# {"dt": "Web Page", "filters": {"module": "tropisme"}},
	# {"dt": "Notification", "filters": {"module": "tropisme"}},
	# {"dt": "Event Post Category"},
	# {"dt": "Role", "filters":{"name": "Event Scheduler"}}
	{"dt": "Employment Type", "filters": {"name": "Intermittent"}}
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tropisme.utils.jinja_methods",
# 	"filters": "tropisme.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tropisme.install.before_install"
# after_install = "tropisme.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tropisme.uninstall.before_uninstall"
# after_uninstall = "tropisme.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

after_install = [
	"tropisme.setup.install.add_supporting_documents"
]

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tropisme.utils.before_app_uninstall"
# after_app_uninstall = "tropisme.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tropisme.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Event": {
		"before_save": [
			"tropisme.controllers.event.update_publication",
		],
		"after_save": "tropisme.controllers.event.sync_item_booking",
	},
	"Quotations": {
		"before_validate": "tropisme.controllers.quotation.update_project_event"
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"tropisme.controllers.event.technical_team_no_reply"
	]
}

# Testing
# -------

# before_tests = "tropisme.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tropisme.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tropisme.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tropisme.utils.before_request"]
# after_request = ["tropisme.utils.after_request"]
# Job Events
# ----------
# before_job = ["tropisme.utils.before_job"]
# after_job = ["tropisme.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tropisme.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

