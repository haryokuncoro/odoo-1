{
    'name': "custom_haryo",

    'summary': "Custom enhancements for Sale Order and Purchase Order",

    'author': "haryo kuncoro",
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'purchase', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/wizard/import_so_lines_views.xml',
    ],
    'installable': True,
    'application': False,
}

