frappe.ui.form.on("Airplane Ticket", {
    flight_price: calculate_total_amount,
    flight: fetch_remaining_seat,
    seat_available(frm) {
        if (frm.doc.seat_available <= 0) {
            frappe.msgprint({
                title: __('Flight Fully Booked'),
                indicator: 'red',
                message: __('This flight is already fully booked.')
            });
        } else {
            calculate_total_amount(frm);
        }
    }
});

frappe.ui.form.on("Airplane Ticket Add-on Item", {
    amount: calculate_total_amount,
    quantity: calculate_total_amount,
    add_ons_remove: calculate_total_amount
});

frappe.ui.form.on("Flight Passenger", {
    flight_passenger_add: calculate_total_amount,
    flight_passenger_remove: calculate_total_amount
});

function fetch_remaining_seat(frm) {
    if (frm.doc.flight) {
        frappe.call({
            method: "airplane_management_system.airplane_management_system.doctype.airplane_ticket.ticket.get_remaining_seat_capacity",
            args: {
                flight_id: frm.doc.flight
            },
            callback: function(r) {
                let remaining_seat = r.message || 0;
                frm.set_value('seat_available', remaining_seat);
            },
            error: function(r) {
                console.log(r);
            }
        });
    }
}

function calculate_total_amount(frm) {
    let remaining_seat = frm.doc.seat_available;

    // Check if flight_passenger exists and is an array
    if (!Array.isArray(frm.doc.flight_passenger)) {
        frm.doc.flight_passenger = [];
    }

    let passenger_count = frm.doc.flight_passenger.length;

    // Only perform the check if passengers are added
    if (passenger_count > 0 && passenger_count > remaining_seat) {
        frappe.msgprint({
            title: __('Flight is full'),
            indicator: 'red',
            message: __('Passenger count exceeds the remaining seats.')
        });
        return;
    }

    let total_amount = frm.doc.flight_price || 0;

    if (passenger_count > 0) {
        total_amount *= passenger_count;
    }
    
    if (Array.isArray(frm.doc.add_ons)) {
        for (let item of frm.doc.add_ons) {
            total_amount += (item.amount * item.quantity);
        }
    }

    frm.set_value("total_amount", total_amount);
}
