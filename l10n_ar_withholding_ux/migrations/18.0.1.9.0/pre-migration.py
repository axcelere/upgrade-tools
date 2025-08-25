from odoo import SUPERUSER_ID, api, tools
import logging
_logger = logging.getLogger(__name__)

def migrate(env, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    view = env.ref("stock_ux.res_config_settings_view_form", raise_if_not_found=False)
    if view:
        view.unlink()
    # Elimina todas las vistas (ir.ui.view) cuyo campo 'module' corresponde a este addon
    addon_name = 'l10n_ar_withholding_ux'
    views = env['ir.ui.view'].search([('module', '=', addon_name)])
    if views:
        logger.info(f"Eliminando {len(views)} vistas del módulo '{addon_name}'.")
        views.unlink()
    else:
        logger.info(f"No se encontraron vistas para el módulo '{addon_name}'.")
    env.cr.commit()

