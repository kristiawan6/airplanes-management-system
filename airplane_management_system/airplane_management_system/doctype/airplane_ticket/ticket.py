import frappe

@frappe.whitelist()
def get_remaining_seat_capacity(flight_id) :
    flight = frappe.get_doc("Airplane Flight", flight_id)
    max_capacity = flight.capacity_seat
    
    total_passengers = frappe.db.sql("""
        SELECT COUNT(fp.name)
        FROM `tabFlight Passenger` fp
        JOIN `tabAirplane Ticket` at ON at.name = fp.parent
        WHERE at.flight = %s AND at.docstatus < 2
    """, (flight_id,))[0][0] or 0
    
    return max_capacity - total_passengers

