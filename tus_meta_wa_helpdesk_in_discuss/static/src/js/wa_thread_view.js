/** @odoo-module **/

import { WaThreadView } from "@tus_meta_wa_discuss/js/wa_thread_view";
import { patch } from 'web.utils';
import { HelpdeskList } from "@tus_meta_wa_helpdesk_in_discuss/js/HelpdeskList";
import { useEffect } from "@web/core/utils/hooks";

const { ComponentWrapper, WidgetAdapterMixin } = require('web.OwlCompatibility');

patch(WaThreadView.prototype, 'tus_meta_wa_helpdesk_in_discuss/static/src/js/wa_thread_view.js', {
    tabHelpdesk(){
        this.state.nav_active = 'helpdesk'
        $('.back_btn').addClass('o_hidden');
        $('.main-button').addClass('o_hidden');
        $('#main-form-view').replaceWith("<div id='main-form-view'></div>")
        const ProductComponent=new ComponentWrapper(this, HelpdeskList, {});
        ProductComponent.mount($('#main-form-view')[0]);
    },
    onClickBack(){
        this._super()
        if(this.state.nav_active == 'helpdesk'){
            this.tabHelpdesk();
        }
    }
});