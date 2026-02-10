from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    title = fields.Many2one('res.partner.title')
