/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";
import { attr, many, one } from '@mail/model/model_field';
export const X2M_TYPES = ["one2many", "many2many"];

registerPatch({
    name: 'User',

        modelMethods: {
            /**
             * @param {Object} data
             * @returns {Object}
             */
            convertData(data) {
                const data2 = this._super(data);
                // relation
                if ('user_id' in data) {
                    if (!data.user_id) {
                        data2.user = unlinkAll();
                    } else {
                        let user = {};
                        if (Array.isArray(data.user_id)) {
                            user = {
                                id: data.user_id[0],
                                display_name: data.user_id[1],
                            };
                        } else {
                            user = {
                                id: data.user_id,
                            };
                        }
                        user.isInternalUser = data.is_internal_user;
                        user.isWhatsappUser = data.is_whatsapp_user;
                        user.not_send_msgs_btn_in_chatter = insertAndReplace(data.not_send_msgs_btn_in_chatter.map(attachmentData =>
                                this.messaging.models['ir.model'].convertData(attachmentData)
                            ));
                        user.not_wa_msgs_btn_in_chatter = insertAndReplace(data.not_wa_msgs_btn_in_chatter.map(attachmentData =>
                                this.messaging.models['ir.model'].convertData(attachmentData)
                            ));
                        data2.user = insert(user);
                    }
                }

                return data2;
            },
        },
        recordMethods: {
            /**
             * @override
             */
            async getChat() {
                if (!this.user && !this.hasCheckedUser) {
                    await this.partner.checkIsUser();
                    if (!this.exists()) {
                        return;
                    }
                }
                // prevent chatting with non-users

                if (!this.user) {
    ////                    var threads = this.messaging.models['Thread'].all().filter(thread => thread.localId==this.props.localId);
    //                    let chat = this.messaging.models['Thread'].all().filter(thread =>
    //                    thread.channel_type === 'chat' &&
    //                    thread.correspondent === this &&
    //                    thread.model === 'mail.channel' &&
    //                    thread.public === 'private'
    //                );
                    let chat = this.partner.dmChatWithCurrentPartner;
                    if (!chat || !chat.thread.isPinned) {
                        // if chat is not pinned then it has to be pinned client-side
                        // and server-side, which is a side effect of following rpc
                        chat = await this.messaging.models['Channel'].performRpcCreateChat({
                            partnerIds: [this.partner.id],
                        });
                        if (!this.exists()) {
                            return;
                        }
                    }
                    if (!chat) {
                        this.messaging.notify({
                        message: this.env._t("An unexpected error occurred during the creation of the chat."),
                        type: 'warning',
                    });
                        return;
                    }
                    return chat;
                }
                return this.user.getChat();
             },
      },
        fields: {
            isWhatsappUser: attr(),
//            not_send_msgs_btn_in_chatter: many2many('ir.model', {
//            }),
//            not_wa_msgs_btn_in_chatter: many2many('ir.model', {
//            })
        },
});