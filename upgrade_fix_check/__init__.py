import logging

_logger = logging.getLogger(__name__)

from odoo import models, api


class FixCheck(models.Model):
    _inherit = "l10n_latam.check"

    @api.model
    def fix_checks_ofupgrade_15(self):
        AccountPayment = self.env['account.payment'].sudo()
        Check = self.env['l10n_latam.check'].sudo()
        # select COUNT(*) from account_payment where journal_id IN (22,15) and check_number_moved0 <> '0' AND payment_type = 'inbound';
        self.env.cr.execute(
            """SELECT
    p.id
FROM
    account_payment p,
    account_payment_method_line pml,
    account_payment_method pm
WHERE
    p.journal_id IN (22, 15)
    AND (p.check_number_moved0 IS NOT NULL OR p.check_number_moved0 <> '0')
    AND p.payment_type = 'inbound'
    AND p.payment_method_line_id = pml.id
    AND pml.payment_method_id = pm.id
""",
        )
        ids = self.env.cr.fetchall()
        old_checks = AccountPayment.browse([x[0] for x in ids])
        for old_check in old_checks:
            query = """select check_number_moved0 from account_payment where id = %s""" % (old_check.id, )
            Check.create({
                'name': old_check.check_number,
                'amount': old_check.amount,
                'payment_id': old_check.id,
                'payment_date': old_check.date,
            })

        # CHEQUES PROPIOS
        self.env.cr.execute(
            """SELECT
    p.id
FROM
    account_payment p,
    account_payment_method_line pml,
    account_payment_method pm
WHERE
    (p.check_number_moved0 IS NOT NULL OR p.check_number_moved0 <> '0')
    AND p.payment_type = 'outbound'
    AND p.payment_method_line_id = pml.id
    AND pml.payment_method_id = pm.id AND pm.code='check_printing';""",
        )
        ids = self.env.cr.fetchall()
        old_checks = AccountPayment.browse([x[0] for x in ids])
        for old_check in old_checks:
            liquidity_line = old_check._seek_for_lines()[0]
            Check.create({
                'name': old_check.check_number,
                'amount': old_check.amount,
                'payment_id': old_check.id,
                'payment_date': old_check.date,
                'outstanding_line_id': liquidity_line.id,
            })
        return True
