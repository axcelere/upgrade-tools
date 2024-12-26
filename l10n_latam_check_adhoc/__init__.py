##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from . import models

def _pre_init_method(env):
    for rec in env['account.payment.method'].search([]):
        rec.write({'code': '%s-%s' % (rec.code, 'old')})
