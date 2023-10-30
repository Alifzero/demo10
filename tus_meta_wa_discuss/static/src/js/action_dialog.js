
/** @odoo-module **/

import { ActionDialog } from "@web/webclient/actions/action_dialog";
import { patch } from "@web/core/utils/patch";
import { useComponent, Component, onMounted, onWillUnmount,onPatched, useEffect, useRef } from "@odoo/owl";
//import { Component, onMounted, onWillUnmount, useExternalListener, useState, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { DebugMenu } from "@web/core/debug/debug_menu";
import { useOwnDebugContext } from "@web/core/debug/debug_context";
import { useLegacyRefs } from "@web/legacy/utils";
import { WaThreadView } from "@tus_meta_wa_discuss/js/wa_thread_view";
var Widget = require('web.Widget');
const LEGACY_SIZE_CLASSES = {
    "extra-large": "modal-xl",
    large: "modal-lg",
    small: "modal-sm",
};
var core = require('web.core');
var QWeb = core.qweb;
import { ClientActionAdapter, ViewAdapter } from "@web/legacy/action_adapters";
import { useUpdate } from '@mail/component_hooks/use_update';

patch(ActionDialog.prototype, 'tus_meta_wa_discuss/static/src/js/action_dialog.js', {
    setup() {
        this._super();
        onMounted(() => this._mounted());
//        console.log(">>>>>>>>>>1>>",this)
        if (this.props.actionProps.context.main_form || $('#main-form-view').length > 0) {
//            console.log("TEst",$('#main-form-view'))
        }
//        if(this.props.actionProps.action.main_form || $('#main-form-view').length > 0){
//        useEffect(
//            () => {
//                    // Retrieve the widget climbing the wrappers
//                    const componentController = this.actionRef.comp;
//                    const controller = componentController.componentRef.comp;
//                    const viewAdapter = controller.controllerRef.comp;
//                    const widget = viewAdapter.widget;
//                    // Render legacy footer buttons
//                    const footer = this.modalRef.el.querySelector("footer");
//                    if(this.props.actionProps.action.main_form || $('#main-form-view').length){
//                        widget.renderButtons($('.modal-footer'));
//                    }
//            },
//            () => []
//        ); // TODO: should this depend on actionRef.comp?
//        }
    },
    _mounted(){
//        console.log(">>>>>>>>222>>>>",this)
        if(this.props.actionProps.context.main_form || $('#main-form-view').length > 0){
            if(typeof(this.props.actionProps.context.main_form) == 'undefined' ){
                $('.back_btn').removeClass('o_hidden')
            }
//            console.log(">>>>>>>>33333333333>>>>",this)
            if(this.modalRef && this.modalRef.el){
                $('#main-form-view').html($(this.modalRef.el).find('.modal-body'));
                $('#main-buttons-view').html($(this.modalRef.el).find('.modal-footer'));
            }
            $(document.body).find('.o_dialog_container').remove();
            $(document.body).find('.o_effects_manager').after('<div class="o_dialog_container"></div>');
        }
    }
});

//patch(ActionDialog.prototype, 'tus_meta_wa_discuss/static/src/js/action_dialog.js', {
//
//
//    setup() {
//        this._super();
//        const node = this.__owl__;
//        const actionProps = this.props && this.props.actionProps;
//        const actionContext = actionProps && actionProps.context;
//        const actionDialogSize = actionContext && actionContext.dialog_size;
//        this.props.size = LEGACY_SIZE_CLASSES[actionDialogSize] || Dialog.defaultProps.size;
//        const ControllerComponent = this.props && this.props.ActionComponent;
//        const Controller = ControllerComponent && ControllerComponent.Component;
//        this.isLegacy = Controller && Controller.isLegacy;
//        const env = owl.useEnv();
//        const legacyRefs = useLegacyRefs();
//        legacyRefs.component = this;
//
//        if(this.props.actionProps.context.main_form || $('#main-form-view').length > 0){
//            useEffect(
//                () => {
//
//                        // Render legacy footer buttons
//                        legacyRefs.widget = this.widget;
//                        const footer = this.modalRef.el.querySelector("footer");
//                        if(this.props.actionProps.context.main_form || $('#main-form-view').length){
////                            this.modalRef.el.querySelector(".modal-footer")
//                            //widget.renderButtons($('.modal-footer'));
//                            //legacyRefs.widget.renderButtons($(footer));
//                        }
//
//                },
//                () => []
//            ); // TODO: should this depend on actionRef.comp?
//        }
////        onMounted(() => {
////             if(this.props.actionProps.context.main_form || $('#main-form-view').length > 0){
////                 if(typeof(this.props.actionProps.context.main_form) == 'undefined' ){
////                    $('.back_btn').removeClass('o_hidden')
////                 }
////                 $('#main-form-view').html($(this.modalRef.el).find('.modal-body'));
////                    $('#main-buttons-view').html($(this.modalRef.el).find('.modal-footer'));
////                    $(document.body).find('.o_dialog_container').remove();
////                    $(document.body).find('.o_effects_manager').after('<div class="o_dialog_container"></div>');
////             }
////        });
////        onWillUnmount(() => {
////            const portal = node.bdom;
////            portal.remove();
////        });
//    }
//});