from odoo import api, fields, models
import requests
from PIL import Image
from io import BytesIO
import base64


class ProductTemplate(models.Model):
    _inherit = "product.template"

    server_id = fields.Integer(string="System ID")
    description = fields.Text(string="Description")
    destination_name = fields.Char(string="Destination")
    image = fields.Binary(string="Image")
    fuel = fields.Char(string="Fuel Type")
    seat = fields.Char(string="Seats")
    speed = fields.Char(string="Top Speed")
    engine = fields.Char(string="Engine")
    transmission = fields.Char(string="Transmission")
    perdaylimit = fields.Char(string="Per Day Limit")
    cylinder = fields.Char(string="Cylinders")
    deposit = fields.Float(string="Deposit")
    body = fields.Char(string="Body Type")
    service_name = fields.Char(string="Service")
    service_slug = fields.Char(string="Slug")
    service_dec = fields.Char(string="Description")
    city_name = fields.Char(string="City")
    slug = fields.Char(string="Slug")

    def fetch_product_template(self):
        url = 'https://clarity.richylife.ae/api/products?populate=*'
        token = "a20427239689acf3bd60e94c32b134d307689a42c9bd4437c8438e65d23378a4c3fa47417c4ffe0b1b652e4537547e01a6148d065d5b6a04d2e5d734d445499b87033897d24001f4badb9a8cfba4e39a8c6e79781bae7e86649f61bd65db66cb03001e8e6266998ce3fa4f19a205141354295749e9b5974281cab26444b82c7a"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for item in data:
                # product_data = item['attributes']
                destination_name = None
                if item['destination']:
                    destination_data = item['destination']
                    destination_name = destination_data.get('name')

                image_binary = None
                if item['image']:
                    image_data = item['image'][0]
                    image_url = image_data.get('url')
                    if image_url:
                        try:
                            image_response = requests.get(image_url)
                            image_response.raise_for_status()
                            image = Image.open(BytesIO(image_response.content))
                            buffered = BytesIO()
                            image.save(buffered, format=image.format)
                            image_binary = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        except (requests.exceptions.RequestException, Image.UnidentifiedImageError) as image_error:
                            print(f"Error processing image URL {image_url}: {image_error}")

                details_data = None

                if item['details']:
                    details_data = item['details'][0]
                service_name = None
                service_data = None
                if item['service']:
                    service_data = item['service']
                    service_name = service_data.get('name')
                city_name = None
                if item['city']:
                    city_data = item['city']
                    city_name = city_data.get('city')

                vals = {
                    'server_id': details_data.get('id') if details_data else False,
                    'name': item['name'],
                    'description': item['description'],
                    'list_price': item['price'],
                    'slug': item['slug'],
                    'destination_name': destination_name,
                    'image': image_binary,
                    'image_1920': image_binary,
                    'fuel': details_data.get('fuel') if details_data else False,
                    'seat': details_data.get('seat') if details_data else False,
                    'speed': details_data.get('speed') if details_data else False,
                    'engine': details_data.get('engine') if details_data else False,
                    'transmission': details_data.get('transmission') if details_data else False,
                    'perdaylimit': details_data.get('perdaylimit') if details_data else False,
                    'cylinder': details_data.get('cylinder') if details_data else False,
                    'deposit': details_data.get('deposit') if details_data else False,
                    'body': details_data.get('body') if details_data else False,
                    'service_name': service_name,
                    'service_slug': service_data.get('name') if service_data else False,
                    'service_dec': service_data.get('description') if service_data else False,
                    'city_name': city_name,
                }

                if details_data :
                    product = self.search([('server_id', '=', details_data.get('id'))])
                    if product:
                        product.write(vals)
                    else:
                        product = self.create(vals)
                else:
                    product = self.create(vals)
                print(f"Product {product.name} processed with ID {product.id}")

        except requests.exceptions.RequestException as e:
            print('Error:', e)
