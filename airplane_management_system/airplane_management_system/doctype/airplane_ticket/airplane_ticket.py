# Copyright (c) 2024, BroCode and contributors
# For license information, please see license.txt

import random
import string
import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("You can not submit ticket, ticket status must be boarded.")
    
    def before_save(self):
        self.cal_total_amount()
        
        # Set status to Boarded
        self.status = "Boarded"
        
        self.booking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        for passenger in self.flight_passenger:
            passenger.generate_full_name()

        for passenger in self.flight_passenger:
            # Example: Combine first name and last name into full name
            full_name = f"{passenger.first_name} {passenger.last_name}"
            passenger.full_name = full_name.strip()  # Strip to remove any leading/trailing spaces

            # Example: Generate random code for each passenger
            passenger.ticket_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def validate(self):
        unique_data = set()
        filtered_res = []
        for item in self.add_ons:
            if item.get('item') not in unique_data:
                filtered_res.append(item)
                unique_data.add(item.get('item'))
        self.set('add_ons', filtered_res)

    def cal_total_amount(self):
        # Calculate base flight price based on class
        base_price = float(self.flight_price)
        if self.flight_class == "Business Class":
            base_price *= 2
        elif self.flight_class == "First Class":
            base_price *= 5

        # Calculate total amount for add-ons
        total_amount_add_ons = 0.0  # Initialize total amount

        for add_on in self.add_ons:
            if add_on.amount and add_on.quantity:
                try:
                    total_amount_add_ons += float(add_on.amount) * float(add_on.quantity)
                except ValueError:
                    frappe.throw("Invalid amount or quantity in add-ons")

        # Multiply base price by the number of passengers
        passenger_count = len(self.flight_passenger)
        total_amount = base_price * passenger_count + total_amount_add_ons

        # Set the total amount
        self.total_amount = total_amount

