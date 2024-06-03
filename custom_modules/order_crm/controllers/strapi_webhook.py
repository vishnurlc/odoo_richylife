from odoo import http

class StrapiWebhook(http.Controller):
    @http.route('/strapi/webhook', type='json', auth='public')
    def strapi_webhook(self, **kwargs):
        if 'user' in kwargs:
            user_data = kwargs['user']
            existing_user = http.request.env['strapi.user'].search([('email', '=', user_data['email'])])
            if not existing_user:
                http.request.env['strapi.user'].create({
                    'name': user_data['name'],
                    'email': user_data['email'],
                })
        elif 'order' in kwargs:
            order_data = kwargs['order']
            user = http.request.env['strapi.user'].search([('email', '=', order_data['user']['email'])])
            if user:
                http.request.env['strapi.order'].create({
                    'user_id': user.id,
                    'order_details': order_data['details'],
                })
        return {'status': 'success'}

    @http.route('/refresh_fetch_strapi_data',auth='public', website=True)
    def refresh_fetch_strapi_data(self):
        http.request.env['fetch.strapi.data'].fetch_strapi_data()
        return "helllo"