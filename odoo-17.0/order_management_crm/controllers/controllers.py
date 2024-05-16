# -*- coding: utf-8 -*-
# from odoo import http


# class OrderManagementCrm(http.Controller):
#     @http.route('/order_management_crm/order_management_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/order_management_crm/order_management_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('order_management_crm.listing', {
#             'root': '/order_management_crm/order_management_crm',
#             'objects': http.request.env['order_management_crm.order_management_crm'].search([]),
#         })

#     @http.route('/order_management_crm/order_management_crm/objects/<model("order_management_crm.order_management_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('order_management_crm.object', {
#             'object': obj
#         })

