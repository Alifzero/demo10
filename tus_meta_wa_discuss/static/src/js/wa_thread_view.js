/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { registerModel } from '@mail/model/model_core';
import { registerMessagingComponent } from '@mail/utils/messaging_component';
const { Component, onWillUnmount, onWillUpdateProps, useState } = owl;
import Dialog from 'web.Dialog';
import OwlDialog from 'web.OwlDialog';
import core from 'web.core';
import { AgentsList } from '@tus_meta_wa_discuss/js/AgentsList';
const { ComponentWrapper, WidgetAdapterMixin } = require('web.OwlCompatibility');
import { attr, one } from '@mail/model/model_field';
import { clear } from '@mail/model/model_field_command';


export class WaThreadView extends Component {
    setup() {
        super.setup();
        this.messaging.wa_thread_view = this
        this.state = useState({
            nav_active:'partner'
        });
    }


    mounted(){
        super.mounted();
         if(this.state.nav_active == 'partner'){
            this.tabPartner();
        }
    }
    render(){
        super.render();
        if(this.state.nav_active == 'partner'){
            this.tabPartner();
        }
    }

    onClickBack(){
        if(this.state.nav_active == 'partner'){
            this.tabPartner();
        }
    }

    tabPartner(){
        var self= this
        this.state.nav_active = 'partner'
        if(self.waThreadView){
            if(self.messaging.currentPartner){
                var partner = this.env.services['action'].doAction({
                    name: 'Partner',
                    type: 'ir.actions.act_window',
                    res_model: 'res.partner',
                    res_id: self.messaging.currentPartner.id,
                    views: [[false, 'form']],
//                    main_form: true,
                    target: 'new',
                    context: {main_form: true, create: false},
                    flags: {mode: 'edit'},
                    options: {main_form: true,}
                });
            }
        }
        $('.main-button').removeClass('o_hidden');
        $('.back_btn').addClass('o_hidden');
    }

    tab_agent(){
        var self= this
        this.state.nav_active = 'agent'
        $('.main-button').addClass('o_hidden');
        $('#main-form-view').replaceWith("<div id='main-form-view'></div>")
        const AgentsListComponent = new ComponentWrapper(this, AgentsList, {});
        AgentsListComponent.mount($('#main-form-view')[0]);
    }
    get waThreadView() {

        var threads = this.messaging.models['Thread'].all().filter(thread => thread.localId == this.props.threadViewLocalId);
        return threads && threads[0];
    }

}

Object.assign(WaThreadView, {
    props: { threadViewLocalId: String },
    template: 'tus_meta_wa_discuss.WaThreadView',
});

registerMessagingComponent(WaThreadView);

registerPatch({
    name: 'Discuss',
    recordMethods: {
        waThreadView() {
            return this.messaging;
        },
    },
    fields: {
        hasWAThreadNav: attr({
            compute() {
                return Boolean(this.messaging.discuss.thread && this.messaging.discuss.thread.localId);
            },
        }),
    },
});