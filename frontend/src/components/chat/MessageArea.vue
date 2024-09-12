<template>
  <div class="d-flex flex-column h-100 border border-dark bg-light">
    <!-- Ventana de mensajes -->
    <div class="message-window flex-grow-1 overflow-auto border p-2 mb-2">
      <div v-if="selectedChat">
        <div v-for="(msg, index) in messages[selectedChat]" :key="index" class="message text-start">
          <strong>{{ msg.sender }}:</strong> {{ msg.text }}
        </div>
      </div>
      <div v-else>
        <div class="alert alert-info">
          Selecciona o crea un chat para ver los mensajes.
        </div>
      </div>
    </div>

    <div class="d-flex">
      <input
        type="text"
        v-model="newMessage"
        @keyup.enter="sendMessage"
        class="form-control me-2"
        placeholder="Escribe un mensaje..."
      />
      <button class="btn btn-primary" @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  selectedChat: String
});

const messages = ref({});

const newMessage = ref('');

// Función para enviar un mensaje
function sendMessage() {
  if (newMessage.value.trim() && props.selectedChat) {
    if (!messages.value[props.selectedChat]) {
      messages.value[props.selectedChat] = [];
    }
    messages.value[props.selectedChat].push({
      sender: 'Tú',
      text: newMessage.value.trim()
    });
    newMessage.value = ''; // Limpiar el campo de input
  }
}
</script>
