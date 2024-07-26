from odoo import http
from odoo.http import request
from datetime import datetime
import base64


class CustomerController(http.Controller):

    @http.route('/create/customer', type='json', auth='public', methods=['POST'], csrf=False)
    def create_customer(self, **kw):
        username = kw.get('username') or ''
        surname = kw.get('surname') or ''
        email = kw.get('email')
        date_of_birth = kw.get('date_of_birth')
        if not username or not email:
            return {'error': 'Name and email are required fields'}
        existing_customer = request.env['res.partner'].sudo().search(
            [('email', '=', kw.get('email')), ('server_id', '=', kw.get('server_id'))], limit=1)
        user_data = {
            'server_id': kw.get('server_id'),
            'name': username + " " + surname,
            'email': kw.get('email'),
            'provider': kw.get('provider'),
            'create_date': kw.get('createdAt'),
            'write_date': kw.get('updatedAt'),
            'invitee_id': kw.get('invitee_id'),
            'referral_id': kw.get('referralId'),
            'referrallink': kw.get('referrallink'),
            'usertype': kw.get('usertype'),
            'bio': kw.get('bio'),
            'currency_id': kw.get('currency') if kw.get('currency') else None,
            'phone': kw.get('phone'),
            'date_of_birth': date_of_birth,
            'nationality': kw.get('nationality'),
        }

        if existing_customer:
            existing_customer.sudo().write(user_data)
            return {'success': True, 'customer_id': existing_customer.id}
        else:
            customer = request.env['res.partner'].sudo().create(user_data)
            return {'success': True, 'customer_id': customer.id}

    @http.route('/create/product_template', type='json', auth='public', methods=['POST'], csrf=False)
    def create_product_template(self, **kw):

        # Extract fields from the params
        server_id = kw.get('server_id')
        description = kw.get('description')
        destination_name = kw.get('destination_name')
        image = kw.get('image')
        fuel = kw.get('fuel')
        seat = kw.get('seat')
        speed = kw.get('speed')
        engine = kw.get('engine')
        transmission = kw.get('transmission')
        perdaylimit = kw.get('perdaylimit')
        cylinder = kw.get('cylinder')
        deposit = kw.get('deposit')
        body = kw.get('body')
        service_name = kw.get('service_name')
        city_name = kw.get('city_name')
        name = kw.get('name')
        list_price = kw.get('list_price')

        # # Process the image if provided
        # if image:
        #     image_binary = base64.b64decode(image)
        # else:
        #     image_binary = None

        vals = {
            'name': name,
            'list_price': list_price,
            'server_id': server_id,
            'description': description,
            'destination_name': destination_name,
            # 'image': image_binary,
            # 'image_1920': image_binary,
            'fuel': fuel,
            'seat': seat,
            'speed': speed,
            'engine': engine,
            'transmission': transmission,
            'perdaylimit': perdaylimit,
            'cylinder': cylinder,
            'deposit': deposit,
            'body': body,
            'service_name': service_name,
            'city_name': city_name,
        }

        # Create or update the product template
        product = request.env['product.template'].sudo().search([('server_id', '=', server_id)])
        if product:
            product.sudo().write(vals)
        else:
            product = request.env['product.template'].sudo().create(vals)

        return {'success': True, 'product_id': product.id}

    @http.route('/create/order', type='json', auth='public', methods=['POST'], csrf=False)
    def create_order(self, **kw):
        partner_server_id = kw.get('partner_server_id')
        partner_email = kw.get('partner_email')
        order_lines = kw.get('order_lines')

        partner_id = request.env['res.partner'].search(
            [('server_id', '=', partner_server_id), ('email', '=', partner_email)], limit=1)

        if partner_id:
            order_data = {
                'partner_id': partner_id.id,
                'order_line': [],
            }

            for item in order_lines:
                product_id = request.env['product.product'].search([('server_id', '=', item.get('id'))], limit=1)
                if product_id:
                    order_data['order_line'].append((0, 0, {
                        'product_id': product_id.id,
                        'product_uom_qty': item.get('product_uom_qty'),
                        'price_unit': item.get('price_unit'),
                    }))

            sale_order = request.env['sale.order'].create(order_data)

            return {'success': True, 'order_id': sale_order.id}
        else:
            return {'success': False, 'error': 'Partner not found'}
