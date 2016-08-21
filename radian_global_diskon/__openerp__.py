# -*- coding: utf-8 -*-
{
    'name': "Global Diskon",

    'summary': """
        Diskon tambahan sebelum PPN""",

    'description': """
        Penambahan Diskon secara rupiah dan tidak tergantung item barang
    """,

    'author': "Radian Delta",
    'website': "http://www.radiandelta.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2016-02-22.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}