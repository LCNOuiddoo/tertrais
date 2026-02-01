from odoo import fields, models


class PartnerTitle(models.Model):
    _name = "res.partner.title"
    _order = "name"
    _description = "Partner Title"

    name = fields.Char(string="Title", required=True, translate=True)
    shortcut = fields.Char(string="Abbreviation", translate=True)
