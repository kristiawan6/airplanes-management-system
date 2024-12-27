# Copyright (c) 2024, BroCode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
    def generate_full_name(self):
        if self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        else:
            self.full_name = f"{self.first_name}"

    def before_save(self):
        self.generate_full_name()