<!-- ChatInput.vue - 处理消息输入 -->
<template>
  <div class="input-area">
    <input v-model="message" class="message-input" placeholder="Message here..." @keyup.enter="sendMessage" />
    <button class="send-button" @click="sendMessage">
      Send
    </button>
  </div>
</template>

<script>
export default {
  name: 'ChatInput',
  data() {
    return {
      message: ''
    }
  },
  methods: {
    sendMessage() {
      if (this.message.trim() === '') return;
      this.$emit('send-message', this.message);
      this.message = '';
    }
  }
}
</script>

<style scoped>
.input-area {
  padding: 1.5rem;
  background: white;
  border-top: 1px solid #dee2e6;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 1rem;
  border: 1.5px solid #e9ecef;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  height: 48px;
  line-height: 1;
  display: flex;
  align-items: center;
}

.message-input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 2px rgba(0, 113, 227, 0.2);
}

.send-button {
  padding: 1rem 1.5rem;
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-button:hover {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
}

.send-button:active {
  transform: translateY(0);
  box-shadow: none;
}

@media (prefers-color-scheme: dark) {
  .input-area {
    background: #1a1a1a;
    border-color: #3d3d3d;
  }

  .message-input {
    background: #3d3d3d;
    border-color: #4d4d4d;
    color: #e9ecef;
  }
}
</style> 