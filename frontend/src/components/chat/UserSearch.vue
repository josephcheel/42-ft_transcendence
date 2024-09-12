<template>
    <div class="d-flex flex-column h-100 border border-dark bg-success">
        <div>
            <label for="nickname-input" class="form-label bg-success">New Chat</label>
                <input
                    id="nickname-input"
                    type="text"
                    v-model="nickname"
                    @keyup.enter="searchUser"
                    class="form-control"
                    placeholder="Introduce el nickname"
                />
        </div>
        <ul class="list-group flex-grow-1 overflow-auto">
          <li
            v-for="(chat, index) in chats"
            :key="index"
            class="list-group-item list-group-item-action bg-success"
            @click="selectChat(chat)"
          >
            {{ chat }}
          </li>
        </ul>
    </div>
</template>

<script setup>
    import {ref, defineEmits } from 'vue';

    const emit = defineEmits(['chat-selected']);

    const nickname = ref('');
    const chats = ref([]);

    function addChat() {
        const trimedNickname = nickname.value.trim();
        if (trimedNickname && !chats.value.includes(trimedNickname)) {
          chats.value.push(trimedNickname);
          nickname.value = '';
        }
    }

    // Función para seleccionar un chat (esto es solo un ejemplo, deberías manejar la lógica real)
    function selectChat(chat) {
      console.log(`Chat seleccionado: ${chat}`);
      emit('chat-selected', chat);
    }

    function searchUser()
    {
        console.log(nickname.value);
        addChat();
    }
</script>