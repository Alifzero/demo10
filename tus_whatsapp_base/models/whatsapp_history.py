from odoo import models, api, fields
import json
import requests
from odoo.exceptions import UserError, ValidationError

class WhatsappHistory(models.Model):
    _description = 'Whatsapp History'
    _name = 'whatsapp.history'
    _rec_name = 'phone'

    provider_id = fields.Many2one('provider', 'Provider',readonly=True)
    author_id = fields.Many2one('res.partner', 'Author',readonly=True)
    partner_id = fields.Many2one('res.partner', 'Recipient',readonly=True)
    phone = fields.Char(string="Whatsapp Number",readonly=True)
    # phn_no = fields.Char('Phone Number')
    message = fields.Char('Message',readonly=True)
    type = fields.Selection([
        ('in queue', 'In queue'),
        ('sent', 'Sent'),
        ('delivered','delivered'),
        ('received', 'Received'),('read','Read'),('fail','Fail')], string='Type', default='in queue',readonly=True)
    attachment_ids = fields.Many2many(
        'ir.attachment', 'wa_history_attachment_rel',
        'wa_message_id', 'wa_attachment_id',
        string='Attachments', readonly=True)
    message_id = fields.Char("Message ID",readonly=True)
    fail_reason = fields.Char("Fail Reason",readonly=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company,readonly=True)
    date = fields.Datetime('Date', default=fields.Datetime.now,readonly=True)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        # phone change to mobile
        for rec in self:
            self.phone = self.partner_id.mobile

    @api.model
    def create(self, vals):
        res = super(WhatsappHistory, self).create(vals)
        if res.provider_id and res.partner_id and res.partner_id.mobile:
            res.partner_id.write({'mobile':res.partner_id.mobile.strip('+').replace(' ', '')})
            # partner = self.env['res.partner'].browse
            part_lst = []
            part_lst.append(res.partner_id.id)
            part_lst.append(int(vals.get('author_id')))

            channel = False
            if res.type == 'received':
                provider_channel_id = res.partner_id.channel_provider_line_ids.filtered(lambda s: s.provider_id == res.provider_id)
                if provider_channel_id:
                    channel = provider_channel_id.channel_id
                else:
                    name = res.partner_id.mobile
                    channel = self.env['mail.channel'].sudo().create({
                        'public': 'public',
                        'channel_type': 'chat',
                        'name': name,
                        'whatsapp_channel': True,
                        'channel_partner_ids': [(4,int(vals.get('partner_id')) ),(4,int(vals.get('author_id')) )],
                    })

                    mail_channel_partner = self.env['mail.channel.partner'].sudo().search(
                        [('channel_id', '=', channel.id),
                         ('partner_id', '=', int(vals.get('author_id')))])
                    mail_channel_partner.write({'is_pinned': True})

                    channel.write({'channel_member_ids': [(5, 0, 0)] + [(0, 0, {'partner_id': line_vals}) for
                                                                                   line_vals in part_lst]})
                    res.partner_id.write(
                        {'channel_provider_line_ids': [(0, 0, {'channel_id': channel.id, 'provider_id': res.provider_id.id})]})

                if channel:
                    message_values = {
                        'body': '<p> ' + res.message + '</p>',
                        'author_id': res.partner_id.id,
                        'email_from': res.partner_id.email or '',
                        'model': 'mail.channel',
                        'message_type': 'wa_msgs',
                        'wa_message_id': vals.get('message_id'),
                        'isWaMsgs': True,
                        'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id('mail.mt_comment'),
                        'partner_ids': [(4, res.partner_id.id)],
                        'res_id': channel.id,
                        'reply_to': res.partner_id.email,
                        'company_id': res.company_id.id,
                    }
                    if res.attachment_ids:
                        message_values.update({'attachment_ids': res.attachment_ids})
                    if 'quotedMsgId' in self.env.context:
                        parent_message = self.env['mail.message'].sudo().search_read(
                            [('wa_message_id', '=', self.env.context['quotedMsgId'])],
                            ['id', 'body', 'chatter_wa_model', 'chatter_wa_res_id', 'chatter_wa_message_id'])
                        if len(parent_message) > 0:
                            message_values.update({'parent_id': parent_message[0]['id']})
                            if parent_message[0].get('chatter_wa_model') and parent_message[0].get(
                                    'chatter_wa_res_id') and parent_message[0].get('chatter_wa_message_id'):
                                chatter_wa_message_values = {
                                    'body': res.message,
                                    'author_id': res.partner_id.id,
                                    'email_from': res.partner_id.email or '',
                                    'model': parent_message[0].get('chatter_wa_model'),
                                    'message_type': 'comment',
                                    'isWaMsgs': True,
                                    'subtype_id': self.env['ir.model.data'].sudo()._xmlid_to_res_id('mail.mt_comment'),
                                    # 'channel_ids': [(4, channel.id)],
                                    'partner_ids': [(4, res.partner_id.id)],
                                    'res_id': parent_message[0].get('chatter_wa_res_id'),
                                    'reply_to': res.partner_id.email,
                                    'parent_id': parent_message[0].get('chatter_wa_message_id'),
                                }
                                if vals.get('attachment_ids'):
                                    message_values.update({'attachment_ids': res.attachment_ids})
                                chatter_wa_message = self.env['mail.message'].sudo().create(
                                    chatter_wa_message_values)
                                notifications = channel._channel_message_notifications(chatter_wa_message)
                                self.env['bus.bus']._sendmany(notifications)

                    message = self.env['mail.message'].sudo().with_context({'message': 'received'}).create(
                        message_values)
                    notifications = channel._channel_message_notifications(message)
                    self.env['bus.bus']._sendmany(notifications)
            else:
                if not self.env.context.get('whatsapp_application'):
                    if 'template_send' in self.env.context and self.env.context.get('template_send'):
                        wa_template = self.env.context.get('wa_template')
                        params = []
                        for component in wa_template.components_ids:
                            object_data = self.env[wa_template.model_id.model].search_read(
                                [('id', '=', self.env.context.get('active_model_id'))])[0]

                            template_dict = {}

                            if component.type in ['body', 'footer']:
                                if component.variables_ids:
                                    template_dict.update({'type': component.type})
                                    parameters = []
                                    for variable in component.variables_ids:
                                        parameter_dict = {}
                                        if variable.field_id.ttype == 'text':
                                            if object_data.get(variable.field_id.name):
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': object_data.get(variable.field_id.name)})
                                            else:
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': ''})
                                        if variable.field_id.ttype == 'many2one':
                                            if object_data.get(variable.field_id.name):
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': object_data.get(variable.field_id.name)[1]})
                                            else:
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': ''})
                                        if variable.field_id.ttype == 'integer':
                                            parameter_dict.update(
                                                {'type': 'text',
                                                 'text': str(object_data.get(variable.field_id.name))})
                                        if variable.field_id.ttype == 'float':
                                            parameter_dict.update(
                                                {'type': 'text',
                                                 'text': str(object_data.get(variable.field_id.name))})
                                        if variable.field_id.ttype == 'monetary':
                                            text = False
                                            if 'currency_id' in object_data:
                                                currency_id = object_data.get('currency_id')[0]
                                                currency = self.env['res.currency'].browse(currency_id)
                                                if currency.position == 'after':
                                                    text = str(
                                                        object_data.get(variable.field_id.name)) + currency.symbol
                                                else:
                                                    text = currency.symbol + str(
                                                        object_data.get(variable.field_id.name))
                                            parameter_dict.update(
                                                {'type': 'text', 'text': text})
                                        if variable.field_id.ttype in ['char', 'selection']:
                                            if object_data.get(variable.field_id.name):
                                                parameter_dict.update({'type': 'text', 'text': object_data.get(
                                                    variable.field_id.name)})
                                            else:
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': ''})
                                        if variable.field_id.ttype in ['date']:
                                            if object_data.get(variable.field_id.name):
                                                parameter_dict.update({'type': 'text', 'text': object_data.get(
                                                    variable.field_id.name).strftime("%m/%d/%Y")})
                                            else:
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': ''})
                                        if variable.field_id.ttype in ['datetime']:
                                            if object_data.get(variable.field_id.name):
                                                parameter_dict.update({'type': 'text', 'text': object_data.get(
                                                    variable.field_id.name).strftime("%m/%d/%Y")})
                                            else:
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': ''})
                                        parameters.append(parameter_dict)
                                    template_dict.update({'parameters': parameters})

                            if component.type == 'header':
                                if component.formate == 'text':
                                    if component.variables_ids:
                                        template_dict.update({'type': component.type})
                                        parameters = []
                                        for variable in component.variables_ids:
                                            parameter_dict = {}
                                            if variable.field_id.ttype == 'text':
                                                if object_data.get(variable.field_id.name):
                                                    parameter_dict.update(
                                                        {'type': 'text',
                                                         'text': object_data.get(variable.field_id.name)})
                                                else:
                                                    parameter_dict.update(
                                                        {'type': 'text',
                                                         'text': ''})
                                            if variable.field_id.ttype == 'many2one':
                                                if object_data.get(variable.field_id.name):
                                                    parameter_dict.update(
                                                        {'type': 'text',
                                                         'text': object_data.get(variable.field_id.name)[1]})
                                                else:
                                                    parameter_dict.update(
                                                        {'type': 'text',
                                                         'text': ''})
                                            if variable.field_id.ttype == 'integer':
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': str(object_data.get(variable.field_id.name))})
                                            if variable.field_id.ttype == 'float':
                                                parameter_dict.update(
                                                    {'type': 'text',
                                                     'text': str(object_data.get(variable.field_id.name))})
                                            if variable.field_id.ttype == 'monetary':
                                                text = False
                                                if currency.position == 'after':
                                                    text = str(
                                                        object_data.get(variable.field_id.name)) + currency.symbol
                                                else:
                                                    text = currency.symbol + str(
                                                        object_data.get(variable.field_id.name))
                                                parameter_dict.update(
                                                    {'type': 'text', 'text': text})
                                            if variable.field_id.ttype in ['char', 'selection']:
                                                if object_data.get(variable.field_id.name):
                                                    parameter_dict.update({'type': 'text', 'text': object_data.get(
                                                        variable.field_id.name)})
                                                else:
                                                    parameter_dict.update(
                                                        {'type': 'text',
                                                         'text': ''})
                                            parameters.append(parameter_dict)
                                            template_dict.update({'parameters': parameters})

                                if component.formate == 'media':
                                    IrConfigParam = self.env['ir.config_parameter'].sudo()
                                    base_url = IrConfigParam.get_param('web.base.url', False)
                                    if component.media_type == 'document':
                                        if self.env.context.get('attachment_ids'):
                                            template_dict.update({'type': component.type})
                                            parameters = [{'type': component.media_type, 'document': {
                                                "link": base_url + "/web/content/" + str(
                                                    self.env.context.get('attachment_ids')[0]),
                                                "filename": self.env['ir.attachment'].sudo().browse(
                                                    self.env.context.get('attachment_ids')[0]).name}}]
                                            template_dict.update({'parameters': parameters})
                                    if component.media_type == 'video':
                                        if self.env.context.get('attachment_ids'):
                                            template_dict.update({'type': component.type})
                                            parameters = [{'type': component.media_type, 'video': {
                                                "link": base_url + "/web/content/" + str(
                                                    self.env.context.get('attachment_ids')[0]),
                                                "filename": self.env['ir.attachment'].sudo().browse(
                                                    self.env.context.get('attachment_ids')[0]).name}}]
                                            template_dict.update({'parameters': parameters})
                                    if component.media_type == 'image':
                                        template_dict.update({'type': component.type})
                                        parameters = [{'type': component.media_type, 'image': {
                                            "link": base_url + "/web/image/ir.attachment/" + str(
                                                self.env.context.get('attachment_ids')[0]) + "/datas",
                                        }}]
                                        template_dict.update({'parameters': parameters})

                            if bool(template_dict):
                                params.append(template_dict)
                        answer = res.provider_id.send_template(wa_template.name,wa_template.lang.iso_code,wa_template.namespace,res.partner_id,params)
                        if answer.status_code == 200:
                            dict = json.loads(answer.text)
                            if 'sent' in dict and dict.get('sent'):
                                res.message_id = dict['id']
                                if self.env.context.get('wa_messsage_id'):
                                    self.env.context.get('wa_messsage_id').wa_message_id = dict['id']
                            else:
                                if not self.env.context.get('cron'):
                                    if 'message' in dict:
                                        raise UserError(
                                            (dict.get('message')))
                                    if 'error' in dict:
                                        raise UserError(
                                            (dict.get('error').get('message')))
                                else:
                                    res.write({'type': 'fail'})
                                    if 'error' in dict:
                                        res.write({'fail_reason': dict.get('error').get('message')})
                    else:
                        if res.message:
                            answer = False
                            if 'message_parent_id' in self.env.context:
                                parent_msg = self.env['mail.message'].sudo().search(
                                    [('id', '=', self.env.context.get('message_parent_id').id)])
                                answer = res.provider_id.send_message(res.partner_id,res.message,parent_msg.wa_message_id)
                            else:
                                answer = res.provider_id.send_message(res.partner_id,res.message)
                            if answer.status_code == 200:
                                dict = json.loads(answer.text)
                                if 'sent' in dict and dict.get('sent'):
                                    res.message_id = dict['id']
                                    if self.env.context.get('wa_messsage_id'):
                                        self.env.context.get('wa_messsage_id').wa_message_id = dict['id']
                                else:
                                    if not self.env.context.get('cron'):
                                        if 'message' in dict:
                                            raise UserError(
                                                (dict.get('message')))
                                        if 'error' in dict:
                                            raise UserError(
                                                (dict.get('error').get('message')))
                                    else:
                                        res.write({'type': 'fail'})
                                        if 'message' in dict:
                                            res.write({'fail_reason': dict.get('message')})

                        if res.attachment_ids:
                            for attachment_id in res.attachment_ids:
                                answer = res.provider_id.send_file(res.partner_id, attachment_id)
                                if answer.status_code == 200:
                                    dict = json.loads(answer.text)
                                    if 'sent' in dict and dict.get('sent'):
                                        res.message_id = dict['id']
                                        if self.env.context.get('wa_messsage_id'):
                                            self.env.context.get('wa_messsage_id').wa_message_id = dict['id']
                                    else:
                                        if not self.env.context.get('cron'):
                                            if 'message' in dict:
                                                raise UserError(
                                                    (dict.get('message')))
                                            if 'error' in dict:
                                                raise UserError(
                                                    (dict.get('error').get('message')))
                                        else:
                                            res.write({'type': 'fail'})
                                            if 'message' in dict:
                                                res.write({'fail_reason': dict.get('message')})
        return res
