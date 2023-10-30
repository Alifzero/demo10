/** @odoo-module **/

const { Component, onRendered, useRef, useEffect, useState, xml } = owl;
const rpc = require('web.rpc');
var session = require('web.session');

const { qweb } = require('web.core');
const ajax = require('web.ajax');
const {assets} = require('@web/core/assets');

export class LeadList extends Component{
            counter1 = useState({ value: 0 ,});
            constructor(WaThreadView) {
                super(...arguments);
                this.WaThreadView = WaThreadView
                var self=this;
                self.leads = []
                var partner_id
                if(session.partner_id){
                    partner_id = session.partner_id
                }
                self.partner_id = partner_id
                rpc.query({
                    model: 'crm.lead',
                    method: 'search_read',
                    domain: [
                        ['partner_id', '=', partner_id],
                    ],
                }).then(function (result) {
                      self.leads = result
                      var data_lead = []

                      for (var i = 0; i < self.leads.length; i++) {
                            var email = ''
                            if(self.leads[i]['email_from']){
                                email = self.leads[i]['email_from']
                            }
                            var expected_revenue = ''
                            if(self.leads[i]['expected_revenue']){
                                expected_revenue = self.leads[i]['expected_revenue']
                            }
                           data_lead.push([self.leads[i]['name'], self.leads[i]['partner_id'][1],email,self.leads[i]['user_id'][1],expected_revenue,self.leads[i]['stage_id'][1]+'<button class="btn btn-primary edit_purchase fa fa-edit ml-2" style="border-radius: 20px;" id="'+self.leads[i]['id']+'"></button>',]);
                      }
                       var table = $('#lead').DataTable({
                           data:data_lead,
                        "dom": '<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-tl ui-corner-tr"<"#reloadBtn">lfr>t<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-bl ui-corner-br"ip>',retrieve: true});
                       if($('.lead_create').length != 1){
                            $("#lead_length").after("<div class='lead_create' style='float:left;width:50%;'><div class='row pt-3'><div class='col-6' style='text-align:right;'><strong><p style='font-size: large;'>Lead</p></strong></div><div class='col-6' style='text-align:left;'><button type='button' class='btn btn-primary ml-2 create_order'>Create</button></span></div></div></div>");
                        }
                        $('.create_order').on('click', function (e) {
                              var sale_order = self.env.bus.trigger('do-action', {action: {
                                    context: {main_form: true, create: false,'default_partner_id':self.partner_id},
                                    type: 'ir.actions.act_window',
                                    res_model: 'crm.lead',
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
                                    res_model: 'crm.lead',
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
LeadList.template = "tus_meta_wa_crm_in_discuss.LeadList";