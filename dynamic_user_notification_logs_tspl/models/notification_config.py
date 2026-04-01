from odoo import fields, models


class DynamicUserNotificationConfig(models.Model):
    _inherit = 'dynamic.user.notification.config'

    create_log_on_create = fields.Boolean(string='Create Logs on Create')
    create_log_on_write = fields.Boolean(string='Create Logs on Update')
    create_log_on_unlink = fields.Boolean(string='Create Logs on Delete')

    notification_log_ids = fields.One2many('dynamic.user.notification.logs', 'config_id', string='Notification Logs')
    notification_log_count = fields.Integer(string='Log Count', compute='_compute_notification_log_count')

    def _compute_notification_log_count(self):
        logs_model = self.env['dynamic.user.notification.logs'].sudo()
        for config in self:
            config.notification_log_count = logs_model.search_count([('config_id', '=', config.id)])

    def action_open_notification_logs(self):
        self.ensure_one()
        action = self.env.ref('dynamic_user_notification_logs_tspl.action_dynamic_user_notification_logs').read()[0]
        action['domain'] = [('config_id', '=', self.id)]
        action['context'] = {'create': False, 'edit': False, 'default_config_id': self.id}
        return action

    def _check_and_notify(self, records, action_type, vals=None):
        notifications = super()._check_and_notify(records, action_type, vals=vals)
        create_log_field = {
            'create': 'create_log_on_create',
            'write': 'create_log_on_write',
            'unlink': 'create_log_on_unlink',
        }.get(action_type, '')

        user = self.env.user
        log_vals = []
        for notification in notifications:
            config = notification['config_id']
            if not getattr(config, create_log_field, False):
                continue
            record = notification['origin_record']
            log_vals.append({
                'config_id': config.id,
                'model_name': record._name,
                'res_id': record.id,
                'record_id': f"{record._name},{record.id}",
                'action_type': action_type,
                'user_id': user.id,
                'notified_user_id': notification['notified_user_id'].id,
                'message': notification['message']
            })
        if log_vals:
            self.env['dynamic.user.notification.logs'].sudo().create(log_vals)
        return notifications
