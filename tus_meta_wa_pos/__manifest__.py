{
    'name': 'Odoo Meta Whatsapp POS',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'Point of Sale',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 19,
    'currency': 'USD',
    'summary': 'Whatsapp POS point of sale modules allows to send the receipt by whatsapp',
    'description': """
        whatsapp all in one and whatsapp pos will allow user to send the orders of point of sale to customer and customer can rate that.
    """,
    'depends': ['tus_meta_whatsapp_base', 'point_of_sale'],
    'data': [
        'security/pos_security.xml',
        'data/wa_template.xml',
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'tus_meta_wa_pos/static/src/js/**/*.js',
            ('after', 'point_of_sale/static/src/scss/pos.scss', 'tus_meta_wa_pos/static/src/scss/pos_ext.scss'),
            'tus_meta_wa_pos/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
