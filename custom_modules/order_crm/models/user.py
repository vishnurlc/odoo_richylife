from odoo import models, fields

class StrapiUser(models.Model):
    _name = 'strapi.user'
    _description = 'Strapi User'

    id = fields.Integer(string='ID', required=True)
    username = fields.Char(string='Username', required=True)
    email = fields.Char(string='Email', required=True)
    provider = fields.Char(string='Provider')
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
