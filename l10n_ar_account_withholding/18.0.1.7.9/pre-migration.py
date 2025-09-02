from odoo import SUPERUSER_ID, api, tools
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Eliminar cualquier vista que tenga el campo regimenes_ganancias_ids en su definición arch
    IrUiView = env['ir.ui.view']
    views_with_regimenes_ganancias = IrUiView.search([
        ('arch_db', 'ilike', 'regimenes_ganancias_ids')
    ])
    for view in views_with_regimenes_ganancias:
        _logger.info(f"Eliminando vista {view.xml_id or view.id} que contiene 'regimenes_ganancias_ids'")
        view.unlink()

    env.cr.commit()
