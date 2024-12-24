from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    for rec in env['account.payment.method'].search([]):
        rec.write({'code': '%s-%s' % (rec.name, 'old')})
