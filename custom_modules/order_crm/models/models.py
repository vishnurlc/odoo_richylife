# -*- coding: utf-8 -*-

import requests
import logging
from odoo import models, fields, api


class Order(models.Model):
    _name = 'order_crm.order_crm'
    _description = 'order_crm.order_crm'

    # name = fields.Char(string="Order Name", required=True)
    order_id = fields.Char(string="Order ID", required=True, readonly=False)
    ordered_person_name = fields.Char(string="Ordered Person Name", required=True)
    image = fields.Binary(string="Image")
    email = fields.Char(string="Email Address", required=True)
    phone = fields.Char(string="Phone Number", required=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ], string='Payment Status', default='pending')
    order_status = fields.Selection([
        ('pending', 'pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string='Order Status', default='pending')
    value = fields.Integer(string="Value")
    value2 = fields.Float(compute="_compute_value_pc", store=True, string="Computed Value")
    description = fields.Text(string="Description")

    @api.model
    def create(self, vals):
        if vals.get('order_id', _('New')) == _('New'):
            vals['order_id'] = self.env['ir.sequence'].next_by_code('orders.management') or _('New')
        result = super(Order, self).create(vals)
        return result

    @api.depends('value')
    def _compute_value_pc(self):
        for order in self:
            order.value2 = float(order.value) * 0.10  # Example computation


    @api.model
    def fetch_data_from_api(self):
        url = "http://localhost:1337/api/orders?populate=*"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()  # Parse the JSON response
            print(data)
            self._process_api_data(data)  # Process the fetched data
        except requests.exceptions.RequestException as e:
            _logger.error("Error fetching data from API: %s", e)

    def _process_api_data(self, data):
        for item in data:
            # Find existing record by external_id
            existing_record = self.search([('external_id', '=', item.get('id'))], limit=1)
            if existing_record:
                # Update existing record
                existing_record.write({
                    'order_id': item.get('id'),
                    'description': item.get('description'),
                })
            else:
                # Create new record
                self.create({
                    'name': item.get('name'),
                    'description': item.get('description'),
                    'external_id': item.get('id'),
                })
# from odoo import models, fields, api


# class order_crm(models.Model):
#     _name = 'order_crm.order_crm'
#     _description = 'order_crm.order_crm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

