from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

class WarehousesInventory(models.Model):
    _name = "res.inventories"
    _description = "Inventory"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code desc'
    
    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('on_progress', 'On Progress'),
        ('loaded', 'Loaded'),
        ('cancel', 'Cancelled'), ],
        string='Status', default='draft', tracking=True)
    inventories_lines_ids = fields.One2many('res.inventories.lines', 'inventory_id', string='Inventory Lines')

    def action_confirm(self):
        self.state = 'on_progress'
        
    def action_done(self):
        self.state = 'loaded'
        
    def action_draft(self):
        self.state = 'draft'  
        
    def action_cancel(self):
        self.state = 'cancel'
        
    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = 'New Inventory'
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('res.inventories') or _('New') 
        result = super(WarehousesInventory, self).create(vals)
        return result
    
    # @api.model
    # def default_get(self, fields):
    #     result = super(WarehousesInventory, self).default_get(fields)
    #     print("value result", result)
    #     result['gender'] = 'female'
    #     return result
    
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            inventories = self.env['res.inventories'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if inventories:
                raise ValidationError(_('Name %s Already Exists' %rec.name))

            
    # def name_get(self):
    #     result = []
    #     print("context is", self.env.context)
    #     for rec in self:
    #         if self.env.context.get('hide_code'):
    #             name = rec.name
    #         else:
    #             name = '[' + rec.reference + '] ' + rec.name 
    #         result.append((rec.id, name))
    #     return result
    