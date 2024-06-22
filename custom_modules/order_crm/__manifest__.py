# -*- coding: utf-8 -*-
{
    'name': "order_crm",

    'summary': "order management for travel packages and services",

    'description': """
The Order Management System is a comprehensive software solution designed to streamline and automate the process of managing orders for your business. With its intuitive interface and powerful features, the system empowers your team to efficiently handle all aspects of the order lifecycle, from creation to fulfillment.
    """,
'sequence': '-100',

    'author': "Richylife",
    'website': "https://www.richylife.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'travel',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/user_view.xml',
        'views/order_view.xml',
        'data/cron_jobs.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'maintainer':'richylife,vishnu,rahul',

}

