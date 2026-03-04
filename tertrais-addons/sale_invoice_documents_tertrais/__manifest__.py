# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale & Invoice Portal PDF Customization",
    "version": "19.0.2.0.0",
    "category": "Sales/Accounting",
    "summary": "Custom portal and PDF templates for sale orders and invoices",
    "author": "Ouiddoo",
    "website": "https://www.ouiddoo.com",
    "maintainers": ["Louis-de-Bontin"],
    "license": "AGPL-3",
    "depends": [
        "sale",
        "account",
        "portal",
        "web",
    ],
    "data": [
        # Report templates
        "report/sale_order_report_templates.xml",
        "report/invoice_report_templates.xml",
        # Portal views
        "views/portal_sale_order_templates.xml",
        # Cron jobs
        "data/cron.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
