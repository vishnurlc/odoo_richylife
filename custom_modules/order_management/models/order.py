from odoo import models, fields, api

class Order(models.Model):
    _name = 'orders.management'
    _description = 'Order Management'

    name = fields.Char(string="Order Name", required=True)
    order_id = fields.Char(string="Order ID", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
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
    ], string='Order Status', default='draft')
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
