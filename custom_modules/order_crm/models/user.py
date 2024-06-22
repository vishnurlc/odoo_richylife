from odoo import models, fields, api, http
import requests
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StrapiUser(models.Model):
    _name = 'strapi.user'
    _description = 'Strapi User'

    rootid = fields.Integer(string='Roorid', required=True)
    username = fields.Char(string='Username', required=True)
    email = fields.Char(string='Email', required=True)
    provider = fields.Char(string='Provider')
    verified = fields.Boolean(string='verified')
    confirmed = fields.Boolean(string='Confirmed')
    blocked = fields.Boolean(string='Blocked')
    created_at = fields.Char(string='Created At')
    updated_at = fields.Char(string='Updated At')
    invitee_id = fields.Char(string='Invitee ID')
    referral_id = fields.Char(string='Referral ID')
    referrallink = fields.Char(string='Referral Link')
    usertype = fields.Char(string='User Type')
    bio = fields.Text(string='Bio')
    language = fields.Char(string='Language')
    currency = fields.Char(string='Currency')
    userid = fields.Char(string='User ID')
    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    surname = fields.Char(string='Surname')
    date_of_birth = fields.Char(string='Date of Birth')
    nationality = fields.Char(string='Nationality')


    # @api.onchange('verified')
    # def _onchange_verified(self):
    #     self._trigger_action()

    def _trigger_action(self):
        # Custom logic to be executed when 'note' field changes
        print(f"The note has been changed to: {self.verified}")
        # Example action: log a message or update another field

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
            "userid": self.rootid  # Replace with the actual field name for user ID
        }

        try:
            response = requests.post(url, headers=headers,json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()  # Parse the JSON response
            print(data)
        except requests.exceptions.RequestException as e:
            _logger.error("Error fetching data from API: %s", e)

        for record in self:
            record.verified = True
        return True

    # @api.model
    # def write(self, vals):
    #     result = super(StrapiUser, self).write(vals)
    #     if 'verified' in vals:
    #         # Make the API call to update the verified field in your backend
    #         self._update_verified_in_backend()
    #     return result

    # def _update_verified_in_backend(self):
    #     # Your backend URL and endpoint
    #     backend_url = 'https://your-backend.com/api/update_verified'
        
    #     # Authentication details (replace with actual token or credentials)
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': 'Bearer your-access-token'  # Use the correct authentication method
    #     }
        
    #     for record in self:
    #         payload = {
    #             'user_id': record.id,
    #             'verified': record.verified
    #         }
            
    #         response = requests.post(backend_url, headers=headers, json=payload)
    #         if response.status_code == 200:
    #             _logger.info('Successfully updated verified status in backend for user_id: %s', record.id)
    #         else:
    #             _logger.error('Failed to update verified status in backend for user_id: %s. Status: %s, Response: %s', record.id, response.status_code, response.text) 