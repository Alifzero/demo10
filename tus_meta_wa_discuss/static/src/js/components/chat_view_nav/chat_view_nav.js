/** @odoo-module **/

import { registerMessagingComponent } from '@mail/utils/messaging_component';
const { Component } = owl;

export class ChatViewNav extends Component {
    setup() {
        super.setup();
    }
    mounted(){
        super.mounted()
        if(this.chatWindow && this.chatWindow.thread && this.chatWindow.thread.correspondent && this.chatWindow.thread.correspondent.user){
            if(this.chatWindow.thread.isWaMsgs){
                this.onClickWhatsapp()
            }
            else{
                this.onClickLive()
            }
        }
        else{
            this.onClickWhatsapp();
        }
    }
    render(){
        super.render()
        if(this.chatWindow && this.chatWindow.thread && this.chatWindow.thread.channel && this.chatWindow.thread.channel.correspondent && this.chatWindow.thread.channel.correspondent.persona.partner && this.chatWindow.thread.channel.correspondent.persona.partner.user){
            if(this.chatWindow.thread.isWaMsgs){
                this.onClickWhatsapp()
            }
            else{
                this.onClickLive()
            }
        }
        else{
            this.onClickWhatsapp();
        }
    }
    get chatWindow() {
        var chats = this.messaging.models['ChatWindow'].all().filter(chat => chat.localId==this.props.chatWindowLocalId);
        return this.messaging && chats && chats[0];
    }
    onClickLive(){
        if(this.chatWindow && this.chatWindow.thread){
            this.chatWindow.thread.update({isWaMsgs:false})
            //this.chatWindow.thread.refresh()
        }
    }
    onClickWhatsapp(){
        if(this.chatWindow && this.chatWindow.thread){
            this.chatWindow.thread.update({isWaMsgs:true})
            //this.chatWindow.thread.refresh()
        }
    }
}

Object.assign(ChatViewNav, {
     props: {
        chatWindowLocalId: String,
    },
    template: 'tus_meta_whatsapp_base.ChatViewNav',
});

registerMessagingComponent(ChatViewNav);
