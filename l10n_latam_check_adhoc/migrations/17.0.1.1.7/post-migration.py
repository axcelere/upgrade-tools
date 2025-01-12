from openupgradelib import openupgrade
from odoo import fields



@openupgrade.migrate()
def migrate(env, version):
    for rec in env['account.payment.method'].search([]):
        value = 'old %s' % str(fields.Datetime.now())
        rec.write({'code': '%s-%s' % (rec.code, value)})
