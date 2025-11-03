from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    request_vendor_id = fields.Many2one('res.partner', string='Request Vendor')
    no_kontrak = fields.Char(string='No Kontrak')
    with_po = fields.Boolean(string='With PO', default=False)
    purchase_order_ids = fields.One2many('purchase.order', 'origin_sale_id', string='Purchase Orders')

    # override confirm to validate no_kontrak uniqueness
    def action_confirm(self):
        for order in self:
            if order.no_kontrak:
                found = self.env['sale.order'].search([
                    ('no_kontrak','=', order.no_kontrak),
                    ('id','!=', order.id)
                ], limit=1)
                if found:
                    raise ValidationError(_('No Kontrak sudah pernah diinputkan sebelumnya…!'))
        return super(SaleOrder, self).action_confirm()

    # method create PO from SO
    def action_create_po_from_so(self):
        PurchaseOrder = self.env['purchase.order']
        for order in self:
            if not order.with_po:
                raise ValidationError(_('Field With PO harus dicentang agar bisa membuat PO.'))
            if not order.request_vendor_id:
                raise ValidationError(_('Request Vendor harus diisi sebelum membuat PO.'))

            po_vals = {
                'partner_id': order.request_vendor_id.id,
                'origin': order.name,
                'partner_ref': order.name,
                'origin_sale_id': order.id,
            }

            po = PurchaseOrder.create(po_vals)

            for line in order.order_line:
                self.env['purchase.order.line'].create({
                    'order_id': po.id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'product_uom_id': line.product_uom_id.id,
                })

            order.write({'purchase_order_ids': [(4, po.id)]})

        return True

    # method to open import SO lines wizard
    def open_import_so_lines_wizard(self):
        return {
            'name': 'Import SO Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'import.so.lines.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_filename': 'template_import.xlsx', 'active_id': self.id},
        }

# Inherit Purchase Order to add link back to Sale Order
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin_sale_id = fields.Many2one('sale.order', string='Source Sale Order')
