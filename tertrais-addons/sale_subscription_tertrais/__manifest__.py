# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Subscription Tertrais",
    "version": "16.0.1",
    'category': 'sale',
    "summary": "This module allows you to  ***",
    "author": "Ouiddoo",
    "license": "AGPL-3",
    "depends": ["sale_subscription","sale_project","account"],

    "data": [
             "views/sale_order_views.xml",
             "views/account_invoice.xml",
             ],
    "installable": True,

    # 'assets': {
    #     'web.assets_backend': [
    #
    #         'sale_subscription_tertrais/static/src/css/section_note_view.scss',
    #     ],

    #},
}
