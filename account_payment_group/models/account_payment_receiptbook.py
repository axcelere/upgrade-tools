##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class AccountPaymentReceiptbook(models.Model):

    _name = 'account.payment.receiptbook'
    _description = 'Account payment Receiptbook'
    # analogo a account.journal.document.type pero para pagos
    _order = 'sequence asc'

    report_partner_id = fields.Many2one(
        'res.partner',
    )
    mail_template_id = fields.Many2one(
        'mail.template',
        'Email Template',
        domain=[('model', '=', 'account.payment.group')],
        help="If set an email will be sent to the customer when the related"
        " account.payment.group has been posted.",
    )
    sequence = fields.Integer(
        'Sequence',
        help="Used to order the receiptbooks",
        default=10,
    )
    name = fields.Char(
        'Name',
        size=64,
        required=True,
        index=True,
    )
    partner_type = fields.Selection(
        [('customer', 'Customer'), ('supplier', 'Vendor')],
        required=True,
        index=True,
    )