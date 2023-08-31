# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
import logging
import re
from collections import defaultdict, OrderedDict
import warnings

_logger = logging.getLogger(__name__)

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _message_post_after_hook(self, message, msg_vals):
        # if self.partner_email and self.partner_id and not self.partner_id.email:
        #     self.partner_id.email = self.partner_email
        #
        # if self.partner_email and not self.partner_id:
        #     # we consider that posting a message with a specified recipient (not a follower, a specific one)
        #     # on a document without customer means that it was created through the chatter using
        #     # suggested recipients. This heuristic allows to avoid ugly hacks in JS.
        #     new_partner = message.partner_ids.filtered(lambda partner: partner.email == self.partner_email)
        #     if new_partner:
        #         self.search([
        #             ('partner_id', '=', False),
        #             ('partner_email', '=', new_partner.email),
        #             ('stage_id.fold', '=', False)]).write({'partner_id': new_partner.id})
        # # use the sanitized body of the email from the message thread to populate the ticket's description
        # if not self.description and message.subtype_id == self._creation_subtype() and self.partner_id == message.author_id:
        #     self.description = message.body
        res= super(HelpdeskTicket, self)._message_post_after_hook(message, msg_vals)
        self.description=''
        return res