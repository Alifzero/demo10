# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_partner_purchase_order(self, partner_id):
        if partner_id:
            purchases = self.env['purchase.order'].sudo().search_read(
                [('partner_id', '=', int(partner_id)), ('state', 'in', ['draft', 'sent'])],
                ['id', 'name', 'date_order', 'partner_id', 'user_id', 'amount_total', 'state'])
            purchase_orders = self.env['purchase.order'].sudo().search_read(
                [('partner_id', '=', int(partner_id)), ('state', 'in', ['purchase'])],
                ['id', 'name', 'date_order', 'partner_id', 'user_id', 'amount_total', 'state'])
            for purchase in purchases:
                purchase['amount_total'] = self.env.company.currency_id.symbol + " " + str(purchase['amount_total'])
                if purchase['state'] == 'draft':
                    purchase['state'] = 'Quotation'
                if purchase['state'] == 'sent':
                    purchase['state'] = 'Quotation Sent'
            for purchase in purchase_orders:
                if purchase['state'] == 'purchase':
                    purchase['state'] = 'Purchase Order'
            dict = {'purchases': purchases, 'purchase_orders': purchase_orders}
            return dict