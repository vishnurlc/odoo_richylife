from odoo import api, fields, models
import requests
from datetime import datetime
import math


class SaleOrder(models.Model):
    _inherit = "sale.order"
    order_state = fields.Char(string="Server Order Status")

    def fetch_sale_order(self):
        url = 'https://clarity.richylife.ae/api/orders?populate=*'
        token = "a20427239689acf3bd60e94c32b134d307689a42c9bd4437c8438e65d23378a4c3fa47417c4ffe0b1b652e4537547e01a6148d065d5b6a04d2e5d734d445499b87033897d24001f4badb9a8cfba4e39a8c6e79781bae7e86649f61bd65db66cb03001e8e6266998ce3fa4f19a205141354295749e9b5974281cab26444b82c7a"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            print('dataaaaaaaaaaaaa', data)
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return

        for rec in data:
            order_status = rec.get('orderStatus')
            created_at = rec.get('createdAt')
            updated_at = rec.get('updatedAt')
            total_amount = rec.get('total_amount')
            paid_amount = rec.get('paid_amount')
            full_amount_paid = rec.get('full_amount_paid')
            order_items = rec.get('order_items')
            cancellation = rec.get('cancellation')
            order_for = rec.get('order_for')

            # Convert total_amount and paid_amount to float, handling NaN values
            try:
                total_amount = float(total_amount)
                if math.isnan(total_amount):
                    total_amount = 0.0
            except (ValueError, TypeError):
                total_amount = 0.0

            try:
                paid_amount = float(paid_amount)
                if math.isnan(paid_amount):
                    paid_amount = 0.0
            except (ValueError, TypeError):
                paid_amount = 0.0

            partner_id = None
            if order_for:
                partner_email = order_for.get('email')
                partner = self.env['res.partner'].search([('email', '=', partner_email)], limit=1)
                if partner:
                    partner_id = partner.id
                else:
                    partner_data = {
                        'name': order_for.get('name'),
                        'email': partner_email,
                        'phone': order_for.get('phone')
                    }
                    partner = self.env['res.partner'].create(partner_data)
                    partner_id = partner.id


            # Convert dates to Odoo-compatible format
                def convert_date(date_str):
                    try:
                        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        return None

                order_data = {
                    'partner_id': partner_id,
                    'order_state': order_status,
                    'date_order': convert_date(created_at),
                    'amount_total': total_amount,
                    'amount_paid': paid_amount,
                    'order_line': [],
                }

                # for item in order_items:
                #     user = self.env['res.users'].search([('name', '=', item.get('lastupdateby'))])
                #     order_data['order_line'].append((0, 0, {
                #         'name': 'Order Item',
                #         'product_uom_qty': 1,
                #         'price_unit': total_amount,
                #         'write_uid': user.id if user else None
                #     }))

                self.env['sale.order'].create(order_data)
