{
    'name': 'Odoo Meta Whatsapp Invoice',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'Accounting',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 19,
    'currency': 'USD',
    'summary': 'whatsapp invoice all in one invoicing Solutions which allows user to notify to the customer for the invoices and payment',
    'description': """
        whatsapp invoice whatsapp all in one solutions will allow user to send the notifications about the customer invoices and updates.
    """,
    'depends': ['tus_meta_whatsapp_base', 'account'],
    'data': [
        'security/invoice_security.xml',
        'data/wa_template.xml',
        'views/account_move.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
