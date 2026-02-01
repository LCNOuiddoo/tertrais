# -*- coding: utf-8 -*

from odoo import models, fields


class SaleSubscriptionPlan(models.Model):
    _inherit = 'sale.subscription.plan'

    draft_invoice = fields.Boolean('Draft invoice', help='Check this if you want that the invoices created with this '
                                                         'recurrence to be not automatically posted', default=False)
