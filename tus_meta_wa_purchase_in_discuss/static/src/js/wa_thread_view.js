/** @odoo-module **/

import { WaThreadView } from "@tus_meta_wa_discuss/js/wa_thread_view";
import { patch } from 'web.utils';
import { PurchaseList } from './PurchaseList.js';
import { useEffect } from "@web/core/utils/hooks";

const { ComponentWrapper, WidgetAdapterMixin } = require('web.OwlCompatibility');

patch(WaThreadView.prototype, 'tus_meta_wa_purchase_in_discuss/static/src/js/wa_thread_view.js', {
    tabPurchase(){
        this.state.nav_active = 'purchase'
        $('.back_btn').addClass('o_hidden');
        $('.main-button').addClass('o_hidden');
        $('#main-form-view').replaceWith("<div id='main-form-view'></div>")
        const PurchaseComponent=new ComponentWrapper(this, PurchaseList, {});
        PurchaseComponent.mount($('#main-form-view')[0]);
    },
    onClickBack(){
        this._super()
        if(this.state.nav_active == 'purchase'){
            this.tabPurchase();
        }
    }
});