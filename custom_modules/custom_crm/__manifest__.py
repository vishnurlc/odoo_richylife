# -*- coding: utf-8 -*-
{
    'name': "custom_crm",

    'summary': "Odoo richylife crm customisation",

    'author': "Ridhin",
    'category': 'Uncategorized',
    'version': '17.0',
    'depends': ['base','product','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/cron_fetch_customer.xml',
        'views/res_partner_view.xml',
        'views/product_template_view.xml'
    ],
}

