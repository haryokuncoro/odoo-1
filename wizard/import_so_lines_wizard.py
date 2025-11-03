from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io

class ImportSOLinesWizard(models.TransientModel):
    _name = 'import.so.lines.wizard'
    _description = 'Import SO Lines from Excel'

    file = fields.Binary(string='File (.xlsx)', required=True)
    filename = fields.Char(string='Filename')

    def action_import(self):
        if not self.file:
            raise UserError(_('Please upload a file.'))
        data = base64.b64decode(self.file)
        try:
            import openpyxl
            wb = openpyxl.load_workbook(filename=io.BytesIO(data), read_only=True)
            sheet = wb.active
        except Exception as e:
            raise UserError(_('Failed to read xlsx: %s') % e)

        # Expect headers: Product Code | Qty | Unit Price
        rows = list(sheet.iter_rows(values_only=True))
        if not rows or len(rows) < 2:
            raise UserError(_('File kosong atau header tidak ditemukan.'))
        headers = [str(c).strip().lower() for c in rows[0]]
        # get indices
        try:
            idx_prod = headers.index('product code')
            idx_qty = headers.index('qty')
            idx_price = headers.index('unit price')
        except ValueError:
            raise UserError(_('Header harus: Product Code, Qty, Unit Price'))

        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        if not sale_order:
            raise UserError(_('No active Sale Order found.'))

        product_obj = self.env['product.product']
        uom_obj = self.env['uom.uom']
        for row in rows[1:]:
            if not any(row):
                continue
            code = str(row[idx_prod]).strip() if row[idx_prod] else False
            qty = row[idx_qty] or 0
            price = row[idx_price] or 0.0
            product = product_obj.search([('default_code','=',code)], limit=1)
            if not product:
                raise UserError(_('Product with code %s not found') % code)
            sale_order.order_line.create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': product.name,
                'product_uom_qty': qty,
                'price_unit': price,
                'product_uom_id': product.uom_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}
