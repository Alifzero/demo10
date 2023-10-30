/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ComponentWrapper } from 'web.OwlCompatibility';
const children = new WeakMap(); // associates legacy widgets with their Owl children
const { Component } = owl;
    function registerWrapper(parent, wrapper) {
        let parentChildren = children.get(parent);
        if (!parentChildren) {
            parentChildren = [];
            children.set(parent, parentChildren);
        }
        parentChildren.push(wrapper);
    }

    patch(ComponentWrapper.prototype, 'tus_meta_wa_discuss/static/src/js/owl_compatibility.js', {
            setParent(parent) {
/**
 * Here we have patched the code of ComponentWrapper which caused error in v16.
 */
//                if (parent instanceof Component) {
//                    throw new Error('ComponentWrapper must be used with a legacy Widget as parent');
//                }
                if (parent) {
                    registerWrapper(parent, this);
                }
                if (this.parentWidget) {
                    const parentChildren = children.get(this.parentWidget);
                    parentChildren.splice(parentChildren.indexOf(this), 1);
                }

                this.parentWidget = parent;
                if (this.node) {
                    this.node.component.parentWidget = parent;
                }
            }
    });