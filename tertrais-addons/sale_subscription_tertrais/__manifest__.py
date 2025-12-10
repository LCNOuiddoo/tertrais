# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Subscription Tertrais",
    "version": "19.0.1",
    "category": "sale",
    "summary": "This module allows you to fix odoo sale_subscription bug",
    "author": "Ouiddoo",
    "website": "https://www.ouiddoo.com",
    "maintainers": ["Louis-de-Bontin"],
    "license": "AGPL-3",
    "depends": [
        "sale_subscription",
        "sale_project",
        "account",
        "accountant",
        "partner_title",
    ],
    "data": [
        # "views/sale_order_views.xml",
        # "views/account_invoice.xml",
    ],
    "installable": True,
}
