from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Inventories(models.Model):
    _name = "res.inventories.lines"
    _description = "Inventory"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', related='product_id.display_name', store=True, readonly=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, index=True, tracking=True)
    qty = fields.Integer(string='Qty', required=True, default=1, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    inventory_id = fields.Many2one('res.inventories', string='Inventory', required=True, ondelete='cascade', index=True, tracking=True)
    
    _sql_constraints = [
        ("uniq_inventory_product", "unique(inventory_id, product_id)",
         "Product already exists in this inventory."),
    ]
    
    @api.constrains('qty')
    def _check_qty(self):
        for rec in self:
            if rec.qty <= 0:
                raise ValidationError(_('Qty must be greater than zero'))
        
