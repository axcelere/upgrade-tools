##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class AccountPaymentReceiptbook(models.Model):

    _inherit = 'account.payment.receiptbook'

    document_type_id = fields.Many2one(
        'l10n_latam.document.type',
        'Document Type',
        required=True,
    )

    def dummy_method(self):
        return True
