/** @odoo-module **/

const { Component, onRendered, useRef, useEffect, useState, xml } = owl;
const rpc = require('web.rpc');
var session = require('web.session');

export class HelpdeskList extends Component{
            counter1 = useState({ value: 0 ,});
            constructor(WaThreadView) {
                super(...arguments);
                this.WaThreadView = WaThreadView
                var self=this;
                self.tickets = []
                var partner_id
                if(session.partner_id){
                    partner_id = session.partner_id
                }
                self.partner_id = partner_id
                rpc.query({
                    model: 'helpdesk.ticket',
                    method: 'search_read',
                    domain: [
                        ['partner_id', '=', partner_id],
                    ],
                }).then(function (result) {
                    self.tickets = result
                    var data_ticket = []
                    for (var i = 0; i < self.tickets.length; i++) {
                        var user = ''
                        if(self.tickets[i]['user_id'].length > 0){
                            user = self.tickets[i]['user_id'][1]
                        }
                       data_ticket.push([self.tickets[i]['name'], self.tickets[i]['partner_id'][1],self.tickets[i]['team_id'][1],user,self.tickets[i]['stage_id'][1]+'<button class="btn btn-primary edit_sale fa fa-edit ml-2" style="border-radius: 20px;" id="'+self.tickets[i]['id']+'"></button>',]);
                    }
                    self.counter1.value++;
//
                    var table = $('#ticket').DataTable({
                       data:data_ticket,
                    "dom": '<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-tl ui-corner-tr"<"#reloadBtn">lfr>t<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-bl ui-corner-br"ip>',retrieve: true});
                    if($('.ticket_create').length != 1){
                        $("#ticket_length").after("<div class='ticket_create' style='float:left;width:50%;'><div class='row pt-3'><div class='col-6' style='text-align:right;'><strong><p style='font-size: large;'>My Tickets</p></strong></div><div class='col-6' style='text-align:left;'><button type='button' class='btn btn-primary ml-2 create_order'>Create</button></span></div></div></div>");
                    }
                    $('.create_order').on('click', function (e) {
                          var sale_order = self.env.bus.trigger('do-action', {action: {
                                context: {main_form: true, create: false,'default_partner_id':self.partner_id},
                                type: 'ir.actions.act_window',
                                res_model: 'helpdesk.ticket',
                                views: [[false, 'form']],
                                target: 'new',
                                flags: {mode: 'edit'},
                                options: {main_form: true,},
                            }
                          })

                         $('.main-button').removeClass('o_hidden');
                         $('.back_btn').removeClass('o_hidden');
                         $('.back_btn').on('click',function(){
                               self.WaThreadView.parentWidget.tabHelpdesk();
                         })
                    });
                    $('.edit_sale').on('click',function(ev){
                        var sale_order = self.env.bus.trigger('do-action', {action: {
                                context: {main_form: true, create: false},
                                type: 'ir.actions.act_window',
                                res_model: 'helpdesk.ticket',
                                res_id: parseInt(ev.currentTarget.id),
                                views: [[false, 'form']],
                                target: 'new',
                                flags: {mode: 'edit'},
                                options: {main_form: true,},
                            },
                        });
                         $('.main-button').removeClass('o_hidden');
                         $('.back_btn').removeClass('o_hidden');
                         $('.back_btn').on('click',function(){
                           self.discuss.parentWidget.tab_sales()
                         })
                    });
                });
            }
}
HelpdeskList.template = "HelpdeskList";