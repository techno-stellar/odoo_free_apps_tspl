from odoo import models, api

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if (config_model:= self._is_notify_users()) is not False:
            config_model._check_and_notify(records, 'create')
        return records

    def write(self, vals):
        res = super().write(vals)
        if (config_model:= self._is_notify_users()) is not False:
            config_model._check_and_notify(self, 'write', vals=vals)
        return res

    def unlink(self):
        if (config_model:= self._is_notify_users()) is not False:
            config_model._check_and_notify(self, 'unlink')
        res = super().unlink()
        return res

    def _is_notify_users(self):
        if not self.env.context.get('skip_notification') and not self._name.startswith('ir.'):
            config_model = self.env['dynamic.user.notification.config'].sudo()
            if self._name in config_model._get_config_registry():
                return config_model
        return False
