{
    # App information
    'name': 'Dynamic User Notification',
    'version': '18.0.1.0.0',
    'summary': 'Configurable real-time backend notifications for Odoo users.(Dynamic Notification)',
    'description': 'Dynamic User Notification adds a flexible real-time notification system for Odoo backend users. It lets administrators configure model-based notification rules for record creation, state-based updates, and deletion, so internal users receive instant alerts without custom development (Odoo user notifications, backend notifications, real-time alerts, Odoo notification engine, model-based notifications, record create alerts, state change notifications, record deletion alerts, internal user alerts, configurable notifications, Odoo bus notifications, admin notification rules, sticky notifications, workflow alerts, Odoo backend alerts).',
    'category': 'Tools',
    'license': 'LGPL-3',

    # Author
    'author': 'Techno Stellar',
    'maintainer': 'Techno Stellar',

    # Dependencies
    'depends': ['base', 'mail'],

    # Views & Data
    'data': [
        'security/ir.model.access.csv',
        'views/notification_config_views.xml',
        'views/menus.xml',
    ],

    # Technical
    'images': ['static/description/banner.png'],

    'installable': True,
    'application': False,
    'auto_install': False,
}
