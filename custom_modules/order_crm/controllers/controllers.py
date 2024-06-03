# -*- coding: utf-8 -*-
from odoo import http
import requests
import logging

_logger = logging.getLogger(__name__)



class OrderCrm(http.Controller):
    @http.route('/order_crm/order_crm', auth='public', website=True)
    def index(self, **kw):
        data = self.fetch_data_from_api(_logger)
        print(data[0]['id'])
        return http.request.render('order_crm.hello_template', {'data':data})

    def fetch_data_from_api(self, _logger=None):
        url = "http://localhost:1337/api/orders?populate=*"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()  # Parse the JSON response
            print(data)
            return data['data']
        except requests.exceptions.RequestException as e:
            _logger.error("Error fetching data from API: %s", e)


    @http.route('/order_crm/order_crm/objects', auth='public')
    def list(self, **kw):
        return http.request.render('order_crm.listing', {
            'root': '/order_crm/order_crm',
            'objects': http.request.env['order_crm.order_crm'].search([]),
        })

    @http.route('/order_crm/order_crm/objects/<model("order_crm.order_crm"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('order_crm.object', {
            'object': obj
        })

