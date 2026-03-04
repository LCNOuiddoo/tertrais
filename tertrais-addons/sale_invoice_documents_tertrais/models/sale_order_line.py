from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'linked_line_id', 'linked_line_ids')
    def _compute_name(self):
        res = super()._compute_name()
        for line in self:
            line.name = line.name.replace(f"[{line.product_id.default_code}] ", "")
