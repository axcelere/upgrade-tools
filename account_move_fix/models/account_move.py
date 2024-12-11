# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, Command, SUPERUSER_ID, modules, tools
from odoo.tools import (
    index_exists
)

class AccountMove(models.Model):
    _inherit = "account.move"
    
    def _auto_init(self):
        if not index_exists(self.env.cr, 'account_move_to_check_idx'):
            self.env.cr.execute("""
                CREATE INDEX account_move_to_check_idx
                          ON account_move(journal_id)
                       WHERE to_check = true
            """)
        if not index_exists(self.env.cr, 'account_move_payment_idx'):
            self.env.cr.execute("""
                CREATE INDEX account_move_payment_idx
                          ON account_move(journal_id, state, payment_state, move_type, date)
            """)
        # if not index_exists(self.env.cr, 'account_move_unique_name'):
        #     self.env.cr.execute("""
        #         CREATE UNIQUE INDEX account_move_unique_name
        #                          ON account_move(name, journal_id)
        #                       WHERE (state = 'posted' AND name != '/')
        #     """)
        if not index_exists(self.env.cr, 'account_move_sequence_index3'):
            # Used for gap detection in list views
            self.env.cr.execute("""
                CREATE INDEX account_move_sequence_index3
                          ON account_move (journal_id, sequence_prefix desc, (sequence_number+1) desc)
            """)