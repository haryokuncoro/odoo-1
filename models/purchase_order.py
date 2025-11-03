from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin_sale_id = fields.Many2one('sale.order', string='Related Sale Order', ondelete='set null')
