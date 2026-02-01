# -*- coding: utf-8 -*-
{
    'name': "BEONE Subscription Draft Invoices",

    'summary': """
        Give back the ability to push subscription invoices in draft instead of posting them on Odoo 19
        """,

    'description': """
        Adding a check box to the subscription plan item that allow you to specify that you want the invoices on that specific plan to be created in draft instead of posted
        """,

    'author': "Edwin BRASSEUR",
    'website': "http://www.beone.be",

    'category': 'Sales/Subscriptions',
    "version": "19.0.1.0.0",
    'license': 'OPL-1',

    'price': 50.00,
    'currency': 'EUR',

    'depends': ['base', 'sale_subscription'],

    'images': ['static/description/banner.gif'],

    'data': [
        'views/sale_subscription_plan_view_form.xml',
    ],
}
