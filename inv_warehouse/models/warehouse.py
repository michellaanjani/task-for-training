from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class WarehousesInventory(models.Model):
    _name = "res.inventories"
    _description = "Inventory"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _order = 'code desc'
    
    name = fields.Char(string='Name', default=lambda self: _("New"), copy=False, readonly=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('on_progress', 'On Progress'),
        ('loaded', 'Loaded'),
        ('cancel', 'Cancelled'), ],
        string='Status', default='draft', tracking=True, required=True, copy=False)
    inventories_lines_ids = fields.One2many('res.inventories.lines', 'inventory_id', string='Inventory Lines')

    _sql_constraints = [
        ("uniq_inventory_name", "unique(name)", "Inventory name already exists."),
        ("uniq_inventory_code", "unique(code)", "Inventory code already exists."),
    ]
    
    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = seq.next_by_code("res.inventories.name") or _("New")
        return super().create(vals_list)
    
    def _set_inventory_line_names(self):
        if not self.name or self.name == _("New"):
            raise UserError(_("Inventory sequence pada field Name belum terisi."))

        clicked_dt = fields.Datetime.context_timestamp(self, fields.Datetime.now())
        clicked_dt_str = clicked_dt.strftime('%d%m%Y %H:%M')

        for line in self.inventories_lines_ids:
            product_name = line.product_id.name or ''
            line.name = '%s - %s - %s' % (product_name, self.name, clicked_dt_str)
    
    def action_confirm(self):
        self.ensure_one()
        self._set_inventory_line_names()
        self.state = 'on_progress'
        
    def action_done(self):
        self.ensure_one()
        self.state = 'loaded'
        
    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'  
        
    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancel'    