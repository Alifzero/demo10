{
    'name': 'Odoo Meta Whatsapp Sale',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'Sales',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 19,
    'currency': 'USD',
    'summary': 'Whatsapp sales modules allows to send the quotation and sales order by whatsapp message',
    'description': """
        whatsapp all in one and whatsapp sales module will allow user to send the quotation and sales order customer and customer.
    """,
    'depends': ['tus_meta_whatsapp_base', 'sale_management'],
    'data': [
        'security/sale_security.xml',
        'data/wa_template.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
