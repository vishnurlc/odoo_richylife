from odoo import api, fields, models
import requests
from datetime import datetime
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    provider = fields.Char(string="Provider")
    status = fields.Selection(
        [('verified', 'Verified'), ('confirmed', 'Confirmed'), ('blocked', 'Blocked')], string='status')
    invitee_id = fields.Char(string='Invitee ID')
    referral_id = fields.Char(string='Referral ID')
    referrallink = fields.Char(string='Referral Link')
    usertype = fields.Char(string='User Type')
    bio = fields.Text(string='Bio')
    language_id = fields.Many2one(
        "res.lang",
        string="Language",
        default=lambda self: self.env["res.lang"].search(
            [("code", "=", self.env.lang)], limit=1
        ),
    )
    currency_id = fields.Many2one('res.currency', string='Currency', required=False,
                                  default=lambda self: self._default_currency_id())
    date_of_birth = fields.Date(string="Date of Birth")
    nationality = fields.Char(string='Nationality')
    server_id = fields.Integer(string="Server ID")
    verified = fields.Boolean(string='verified')

    def action_do_something(self):
        # verify only if it's not verified
        if self.verified:
            raise UserError("The record is already verified.")

        url = "http://localhost:1337/api/odoo"
        token = "897bb065dfd4245af91a50c643bf19f3143ed36291957ace85580bfba509ad2f3007916558c8017ff242c6af4571599095df72ece27eced4c5360f334cbf5de5db61e49a3bb61fde1235532e08612ff09761f0dc9ee2fefaea5a160a0df270019bdb96ffad796dfb025c8c34c5102f72b03d077825797125bd78804144d86523"  # Replace with your actual token

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "userid": self.server_id
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            print(data)
        except requests.exceptions.RequestException as e:
            print("Error fetching data from API: %s", e)

        self.verified = True

    def _get_status(self, rec):
        if rec.get('Profile', {}).get('verified'):
            return 'verified'
        elif rec.get('confirmed'):
            return 'confirmed'
        elif rec.get('blocked'):
            return 'blocked'
        else:
            return False

    @api.model
    def fetch_customer(self):
        customer_data = requests.get('https://clarity.richylife.ae/api/users')
        if customer_data.status_code == 200:
            customer = customer_data.json()
            for rec in customer:
                print('dattaaaaaa', rec)
                existing_customer = self.env['res.partner'].search(
                    [('email', '=', rec['email']), ('server_id', '=', rec.get('id'))], limit=1)

                username = rec.get('username') or ''
                surname = rec.get('surname') or ''

                # Convert date_of_birth to the correct format
                date_of_birth = rec.get('date_of_birth')
                if date_of_birth:
                    try:
                        date_of_birth = datetime.strptime(date_of_birth, '%d-%m-%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        date_of_birth = None

                user_data = {
                    'name': username + " " + surname,
                    'email': rec.get('email'),
                    'provider': rec.get('provider'),
                    'status': self._get_status(rec),
                    'create_date': rec.get('createdAt'),
                    'write_date': rec.get('updatedAt'),
                    'invitee_id': rec.get('invitee_id'),
                    'referral_id': rec.get('referralId'),
                    'referrallink': rec.get('referrallink'),
                    'usertype': rec.get('usertype'),
                    'bio': rec.get('bio'),
                    'currency_id': rec.get('currency') if rec.get('currency') else None,
                    'phone': rec.get('phone'),
                    'date_of_birth': date_of_birth,
                    'nationality': rec.get('nationality'),
                    'server_id': rec.get('id')
                }

                if existing_customer:
                    existing_customer.write(user_data)
                else:
                    self.env['res.partner'].create(user_data)
