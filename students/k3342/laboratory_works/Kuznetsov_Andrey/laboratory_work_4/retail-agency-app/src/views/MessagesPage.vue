<template>
  <HeaderLoader :currentPath="currentPath" />

  <div class="container">
    <main role="main">
      <section class="dialog-list" aria-labelledby="dialogSection">
        <h2 id="dialogSection" class="sr-only">Dialogs</h2>
        <ul id="dialogs" role="list" aria-live="polite">
          <li
            v-for="dialog in dialogs"
            :key="dialog.id"
            class="dialog-item"
            @click="openChat(dialog.id, dialog.owner)"
          >
            {{ dialog.owner }}
          </li>
        </ul>
      </section>

      <section class="message-container" id="message-container" aria-labelledby="chatHeader">
        <h2 id="chatHeader" aria-live="polite">
          Chat with <span id="chat-owner">{{ currentDialogOwner || 'Select a dialog' }}</span>
        </h2>

        <div class="messages" id="messages" role="region" aria-live="polite">
          <div
            v-for="message in messages"
            :key="message.id"
            class="message"
            :class="message.sender"
          >
            {{ message.text }}
          </div>
        </div>

        <div class="message-input">
          <input
            v-model="messageText"
            type="text"
            placeholder="Type your message here..."
            id="message-input"
            aria-label="Message input"
          />
          <button @click="sendMessage" aria-label="Send message">Send</button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import HeaderLoader from "@/components/HeaderLoader.vue";
import { API_BASE_URL } from "@/config/config.js";

export default {
  name: "MessagesPage",
  components: {
    HeaderLoader,
  },
  data() {
    return {
      currentPath: "/messages",
      dialogs: [], 
      messages: [], 
      messageText: "",
      currentDialogId: null, 
      currentDialogOwner: null,
    };
  },
  async created() {
    await this.loadDialogs();
    const isAuthenticated = localStorage.getItem("isAuthenticated");
    if (!isAuthenticated) {
      this.$router.push({ name: 'Auth' }); 
      return;
    }
  },
  methods: {
    async loadDialogs() {
      try {
        const response = await fetch(`${API_BASE_URL}/dialogs`);
        const dialogs = await response.json();
        this.dialogs = dialogs;
      } catch (error) {
        console.error("Error loading dialogs:", error);
      }
    },

    async openChat(dialogId, owner) {
      this.currentDialogOwner = owner;
      this.currentDialogId = dialogId;
      await this.loadMessages(dialogId);
    },

    async loadMessages(dialogId) {
      try {
        const response = await fetch(`${API_BASE_URL}/messages?dialogId=${dialogId}`);
        const messages = await response.json();
        this.messages = messages;
      } catch (error) {
        console.error("Error loading messages:", error);
      }
    },

    async sendMessage() {
      if (!this.messageText || !this.currentDialogId) {
        alert("Please select a dialog and enter a message.");
        return;
      }

      const newMessage = {
        dialogId: this.currentDialogId,
        sender: "user",
        text: this.messageText,
      };

      try {
        await fetch(`${API_BASE_URL}/messages`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newMessage),
        });

        this.messages.push({ ...newMessage, id: Date.now() }); 
        this.messageText = "";
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },
  },
};
</script>

<style scoped>
@import url('../assets/css/search.css');
@import url('../assets/css/messages.css');
</style>
