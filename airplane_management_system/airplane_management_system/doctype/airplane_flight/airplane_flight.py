# Copyright (c) 2024, BroCode and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status = "Completed"
	
	def before_submit(self):
		date_of_departure_str = self.date_of_departure
		flight_count = frappe.db.count('Airplane Flight', filters={'date_of_departure': self.date_of_departure})		
		unique_flight = flight_count + 1
		unique_flight_str = f"{unique_flight:04d}"
		self.route = f"flight/{date_of_departure_str}-{unique_flight_str}"
		self.is_published = 1

	@frappe.whitelist()
	def set_flight_status(self):
		flight = frappe.get_doc("Airplane Flight",)
		flight.status = "Completed"
		flight.save()
