# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class AccountPaymentGroup(models.Model):
    _name = "account.payment.group"
    _description = "Payment Group"

    name = fields.Char(string='Number', readonly=True, copy=False)
