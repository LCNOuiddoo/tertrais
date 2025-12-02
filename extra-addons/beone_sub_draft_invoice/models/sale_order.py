# -*- coding: utf-8 -*-

import logging

from odoo import api, models, fields
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    have_draft_invoice = fields.Boolean('Have a draft invoice', compute='_compute_have_draft_invoice',
                                        help='The subscription have currently a draft invoice', store=True)

    @api.depends('invoice_ids.state')
    def _compute_have_draft_invoice(self):
        for record in self:
            record.have_draft_invoice = False
            for invoice in record.invoice_ids:
                if invoice.state == 'draft':
                    record.have_draft_invoice = True
                    continue


from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _recurring_invoice_get_subscriptions(self, grouped=False, batch_size=30):
        """
        Odoo 19 standard + filtre pour exclure les abonnements ayant une facture en brouillon
        quand la méthode est appelée sur un recordset (self truthy).

        - Si self est vide (cas cron) : on laisse 100 % la logique standard,
          qui utilise déjà notre _recurring_invoice_domain() surchargé.
        - Si self est non vide : on appelle super(), puis on filtre les résultats
          pour enlever les souscriptions avec have_draft_invoice = True.
        """
        all_subscriptions, need_cron_trigger = super(
            SaleOrder, self
        )._recurring_invoice_get_subscriptions(
            grouped=grouped,
            batch_size=batch_size,
        )

        # Si self est vide : on ne touche à rien, le domaine a déjà été filtré en amont.
        if not self:
            return all_subscriptions, need_cron_trigger

        # Si self est défini : on applique juste notre logique de draft.
        if grouped:
            # all_subscriptions est une liste de recordsets groupés
            cleaned_groups = []
            for subs in all_subscriptions:
                subs_no_draft = subs.filtered(lambda s: not s.have_draft_invoice)
                if subs_no_draft:
                    cleaned_groups.append(subs_no_draft)
            all_subscriptions = cleaned_groups
        else:
            # all_subscriptions est un recordset simple
            all_subscriptions = all_subscriptions.filtered(
                lambda s: not s.have_draft_invoice
            )

        return all_subscriptions, need_cron_trigger

    def _recurring_invoice_domain(self, extra_domain=None):
        my_extra_domain = [
            ('is_invoice_cron', '=', False),
            ('have_draft_invoice', '=', False),
        ]
        if extra_domain:
            my_extra_domain = expression.AND([my_extra_domain, extra_domain])
        return super(SaleOrder, self)._recurring_invoice_domain(
            extra_domain=my_extra_domain
        )

    def _process_auto_invoice(self, invoice):
        """Hook for extension, to support different invoice states."""
        if self.plan_id.draft_invoice:
            self.with_context(mail_notrack=True).write({'payment_exception': False})
            self.env.cr.commit()
        else:
            super(SaleOrder, self)._process_auto_invoice(invoice)
