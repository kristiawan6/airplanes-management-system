import frappe

def get_context(context):
    # Retrieve current URL path
    current_url = frappe.local.request.path

    # Capture flight name from URL parameters
    flight_name = frappe.form_dict.get('flight_name')

    if flight_name:
        context.flight_name = flight_name
    else:
        context.flight_name = None

    # Example: Adding current URL to context
    context.current_url = current_url
