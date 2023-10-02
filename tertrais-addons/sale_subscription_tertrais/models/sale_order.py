# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
import logging
import re
from collections import defaultdict, OrderedDict
import warnings

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def start_subscription(self):
        self.start_date = fields.Date.today()
        self.next_invoice_date = fields.Date.today()
        return True

    def _confirm_subscription(self):
        sub_to_skip = []
        for sub in self:
            if sub.start_date:
                sub_to_skip.append(sub.id)
        super()._confirm_subscription()
        for sub in self:
            if sub.id not in sub_to_skip:
                sub.start_date = False
                sub.next_invoice_date = False
