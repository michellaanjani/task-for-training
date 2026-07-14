from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

class Inventories(models.Model):
    _name = "res.inventories.lines"
    _description = "Inventory"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', related='product_id.name', store=True, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, tracking=True)
    qty = fields.Integer(string='Qty', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    inventory_id = fields.Many2one('res.inventories', string='Inventory', required=True, tracking=True)
    
    @api.constrains('qty')
    def _check_qty(self):
        for rec in self:
            if rec.qty == 0:
                raise ValidationError(_('Qty cannot be zero'))
        
    # @api.model
    # def create(self, vals):
    #     if not vals.get('code'):
    #         vals['code'] = 'New Inventory'
    #     if vals.get('code', _('New')) == _('New'):
    #         vals['code'] = self.env['ir.sequence'].next_by_code('res.inventories') or _('New') 
    #     result = super(Inventories, self).create(vals)
    #     return result
