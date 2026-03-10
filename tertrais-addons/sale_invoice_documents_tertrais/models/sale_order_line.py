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
        return res

    def _get_display_name_without_code(self):
        """Return line name without the product default_code prefix for portal/report."""
        self.ensure_one()
        name = self.name or ""
        if not self.product_id:
            return name
        code = self.product_id.default_code
        if not code:
            return name
        prefix = f"[{code}] "
        return name.replace(prefix, "")

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

    @api.model
    def _cron_unlock_cleanup_relock_sale_order_lines(self, batch_size=1000):
        """Temporarily unlock locked orders, clean up line names, then re-lock them.

        This is intended as a one-off maintenance job. It:
        1) remembers which sale orders were locked,
        2) unlocks only those orders via SQL,
        3) runs the batch cleanup on all lines,
        4) re-locks only the orders that were initially locked.
        """
        cr = self.env.cr

        # 1) Remember which orders are locked right now
        self.env.cr.execute("SELECT id FROM sale_order WHERE locked = TRUE")
        locked_ids = [row[0] for row in self.env.cr.fetchall()]

        # 2) Unlock them in SQL
        if locked_ids:
            cr.execute("UPDATE sale_order SET locked = FALSE WHERE id = ANY(%s)", [locked_ids])
            cr.commit()

        try:
            # 3) Run existing cleanup (now allowed to touch lines of previously locked orders)
            self._cron_cleanup_sale_order_line_names(batch_size=batch_size)
        finally:
            # 4) Re-lock only the orders that were initially locked
            if locked_ids:
                cr.execute("UPDATE sale_order SET locked = TRUE WHERE id = ANY(%s)", [locked_ids])
                cr.commit()

        _logger.info(
            "Unlock/cleanup/relock of sale orders completed (processed %s initially locked orders).",
            len(locked_ids),
        )
