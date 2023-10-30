from odoo.http import request
from odoo import http, _, tools
import requests
import json
import base64
import phonenumbers
import datetime
from odoo.exceptions import UserError, ValidationError
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
)
import hashlib
import base64


class WebHook2(http.Controller):
    _webhook_url = '/graph_tus/webhook'
    _meta_fb_url = '/graph_tus/webhook'

    # @http.route(['/graph_tus/webhook'], auth='public', type="http", csrf=False, methods=['GET'])
    @http.route(_webhook_url, type='http', methods=['GET'], auth='public', csrf=False)
    def facebook_webhook(self, **kw):
        #print("1111111111111111111 main*********************facebook_webhook", self, kw)
        if kw.get('hub.verify_token'):
            return kw.get('hub.challenge')

    def get_channel(self, partner_to, provider):
        partner = False
        if len(partner_to) > 0:
            partner = request.env['res.partner'].sudo().browse(partner_to[0])
        if request.env.user.has_group('base.group_user'):
            partner_to.append(request.env.user.partner_id.id)
        else:
            partner_to.append(provider.user_id.partner_id.id)
        channel = False

        provider_channel_id = partner.channel_provider_line_ids.filtered(lambda s: s.provider_id == provider)
        if provider_channel_id:
            channel = provider_channel_id.channel_id
            if request.env.user.partner_id.id not in channel.channel_partner_ids.ids and request.env.user.has_group(
                    'base.group_user'):
                channel.sudo().write({'channel_partner_ids': [(4, request.env.user.partner_id.id)]})
        else:
            # phone change to mobile
            name = partner.mobile
            channel = request.env['mail.channel'].sudo().create({
                #'public': 'public',
                'channel_type': 'chat',
                'name': name,
                'whatsapp_channel': True,
                'channel_partner_ids': [(4, x) for x in partner_to],
            })
            channel.write({'channel_last_seen_partner_ids': [(5, 0, 0)] + [
                (0, 0, {'partner_id': line_vals}) for line_vals in partner_to]})
            # partner.write({'channel_id': channel.id})
            partner.write({'channel_provider_line_ids': [
                (0, 0, {'channel_id': channel.id, 'provider_id': provider.id})]})
        return channel

    def get_url(self, provider, media_id, phone_number_id):
        if provider.graph_api_authenticated:
            url = provider.graph_api_url + media_id + "?phone_number_id=" + phone_number_id + "&access_token=" + provider.graph_api_token
            headers = {'Content-type': 'application/json'}
            payload = {}
            try:
                answer = requests.request("GET", url, headers=headers, data=payload)
            except requests.exceptions.ConnectionError:
                raise UserError(
                    ("please check your internet connection."))
            return answer
        else:
            raise UserError(
                ("please authenticated your whatsapp."))

    def get_media_data(self, url, provider):
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + provider.graph_api_token
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        decoded = base64.b64encode(response.content)
        return decoded

    # @http.route(['/graph_tus/webhook'], auth='public', type="json", csrf=False, methods=['GET', 'POST'])
    @http.route(_meta_fb_url, type='json', methods=['GET', 'POST'], auth='public', csrf=False)
    def meta_webhook(self, **kw):
        #print("2222222222222222222 main*********************meta_webhook", self, kw)
        wa_dict = {}

        data = json.loads(request.httprequest.data.decode('utf-8'))
        wa_dict.update({'messages': data.get('messages')})

        phone_number_id = ''
        if data and data.get('entry'):
            if data.get('entry')[0].get('changes'):
                if data.get('entry')[0].get('changes')[0].get('value'):
                    if data.get('entry')[0].get('changes')[0].get('value').get('metadata'):
                        if data.get('entry')[0].get('changes')[0].get('value').get('metadata').get('phone_number_id'):
                            phone_number_id = data.get('entry')[0].get('changes')[0].get('value').get('metadata').get(
                                'phone_number_id')

        provider = request.env['provider'].sudo().search(
            [('graph_api_authenticated', '=', True), ('graph_api_instance_id', '=', phone_number_id)], limit=1)
        wa_dict.update({'provider': provider})

        if data and data.get('entry'):
            if data.get('entry')[0].get('changes'):
                if data.get('entry')[0].get('changes')[0].get('value'):
                    if data.get('entry')[0].get('changes')[0].get('value').get('statuses'):
                        for acknowledgment in data.get('entry')[0].get('changes')[0].get('value').get('statuses'):
                            wp_msgs = request.env['whatsapp.history'].sudo().search(
                                [('message_id', '=', acknowledgment.get('id'))], limit=1)
                            if wp_msgs:
                                if acknowledgment.get('status') == 'sent':
                                    wp_msgs.sudo().write({'type': 'sent'})
                                elif acknowledgment.get('status') == 'delivered':
                                    wp_msgs.sudo().write({'type': 'delivered'})
                                elif acknowledgment.get('status') == 'read':
                                    wp_msgs.sudo().write({'type': 'read'})
                                elif acknowledgment.get('status') == 'failed':
                                    wp_msgs.sudo().write(
                                        {'type': 'fail', 'fail_reason': acknowledgment.get('errors')[0].get('title')})

        if provider.graph_api_authenticated:
            user_partner = provider.user_id.partner_id
            if data and data.get('entry'):
                if data.get('entry')[0].get('changes'):
                    if data.get('entry')[0].get('changes')[0].get('value'):
                        if data.get('entry')[0].get('changes')[0].get('value').get('messages'):
                            for mes in data.get('entry')[0].get('changes')[0].get('value').get('messages'):
                                number = mes.get('from')
                                messages_id = mes.get('id')
                                # messages_body = mes.get('text').get('body')
                                wa_dict.update({'chat': True})
                                partners = request.env['res.partner'].sudo().search(
                                    ['|', ('phone', '=', number), ('mobile', '=', number)])
                                wa_dict.update({'partners': partners})
                                if not partners:
                                    pn = phonenumbers.parse('+' + number)
                                    country_code = region_code_for_country_code(pn.country_code)
                                    country_id = request.env['res.country'].sudo().search(
                                        [('code', '=', country_code)], limit=1)
                                    partners = request.env['res.partner'].sudo().create(
                                        {'name': data.get('entry')[0].get('changes')[0].get('value').get('contacts')[
                                            0].get('profile').get('name'), 'country_id': country_id.id,
                                         'mobile': number})

                                for partner in partners:
                                    partner_id = partner.id
                                    if mes.get('type') == 'text':
                                        vals = {
                                            'provider_id': provider.id,
                                            'author_id': user_partner.id,
                                            'message': mes.get('text').get('body'),
                                            'message_id': messages_id,
                                            'type': 'received',
                                            'partner_id': partner_id,
                                            'phone': partner.mobile,
                                            'attachment_ids': False,
                                            'company_id': provider.company_id.id,
                                            # 'date':datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                        }
                                        request.env['whatsapp.history'].sudo().create(vals)

                                    elif mes.get('type') == 'location':
                                        # phone change to mobile
                                        lat = mes.get('location').get('latitude')
                                        lag = mes.get('location').get('longitude')
                                        vals = {
                                            'message': "<a href='https://www.google.com/maps/search/?api=1&query=" + str(
                                                lat) + "," + str(
                                                lag) + "' target='_blank' class='btn btn-primary'>Google Map</a>",
                                            'message_id': messages_id,
                                            'author_id': user_partner.id,
                                            'type': 'received',
                                            'partner_id': partner_id,
                                            'phone': partner.mobile,
                                            'attachment_ids': False,
                                            'provider_id': provider.id,
                                            'company_id': provider.company_id.id,
                                            # 'date': datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                        }
                                        request.env['whatsapp.history'].sudo().create(vals)
                                    elif mes.get('type') == 'image':
                                        media_id = mes.get('image').get('id')
                                        geturl = self.get_url(provider, media_id, phone_number_id)
                                        dict = json.loads(geturl.text)
                                        decoded = self.get_media_data(dict.get('url'), provider)

                                        attachment_value = {
                                            'name': mes.get('image').get('caption'),
                                            'datas': decoded,
                                            'type': 'binary',
                                            'mimetype': mes.get('image').get('mime_type') if mes.get(
                                                'image') and mes.get('image').get('mime_type') else 'image/jpeg',
                                        }
                                        attachment = request.env['ir.attachment'].sudo().create(attachment_value)
                                        res = request.env['whatsapp.history'].sudo().create(
                                            {'message': mes.get('image').get('caption') if 'image' in mes and 'caption' in mes.get('image') else '',
                                             'message_id': messages_id,
                                             'author_id': user_partner.id,
                                             'type': 'received',
                                             'partner_id': partner_id,
                                             'phone': partner.mobile,
                                             'attachment_ids': [(4, attachment.id)],
                                             'provider_id': provider.id,
                                             'company_id': provider.company_id.id,
                                             # 'date': datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                             })
                                    elif mes.get('type') == 'document':
                                        media_id = mes.get('document').get('id')
                                        geturl = self.get_url(provider, media_id, phone_number_id)
                                        dict = json.loads(geturl.text)
                                        decoded = self.get_media_data(dict.get('url'), provider)

                                        attachment_value = {
                                            'name': mes.get('document').get('filename'),
                                            'datas': decoded,
                                            'type': 'binary',
                                            'mimetype': mes.get('document').get('mime_type') if mes.get(
                                                'document') and mes.get('document').get(
                                                'mime_type') else 'application/pdf',
                                        }
                                        attachment = request.env['ir.attachment'].sudo().create(attachment_value)
                                        res = request.env['whatsapp.history'].sudo().create(
                                            {'message': mes.get('document').get('caption') if 'document' in mes and 'caption' in mes.get('document') else '',
                                             'message_id': messages_id,
                                             'author_id': user_partner.id,
                                             'type': 'received',
                                             'partner_id': partner_id,
                                             'phone': partner.mobile,
                                             'attachment_ids': [(4, attachment.id)],
                                             'provider_id': provider.id,
                                             'company_id': provider.company_id.id,
                                             # 'date': datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                             })
                                    elif mes.get('type') == 'video':
                                        media_id = mes.get('video').get('id')
                                        geturl = self.get_url(provider, media_id, phone_number_id)
                                        dict = json.loads(geturl.text)
                                        decoded = self.get_media_data(dict.get('url'), provider)

                                        attachment_value = {
                                            'name': 'whatsapp_video',
                                            'datas': decoded,
                                            'type': 'binary',
                                            'mimetype': mes.get('video').get('mime_type') if mes.get(
                                                'video') and mes.get('video').get('mime_type') else 'video/mp4',
                                        }
                                        attachment = request.env['ir.attachment'].sudo().create(attachment_value)
                                        res = request.env['whatsapp.history'].sudo().create(
                                            {'message': mes.get('video').get('caption') if 'video' in mes and 'caption' in mes.get('video') else '',
                                             'message_id': messages_id,
                                             'author_id': user_partner.id,
                                             'type': 'received',
                                             'partner_id': partner_id,
                                             'phone': partner.mobile,
                                             'attachment_ids': [(4, attachment.id)],
                                             'provider_id': provider.id,
                                             'company_id': provider.company_id.id,
                                             # 'date': datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                             })
                                    elif mes.get('type') == 'audio':
                                        media_id = mes.get('audio').get('id')
                                        geturl = self.get_url(provider, media_id, phone_number_id)
                                        dict = json.loads(geturl.text)
                                        decoded = self.get_media_data(dict.get('url'), provider)

                                        attachment_value = {
                                            'name': 'whatsapp_audio',
                                            'datas': decoded,
                                            'type': 'binary',
                                            'mimetype': mes.get('audio').get('mime_type') if mes.get(
                                                'audio') and mes.get('audio').get('mime_type') else 'audio/mpeg',
                                        }
                                        attachment = request.env['ir.attachment'].sudo().create(attachment_value)
                                        res = request.env['whatsapp.history'].sudo().create(
                                            {'message': mes.get('audio').get('caption') if 'audio' in mes and 'caption' in mes.get('audio') else '',
                                             'message_id': messages_id,
                                             'author_id': user_partner.id,
                                             'type': 'received',
                                             'partner_id': partner_id,
                                             'phone': partner.mobile,
                                             'attachment_ids': [(4, attachment.id)],
                                             'provider_id': provider.id,
                                             'company_id': provider.company_id.id,
                                             # 'date': datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                             })
                                    elif mes.get('type') == 'sticker':
                                        media_id = mes.get('sticker').get('id')
                                        geturl = self.get_url(provider, media_id, phone_number_id)
                                        dict = json.loads(geturl.text)
                                        decoded = self.get_media_data(dict.get('url'), provider)

                                        attachment_value = {
                                            'name': 'whatsapp_sticker',
                                            'datas': decoded,
                                            'type': 'binary',
                                            'mimetype': mes.get('sticker').get('mime_type') if mes.get(
                                                'sticker') and mes.get('sticker').get('mime_type') else 'image/webp',
                                        }
                                        attachment = request.env['ir.attachment'].sudo().create(attachment_value)
                                        res = request.env['whatsapp.history'].sudo().create(
                                            {'message': mes.get('sticker').get('caption') if 'sticker' in mes and 'caption' in mes.get('sticker') else '',
                                             'message_id': messages_id,
                                             'author_id': user_partner.id,
                                             'type': 'received',
                                             'partner_id': partner_id,
                                             'phone': partner.mobile,
                                             'attachment_ids': [(4, attachment.id)],
                                             'provider_id': provider.id,
                                             'company_id': provider.company_id.id,
                                             # 'date': datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                             })
                                    else:
                                        vals = {
                                            'provider_id': provider.id,
                                            'author_id': user_partner.id,
                                            'message': mes.get('text').get('body'),
                                            'message_id': messages_id,
                                            'type': 'received',
                                            'partner_id': partner_id,
                                            'phone': partner.mobile,
                                            'attachment_ids': False,
                                            'company_id': provider.company_id.id,
                                            # 'date':datetime.datetime.fromtimestamp(int(mes.get('time'))),
                                        }
                                        request.env['whatsapp.history'].sudo().create(vals)
        return wa_dict
