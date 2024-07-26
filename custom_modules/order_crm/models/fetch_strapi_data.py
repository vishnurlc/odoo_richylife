import requests
from odoo import api, models
from datetime import datetime

class FetchStrapiData(models.AbstractModel):
    _name = 'fetch.strapi.data'
    _description = 'Strapi fetch'

    @api.model
    def fetch_strapi_data(self):
        user_response = requests.get('https://clarity.richylife.ae/api/users')
        print('pppppppppppppppp',user_response)
        # order_response = requests.get('http://localhost:1337/api/orders?populate=*')

        if user_response.status_code == 200:
            users = user_response.json()
            # orders = order_response.json()
            print(users)

            for user in users:
                existing_user = self.env['strapi.user'].search([('email', '=', user['email'])], limit=1)

                user_data = {
                    'rootid': user.get('id'),
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'provider': user.get('provider'),
                    'verified' : user.get('Profile', {}).get('verified'),
                    'confirmed': user.get('confirmed'),
                    'blocked': user.get('blocked'),
                    'created_at': user.get('createdAt'),
                    'updated_at': user.get('updatedAt'),
                    'invitee_id': user.get('invitee_id'),
                    'referral_id': user.get('referralId'),
                    'referrallink': user.get('referrallink'),
                    'usertype': user.get('usertype'),
                    'bio': user.get('bio'),
                    'language': user.get('language'),
                    'currency': user.get('currency'),
                    'userid': user.get('userid'),
                    'name': user.get('name'),
                    'phone': user.get('phone'),
                    'surname': user.get('surname'),
                    'date_of_birth': user.get('date_of_birth'),
                    'nationality': user.get('nationality'),
                }

                if existing_user:
                    existing_user.write(user_data)
                else:
                    self.env['strapi.user'].create(user_data)

            # for order in orders:
            #     user = self.env['strapi.user'].search([('email', '=', order['user']['email'])])
            #     print(user)
            #     if user:
            #         self.env['strapi.order'].create({
            #             'user_id': user.id,
            #             'order_details': order['details'],
            #         })
