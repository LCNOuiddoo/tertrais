from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def _get_display_name_without_code(self):
        """Return line name without the product default_code prefix for portal/report."""
        self.ensure_one()
        name = self.name or ""
        if not self.product_id:
            return name
        code = self.product_id.default_code
        prefix = f"[{code}] "
        return name.replace(prefix, "")
