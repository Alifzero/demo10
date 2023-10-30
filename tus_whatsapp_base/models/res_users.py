from odoo import _, api, fields, models, modules, tools
from itertools import chain

concat = chain.from_iterable

class ResUsers(models.Model):
    _inherit = 'res.users'

    provider_id = fields.Many2one('provider', 'Provider')

    '''
      Inherited Method
    '''
    def write(self, values):
        """
        Uncheck groups
        :param values: {}
        :return: {}
        """
        values = self._remove_reified_groups(values)
        if values.get('groups_id'):
            groups = values.get('groups_id')
            uncheck_ids = []
            whatsapp_manager_group = self.env.ref('tus_whatsapp_base.whatsapp_group_manager').id
            inherited_groups = self.env['res.groups'].search(
                [('implied_ids', 'in', self.env.ref('tus_whatsapp_base.whatsapp_group_user').ids)])
            for group in groups:
                if group[0] == 3 and group[1] == whatsapp_manager_group:
                    # implied_ids = self.env['res.groups'].sudo().browse(group[1]).implied_ids
                    gs = set(concat(g for g in inherited_groups))
                    uncheck_ids.extend([(3, g.id) for g in gs])
                if group[0] == 4 and group[1] == whatsapp_manager_group:
                    gs = set(concat(g for g in inherited_groups))
                    uncheck_ids.extend([(4, g.id) for g in gs])
            if uncheck_ids:
                values.get('groups_id').extend(uncheck_ids)
        return super(ResUsers, self).write(values)