import logging

_logger = logging.getLogger(__name__)

from odoo import models, api
from datetime import datetime


class FixCheck(models.Model):
    _inherit = "l10n_latam.check"

    @api.model
    def fix_third_checks_ofupgrade_15_from_ids(self, ids_dict={}):
        if not ids_dict:
            return False
        Check = self.env['l10n_latam.check'].sudo()
        Payment = self.env['account.payment'].sudo()
        ids = ids_dict.keys()
        for old_check in Payment.browse(ids):
            try:
                dict_key = ids_dict.get(old_check.id, [False, "", False])
                new_check = Check.create({
                    'name': dict_key[1],
                    'bank_id': dict_key[0],
                    'amount': old_check.amount,
                    'payment_id': old_check.id,
                    'payment_date': old_check.date,
                    'current_journal_id': dict_key[2],
                    'company_id': old_check.company_id.id,
                })
                new_check.write({'current_journal_id': dict_key[2]})
            except Exception as e:
                _logger.error("Error creating check for payment %s: %s", old_check, e)
        return True

    @api.model
    def update_payment_date_third_checks_ofupgrade_15_from_ids(self, ids_dict={}):
        if not ids_dict:
            return False
        Check = self.env['l10n_latam.check'].sudo()
        Payment = self.env['account.payment'].sudo()
        ids = ids_dict.keys()
        for id in ids:
            try:
                with self.env.cr.savepoint():
                    check = Check.search([('payment_id', '=', id)], limit=1)
                    payment_date = ids_dict.get(id, check.payment_date)
                    if isinstance(payment_date, str):
                        # Convierte solo si es string en formato 'dd/mm/yyyy'
                        payment_date = datetime.strptime(payment_date, '%d/%m/%Y').strftime('%Y-%m-%d')
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                    check.write({'payment_date': payment_date})
            except Exception as e:
                _logger.error("Error updating date of check %s: %s", check, e)
        return True

    @api.model
    def fix_cheques_propios_ofupgrade_15_from_ids(self, ids_dict={}):
        if not ids_dict:
            return False
        Check = self.env['l10n_latam.check'].sudo()
        Payment = self.env['account.payment'].sudo()
        ids = ids_dict.keys()
        for old_check in Payment.browse(ids):
            try:
                dict_key = ids_dict.get(old_check.id, [False, "", False])
                liquidity_line = old_check._seek_for_lines()[0]
                with self.env.cr.savepoint():
                    new_check = Check.create({
                        'name': dict_key[1],
                        'bank_id': dict_key[0],
                        'amount': old_check.amount,
                        'payment_id': old_check.id,
                        'payment_date': old_check.date,
                        'current_journal_id': dict_key[2],
                        'company_id': old_check.company_id.id,
                        'outstanding_line_id': liquidity_line.id,
                    })
                    new_check.write({'current_journal_id': dict_key[2]})
            except Exception as e:
                _logger.error("Error creating check for payment %s: %s", old_check, e)
        return True

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
