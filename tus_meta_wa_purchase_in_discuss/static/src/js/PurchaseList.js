/** @odoo-module **/

const { Component, onRendered, useRef, useEffect, useState, xml } = owl;
const rpc = require('web.rpc');
var session = require('web.session');

const { qweb } = require('web.core');
const ajax = require('web.ajax');
const {assets} = require('@web/core/assets');

export class PurchaseList extends Component{
            counter1 = useState({ value: 0 ,});
            constructor(WaThreadView) {
                super(...arguments);
                this.WaThreadView = WaThreadView
                var self=this;
                self.purchases = []
                self.purchase_orders = []
                var partner_id
                if(session.partner_id){
                    partner_id = session.partner_id
                }
                self.partner_id = partner_id
                rpc.query({
                    model: 'purchase.order',
                    method: 'get_partner_purchase_order',
                    args: [[],partner_id],
                }).then(function (result) {
                      self.purchases = result['purchases']
                      self.purchase_orders = result['purchase_orders']
                      var data_purchase = []
                      var data_purchase_orders = []
                      for (var i = 0; i < self.purchases.length; i++) {
                           data_purchase.push([self.purchases[i]['name'], self.purchases[i]['partner_id'][1],self.purchases[i]['date_order'],self.purchases[i]['user_id'][1],self.purchases[i]['amount_total'],self.purchases[i]['state']+'<button class="btn btn-primary edit_purchase fa fa-edit ml-2" style="border-radius: 20px;" id="'+self.purchases[i]['id']+'"></button>',]);
                      }
                      for (var i = 0; i < self.purchase_orders.length; i++) {
                           data_purchase_orders.push([self.purchase_orders[i]['name'], self.purchase_orders[i]['partner_id'][1],self.purchase_orders[i]['date_order'],self.purchase_orders[i]['user_id'][1],self.purchase_orders[i]['amount_total'],self.purchase_orders[i]['state']+'<button class="btn btn-primary edit_purchase fa fa-edit ml-2" style="border-radius: 20px;" id="'+self.purchase_orders[i]['id']+'"></button>',]);
                      }
                       var table = $('#purchase').DataTable({
                           data:data_purchase,
                        "dom": '<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-tl ui-corner-tr"<"#reloadBtn">lfr>t<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-bl ui-corner-br"ip>',retrieve: true});
                        var table2 = $('#purchase_orders').DataTable({
                           data:data_purchase_orders,
                        "dom": '<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-tl ui-corner-tr"<"#reloadBtn">lfr>t<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-bl ui-corner-br"ip>',retrieve: true});
                       if($('.purchase_create').length != 1){
                            $("#purchase_length").after("<div class='purchase_create' style='float:left;width:50%;'><div class='row pt-3'><div class='col-6' style='text-align:right;'><strong><p style='font-size: large;'>Quotations</p></strong></div><div class='col-6' style='text-align:left;'><button type='button' class='btn btn-primary ml-2 create_order'>Create</button></span></div></div></div>");
                            $("#purchase_orders_length").after("<div class='purchase_order_create' style='float:left;width:50%;'><div class='row pt-3'><div class='col-6' style='text-align:right;'><strong><p style='font-size: large;'>Purchase Order</p></strong></div><div class='col-6' style='text-align:left;'><button type='button' class='btn btn-primary ml-2 create_order'>Create</button></span></div></div></div>");
                        }
                        $('.create_order').on('click', function (e) {
                              var sale_order = self.env.bus.trigger('do-action', {action: {
                                    context: {main_form: true, create: false, 'default_partner_id':self.partner_id},
                                    type: 'ir.actions.act_window',
                                    res_model: 'purchase.order',
                                    views: [[false, 'form']],
                                    target: 'new',
                                    flags: {mode: 'edit'},
                                    options: {main_form: true,},
                                }
                             });
                             $('.main-button').removeClass('o_hidden');
                             $('.back_btn').removeClass('o_hidden');
//                             $('.back_btn').on('click',function(){
//                               self.discuss.parentWidget.tab_purchases()
//                             })
                        });
                        $('.edit_purchase').on('click',function(ev){
                            var sale_order = self.env.bus.trigger('do-action', {action: {
                                    context: {main_form: true, create: false},
                                    type: 'ir.actions.act_window',
                                    res_model: 'purchase.order',
                                    res_id: parseInt(ev.currentTarget.id),
                                    views: [[false, 'form']],
                                    target: 'new',
                                    flags: {mode: 'edit'},
                                    options: {main_form: true,},
                                }
                            });
                             $('.main-button').removeClass('o_hidden');
                             $('.back_btn').removeClass('o_hidden');
//                             $('.back_btn').on('click',function(){
//                               self.discuss.parentWidget.tab_purchases()
//                             })
                        });
                });
            }
}
PurchaseList.template = "tus_meta_wa_purchase_in_discuss.PurchaseList";