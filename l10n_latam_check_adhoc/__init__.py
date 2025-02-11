##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from . import models
import logging
_logger = logging.getLogger(__name__)

def _pre_init_method(env):
    _logger.info('L10n Latam Check Adhoc Executing pre init method')
    env.cr.execute('''
        ALTER TABLE account_payment_method
        DROP CONSTRAINT IF EXISTS account_payment_method_name_code_unique;
    ''')
    for rec in env['account.payment.method'].search([]):
        rec.write({'code': '%s-%s' % (rec.code, 'old')})
