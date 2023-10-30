{
    'name': 'Odoo Meta Whatsapp Helpdesk',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'Helpdesk',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 19,
    'currency': 'USD',
    'summary': 'whatsapp all in one helpdesk Solutions which allows user to notify to the customer for the tickets',
    'description': """
        whatsapp helpdesk will allow user to send the notifications about the customer tickets and updates and it is bi-directional.
    """,
    'depends': ['tus_meta_whatsapp_base', 'helpdesk'],
    'data': [
        'data/wa_template.xml',
        'security/helpdesk_security.xml',
        'views/helpdesk_ticket.xml'
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
