import logging

_logger = logging.getLogger(__name__)

from odoo import models, api


class FixCheck(models.Model):
    _inherit = "l10n_latam.check"

    @api.model
    def fix_checks_ofupgrade_15(self):
        AccountPayment = self.env['account.payment'].sudo()
        Check = self.env['l10n_latam.check'].sudo()
        self.env.cr.execute(
            """SELECT account_payment.id FROM account_payment, account_payment_method WHERE account_payment.payment_type = 'inbound' AND check_number_moved0 <> 0 and account_payment.payment_method_id = account_payment_method.id AND account_payment_method.code = 'new_third_party_checks'""",
        )
        ids = self.env.cr.fetchall()
        old_checks = AccountPayment.browse([x[0] for x in ids])
        for old_check in old_checks:
            Check.create({
                'name': old_check.name,
                'amount': old_check.amount,
                'payment_id': old_check.id,
                'payment_date': old_check.date,
            })

        # CHEQUES PROPIOS
        self.env.cr.execute(
            """SELECT account_payment.id FROM account_payment, account_payment_method WHERE check_number_moved0 <> 0 and account_payment.payment_method_id = account_payment_method.id AND account_payment_method.code = 'check_printing'""",
        )
        ids = self.env.cr.fetchall()
        old_checks = AccountPayment.browse([x[0] for x in ids])
        for old_check in old_checks:
            Check.create({
                'name': old_check.name,
                'amount': old_check.amount,
                'payment_id': old_check.id,
                'payment_date': old_check.date,
            })
        return True
