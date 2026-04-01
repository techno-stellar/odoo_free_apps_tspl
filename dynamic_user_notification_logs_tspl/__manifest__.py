{
    # App information
    'name': 'Dynamic User Notification Logs',
    'version': '17.0.1.0.0',
    'summary': 'Audit-ready logs for dynamic backend notifications in Odoo.(Dynamic Notification, Notification Logs)',
    'description': 'Dynamic User Notification Logs adds audit-ready logging for dynamic backend notifications in Odoo. It records which notification rule was triggered, which record caused it, who performed the action, which user received the notification, and the exact message sent (Odoo notification logs, user notification tracking, backend notification audit, notification history, real-time notification logging, Odoo audit trail, notification traceability, notification monitoring, user alert logs, record activity logs, create update delete logs, Odoo admin notifications, dynamic notifications, Odoo notification manager, notification analytics).',
    'category': 'Tools',
    'license': 'LGPL-3',

    # Author
    'author': 'Techno Stellar',
    'maintainer': 'Techno Stellar',

    # Dependencies
    'depends': ['dynamic_user_notification_tspl'],

    # Views & Data
    'data': [
        'security/ir.model.access.csv',
        'views/dynamic_user_notification_logs_views.xml',
        'views/dynamic_user_notification_config_views.xml',
    ],

    # Technical
    'images': ['static/description/banner.png', ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
