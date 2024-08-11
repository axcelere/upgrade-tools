from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'account_withholding.view_account_journal_form',
            'account_withholding.view_account_payment_form',
            'account_withholding.view_account_tax_search',
            'account_withholding_automatic.view_account_payment_group_form',
            'account_withholding_automatic.view_account_payment_form',
            'account_withholding_automatic.view_tax_form',
            'account_withholding_automatic.res_config_settings_view_form',
        ],
        delete_childs=True
    )
    env['ir.ui.view'].search([('arch_db', 'like', 'withholding_sequence_id')]).unlink()
    env['ir.ui.view'].search([('arch_db', 'like', 'l10n_latam_use_checkbooks')]).unlink()
    return
