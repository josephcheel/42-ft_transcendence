<template>
    <div class="container-fluid d-flex h-100">
        <div class="left-panel d-flex flex-column col-md-3 p-2 bg-success">
            <UserSearch class="border border-dark bg-success mb-2" @chat-selected="handleChatSelected" />
        </div>
        <div class="main-panel d-flex flex-column flex-grow-1 ms-2">
            <MessageArea :selectedChat="selectedChat" />
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import UserSearch from './UserSearch.vue';
import MessageArea from './MessageArea.vue';

export default {
  components: {
    UserSearch,
    MessageArea
  },
  data() {
    return {
      selectedChat: null,
      username: null
    };
  },
  mounted() {
  const user = localStorage.getItem('username');
  if(user) {
    username.value = user;
  } else {
    router.push({name: 'Login'})
  }
},
  methods: {
    handleChatSelected(chat) {
      this.selectedChat = chat;
    }
  }
};
</script>