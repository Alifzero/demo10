{
    'name': 'Odoo Meta Whatsapp CRM In Discuss',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'CRM',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 19,
    'currency': 'USD',
    'summary': 'whatsapp crm discuss allows user to send the quotation directly to the customer or leads from the discuss module, it solves the communication gap between the systems.',
    'description': """
Whatsapp crm discuss is the chat platform all in one is used for sending the details of products directly to the customer by single click
    """,
    'depends': ['tus_meta_whatsapp_base', 'crm', 'tus_meta_wa_discuss'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'tus_meta_wa_crm_in_discuss/static/src/js/LeadList.js',
            'tus_meta_wa_crm_in_discuss/static/src/js/wa_thread_view.js',
            'tus_meta_wa_crm_in_discuss/static/src/xml/LeadList.xml',
            'tus_meta_wa_crm_in_discuss/static/src/xml/wa_thread_view.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
