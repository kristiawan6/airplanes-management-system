# Copyright (c) 2024, air and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count,Sum
 
def execute(filters=None):
	columns = get_columns()
	data = get_data()
	chart_data = get_chart_data(data)
	return columns, data,None,chart_data

def get_columns():
	return [
	{
		"label": "Airline",
		"fieldname": "airline",
		"fieldtype": "Link",
		"options": "Airline",
   		"width": 200
	}
	,
	{
		"label": "Revenue",
		"fieldname": "revenue",
		"fieldtype": "Currency",
		"width": 120
	} 
	]

def get_data():
	result =  frappe.db.sql("""
	select airplanes.airline , IFNULL(Sum(airticket.total_amount),0) as 'revenue' 
	from `tabAirplane` airplanes left outer join  
	`tabAirplane Flight` airflights on airflights.airplane = airplanes.name
	left outer join `tabAirplane Ticket` airticket
	on  airticket.flight = airflights.name
	group by  airplanes.airline order by Sum(airticket.total_amount)  desc; """
	 ,as_dict=True) 
	return result


def get_chart_data(data):
	labels=[]
	values=[]
   
	for d in data:
		labels.append(d.airline)
		values.append([d.revenue])
	
   
	return{
	"data": {
		"labels": labels,
		"datasets":[{"values":values
		}]},
		"type":"donut"
	}