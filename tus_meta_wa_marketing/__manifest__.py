{
    'name': 'Odoo Meta Whatsapp Marketing',
    'version': '1.0.',
    'author': 'TechUltra Solutions',
    'category': 'Marketing',
    'live_test_url': 'https://www.techultrasolutions.com/blog/news-2/odoo-whatsapp-integration-a-boon-for-business-communication-25',
    'website': 'www.techultrasolutions.com',
    'price': 59,
    'currency': 'USD',
    'summary': 'Whatsapp Marketing, Whatsapp Messaging, Whatsapp All In One will help to send marketing messages to the customer and raw leads. you can connect with your customer by sending the latest and trending products',
    'description': """
        Whatsapp Marketing servers the purpose of the marketing of the products and brand, by adding the raw leads and by setting up the marketing list you can schedule your whatsapp message to the customer.
    """,
    'depends': ['tus_meta_whatsapp_base'],
    'data': [
        'security/ir.model.access.csv',
        'data/whatsapp_messaging_data.xml',
        'wizard/whatsapp_messaging_schedule_date_views.xml',
        'views/whatsapp_messaging_view.xml',
        'views/whatsapp_messaging_lists_view.xml',
        'views/whatsapp_messaging_lists_contacts_vies.xml',

    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
    # 'post_init_hook': '_set_image_in_company',
}
