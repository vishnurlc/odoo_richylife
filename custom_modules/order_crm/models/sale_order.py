from odoo import models, fields

class SalesOrder(models.Model):
    _inherit = 'crm.lead'

    agent = fields.Many2one('strapi.user', string='rootid')
    agent12 = fields.Char(string="Email Address")
