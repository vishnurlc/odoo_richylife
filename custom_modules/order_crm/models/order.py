from odoo import models, fields

class StrapiOrder(models.Model):
    _name = 'strapi.order'
    _description = 'Strapi Order'

    user_id = fields.Many2one('strapi.user', string='User', required=True)
    order_details = fields.Text(string='Order Details')
