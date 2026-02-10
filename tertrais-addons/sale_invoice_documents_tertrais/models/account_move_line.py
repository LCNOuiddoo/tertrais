# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def get_section_subtotal(self, field='price_subtotal'):
        section_lines = self._get_section_lines()
        return sum(section_lines.mapped(field))
