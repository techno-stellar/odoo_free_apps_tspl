from odoo import models, fields, api
from ..globle import CommonVariables as CV


class DynamicUserNotificationConfig(models.Model):
    _name = 'dynamic.user.notification.config'
    _description = 'Dynamic User Notification Configuration'

    name = fields.Char(string='Name', required=True)
    model_id = fields.Many2one('ir.model', string='Related Model', required=True, ondelete='cascade')
    is_on_create = fields.Boolean(string='Notify on Creation', default=False)
    is_on_state_change = fields.Boolean(string='Notify on State change', default=False)
    is_on_unlink = fields.Boolean(string='Notify on Deletion', default=False)
    is_sticky = fields.Boolean(string='Is Sticky?', default=False)
    state_field_id = fields.Many2one('ir.model.fields', string='State Field',
                                     domain="[('model_id', '=', model_id), ('ttype', '=', 'selection')]")
    state_selection_ids = fields.Many2many('ir.model.fields.selection', string='Selected States',
                                           domain="[('field_id', '=', state_field_id)]")
    notify_user_ids = fields.Many2many('res.users', string='Users to Notify')
    notification_type = fields.Selection([
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ], string='Notification Type', default='success', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft')
    active = fields.Boolean(string='Active', default=True)

    @api.onchange('model_id')
    def _onchange_model_id(self):
        if not self.model_id:
            self.state_field_id = False

    @api.onchange('state_field_id')
    def _onchange_state_field_id(self):
        if not self.state_field_id:
            self.state_selection_ids = False

    @api.model
    def _get_config_registry(self):
        """ Get the raw dictionary of configurations from registry. """
        registry = self.env.registry
        if not hasattr(registry, '_dynamic_notification_registry'):
            all_configs = self.sudo().search([
                ('state', '=', 'confirmed'),
                ('active', '=', True)
            ])
            cache = {}
            for config in all_configs:
                m_name = config.model_id.model
                if m_name not in cache:
                    cache[m_name] = []
                cache[m_name].append(config.id)
            registry._dynamic_notification_registry = cache
        return registry._dynamic_notification_registry

    @api.model
    def _clear_notification_cache(self):
        """ Clear the registry cache when configurations change. """
        if hasattr(self.env.registry, '_dynamic_notification_registry'):
            delattr(self.env.registry, '_dynamic_notification_registry')

    @api.model_create_multi
    def create(self, vals_list):
        records = super(DynamicUserNotificationConfig, self.with_context(skip_notification=True)).create(vals_list)
        self._clear_notification_cache()
        return records

    def write(self, vals):
        res = super(DynamicUserNotificationConfig, self.with_context(skip_notification=True)).write(vals)
        self._clear_notification_cache()
        return res

    def unlink(self):
        res = super(DynamicUserNotificationConfig, self.with_context(skip_notification=True)).unlink()
        self._clear_notification_cache()
        return res

    def action_confirm(self):
        """
        This method is used to confirm the configuration and make it active.
        :return: boolean
        """
        return self.write({'state': 'confirmed'})

    def action_draft(self):
        """
        This method is used to set the configuration back to draft state.
        :return: boolean
        """
        return self.write({'state': 'draft'})

    def _check_and_notify(self, records, action_type, vals=None):
        """
        Checks if notifications should be sent for the given records.
        :param records: Recordset of the model being created/updated
        :param action_type: 'create' or 'write'
        :param vals: The values being written (only for 'write' action)
        :return: List of notifications sent
        """
        registry_dict = self._get_config_registry()
        config_ids = registry_dict.get(records._name, [])
        if not config_ids:
            return

        configs = self.sudo().browse(config_ids)
        configs = self._filter_configs_for_action(configs, action_type)

        notifications = []
        current_user = self.env.user
        for config in configs:
            # For state change, we must verify if the specific state was reached
            if self._is_skip_for_write(action_type, vals, config):
                continue

            # Send notifications
            for record in records:
                message = (f"{record._description} {CV.operations[action_type]}: {record.display_name} - "
                           f"By {current_user.name}")
                if action_type == 'write' and config.state_field_id:
                    field_name = config.state_field_id.name
                    state_label = dict(record._fields[field_name].selection).get(record[field_name])
                    message = (f"{record._description}-{record.display_name} state updated to '{state_label}'. - "
                               f"By {current_user.name}")

                notification_payload = {'type': config.notification_type,
                                        'message': message,
                                        'sticky': config.is_sticky,}

                for user in config.notify_user_ids:
                    notification = {**notification_payload,
                                    'notified_user_id': user,
                                    'origin_record': record,
                                    'config_id': config,}
                    notifications.append(notification)
                    self.env['bus.bus']._sendone(user.partner_id, 'simple_notification', notification_payload)
        return notifications

    @staticmethod
    def _filter_configs_for_action(configs, action_type):
        """
        Helper method to filter configurations based on the action type.
        :param configs: Recordset of configurations to filter
        :param action_type: 'create', 'write', or 'unlink'
        :return: Filtered recordset of configurations
        """
        if action_type == 'create':
            return configs.filtered(lambda c: c.is_on_create)
        elif action_type == 'write':
            return configs.filtered(lambda c: c.is_on_state_change)
        elif action_type == 'unlink':
            return configs.filtered(lambda c: c.is_on_unlink)
        return configs

    @staticmethod
    def _is_skip_for_write(action_type, vals, config):
        """
        Helper method to determine if notification should be skipped for write action based on state change.
        :param action_type: 'write'
        :param vals: The values being written
        :return: Boolean indicating whether to skip notification
        """
        if action_type == 'write' and vals:
            state_field = config.state_field_id.name
            if state_field not in vals:
                return True

            target_states = config.state_selection_ids.mapped('value')
            if vals[state_field] not in target_states:
                return True
        return False
