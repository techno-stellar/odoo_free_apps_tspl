from odoo import fields, models


class DynamicUserNotificationLogs(models.Model):
    _name = 'dynamic.user.notification.logs'
    _description = 'Dynamic User Notification Logs'
    _order = 'id desc'
    _rec_name = 'message'

    def _get_model_reference(self):
        registry_dict = self.env['dynamic.user.notification.config'].sudo()._get_config_registry()
        models = self.env['ir.model'].sudo().search([('model', 'in', list(registry_dict.keys()))])
        return [(model.model, model.name) for model in models]

    config_id = fields.Many2one('dynamic.user.notification.config', string='Notification Config', ondelete='set null')
    model_name = fields.Char(string='Model')
    res_id = fields.Integer(string='Record ID')
    record_id = fields.Reference(selection='_get_model_reference', string='Related Record')
    action_type = fields.Selection([('create', 'Create'), ('write', 'Update'), ('unlink', 'Delete')],
                                   string='Action Type', required=True)
    user_id = fields.Many2one('res.users', string='Triggered By', default=lambda self: self.env.user, ondelete='set null')
    notified_user_id = fields.Many2one('res.users', string='Notified User', ondelete='set null')
    message = fields.Char(string='Message')
