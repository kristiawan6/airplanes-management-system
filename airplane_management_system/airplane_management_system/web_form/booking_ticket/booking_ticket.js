frappe.ready(function () {
    // Function to fetch and populate the flight field
    function setFlightField() {
        // Fetch the value of 'name' field from the first Airplane Flight document
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Airplane Flight",
                filters: {},
                fieldname: "name"
            },
            callback: function (response) {
                if (response.message && response.message.name) {
                    const flightName = response.message.name;
                    const flightField = $('[data-fieldname="flight"]');
                    
                    if (flightField.length > 0) {
                        // Set the flight name
                        flightField.val(flightName);

                        // Trigger change event to ensure the field is updated
                        flightField.trigger("change");
                    } else {
                        // Handle case where flightField is not found
                        frappe.throw("Flight field not found");
                    }
                } else {
                    // Handle case where no flight name is found
                    frappe.throw("No flight name available");
                }
            },
        });
    }

    // Set the flight field when the form is ready
    setFlightField();
});
