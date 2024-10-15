<template>
    <div>
        <modal name="messageModal" class="modalContents">
            <div class="subtitleArea">
                <span class="subtitle">{{$t("message.title")}}</span>
            </div>
            <div class="messageBody">
                <template v-if="messageCode=='aithub_logout'">
                    <h4>{{$t("message.aithub_logout")}}</h4>
                </template>
                <template v-else-if="messageCode=='aithub_logout_whit_error'">
                    <h4>{{$t("message.aithub_logout_whit_error")}}</h4>
                </template>
                <template v-else-if="messageCode=='aithub_E01'">
                    <h4>{{$t("message.aithub_E01_unableToConnect")}}</h4>
                </template>
                <template v-else-if="messageCode=='aithub_E02'">
                    <h4>{{$t("message.aithub_E02_reLogin")}}</h4>
                </template>
                <template v-else>
                    <h4>{{$t("message.aithub_E99_unexpectedErr")}}</h4>
                </template>

                <template v-if="messageText != ''">
                    <span>{{ messageText }}</span>
                </template>
            </div>
            <div id="closeModal" class="closeModal" @click="close">
                ×
            </div>
        </modal>
    </div>
</template>

<script>
export default {
    data() {
        return {
            messageCode: '',
            messageText: ''
        }
    },
    methods: {
        show(messageCode, messageText) {
            if (messageCode !== undefined) {
                this.messageCode = messageCode;
            }
            if (messageText !== undefined) {
                this.messageCode = messageText;
            }
            this.$modal.show("messageModal");
        },
        hide() {
            this.$modal.hide("messageModal");
        },
        close() {
            this.hide();
        },
    }
}
</script>

<style scoped>
.subtitleArea {
    background-color: #dc722b;
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    margin: 0;
    width: 100%;
    height: 3rem;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.messageBody {
    margin-top: 10%;
    margin-left: 10%;
    width: 80%;
}

.modalContents>>>.vm--modal {
    position: absolute !important;
    top: 10% !important;
    width: 32% !important;
    height: 52% !important;
    background-color: #f0f0f0;
    border-radius: 10px;
    overflow-y: auto;
}
</style>