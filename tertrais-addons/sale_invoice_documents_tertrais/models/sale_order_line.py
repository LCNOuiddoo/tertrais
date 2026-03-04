from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'linked_line_id', 'linked_line_ids')
    def _compute_name(self):
        res = super()._compute_name()
        for line in self:
            line.name = line.name.replace(f"[{line.product_id.default_code}] ", "")

    @api.model
    def _cron_cleanup_sale_order_line_names(self, batch_size=1000):
        """One-off cleanup to remove product default_code prefixes from existing SOL names.

        Intended to be called by a (manual) cron and to process the table in batches
        to avoid long-running transactions on large databases.
        """
        last_id = 0
        model = self.env['sale.order.line']

        while True:
            lines = model.search(
                [
                    ('id', '>', last_id),
                    ('product_id.default_code', '!=', False),
                ],
                order='id',
                limit=batch_size,
            )
            if not lines:
                break

            for line in lines:
                name = line.name or ""
                code = line.product_id.default_code
                if not code:
                    continue
                prefix = f"[{code}] "
                if prefix in name:
                    line.name = name.replace(prefix, "")

            # Commit after each batch to keep transactions short on large datasets
            self.env.cr.commit()
            last_id = lines[-1].id

        _logger.info("Completed cleanup of sale.order.line names.")
