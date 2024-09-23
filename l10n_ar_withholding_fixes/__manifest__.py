# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Argentina - Payment Withholdings - FIXES',
    'version': "1.0",
    'description': """Allows to register withholdings during the payment of an invoice.""",
    'author': 'ADHOC SA',
    'countries': ['ar'],
    'category': 'Accounting/Localizations',
    'depends': [
        'l10n_ar_withholding',
    ],
    'data': [
    ],
    'installable': True,
    'auto_install': True,
    'post_init_hook': '_l10n_ar_withholding_post_init',
    'license': 'LGPL-3',
}
