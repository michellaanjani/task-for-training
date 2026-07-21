# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Warehouse Management',
    'version' : '1.0.0.3',
    'summary': 'Warehouse management Software',
    'sequence': 10,
    'description': """Warehouse Management Software""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/productivity',
    'depends' : ['base','mail','product'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/warehouse_view.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}