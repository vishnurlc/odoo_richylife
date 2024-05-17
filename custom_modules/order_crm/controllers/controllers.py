# -*- coding: utf-8 -*-
from odoo import http


class OrderCrm(http.Controller):
    @http.route('/order_crm/order_crm', auth='public')
    def index(self, **kw):
        return "Hello, world"

    # @http.route('/order_crm/order_crm/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('order_crm.listing', {
    #         'root': '/order_crm/order_crm',
    #         'objects': http.request.env['order_crm.order_crm'].search([]),
    #     })
    #
    # @http.route('/order_crm/order_crm/objects/<model("order_crm.order_crm"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('order_crm.object', {
    #         'object': obj
    #     })

