from odoo import fields, models, api, _
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class L10nLatamCheckbook(models.Model):

    _name = 'l10n_latam.checkbook'
    _description = 'Checkbook'
    _rec_name = 'range_to'

    sequence_id = fields.Many2one(
        'ir.sequence', 'Sequence', copy=False, domain=[('code', '=', 'own_check')], help="Checks numbering sequence.")
    next_number = fields.Integer(related='sequence_id.number_next_actual', related_sudo=True, readonly=False)
    type = fields.Selection(
        [('deferred', 'Deferred'), ('currents', 'Currents'), ('electronic', 'Electronic')],
        string='Check type', required=True, default='deferred')
    journal_id = fields.Many2one(
        'account.journal', 'Journal', readonly=True, required=True, ondelete='cascade',)
    range_to = fields.Integer(
        'To Number',
    )
    active = fields.Boolean(default=True)
