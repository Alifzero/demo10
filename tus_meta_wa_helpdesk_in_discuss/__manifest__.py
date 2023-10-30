{
    'name': 'Odoo Meta Whatsapp Helpdesk In Discuss',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'Helpdesk',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 19,
    'currency': 'USD',
    'summary': 'whatsapp all in one helpdesk Solutions with discuss and chat which allows user to notify to the customer for the tickets',
    'description': """
        whatsapp helpdesk bi-directional chat  will allow user to send the notifications about the customer tickets and updates and it is bi-directional.
    """,
    'depends': ['tus_meta_whatsapp_base', 'helpdesk', 'tus_meta_wa_discuss'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'tus_meta_wa_helpdesk_in_discuss/static/src/js/HelpdeskList.js',
            'tus_meta_wa_helpdesk_in_discuss/static/src/js/wa_thread_view.js',
            'tus_meta_wa_helpdesk_in_discuss/static/src/xml/HelpdeskList.xml',
            'tus_meta_wa_helpdesk_in_discuss/static/src/xml/wa_thread_view.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
