<!-- ChatMessages.vue - 处理消息显示 -->
<template>
  <div class="messages" ref="messages">
    <div v-for="message in messages" :key="message.id"
      :class="['message-row', message.type === 'system' ? 'system' : '']">
      <div class="message-content" v-if="message.type !== 'system'">
        <div class="avatar-wrapper">
          <img 
            :src="message.avatar || defaultAvatar" 
            alt="用户头像" 
            class="avatar-image"
          />
        </div>
        <div class="message-body">
          <div class="message-header">
            <span class="message-sender">{{ message.sender }}</span>
            <span class="message-time">{{ message.time }}</span>
          </div>
          <p class="message-text">{{ message.content }}</p>
        </div>
      </div>
      <div class="system-message" v-else>
        <p>{{ message.content }}</p>
        <span class="message-time">{{ message.time }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import defaultAvatarImg from '@/assets/default_avatar.jpg';

export default {
  name: 'ChatMessages',
  props: {
    messages: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      defaultAvatar: defaultAvatarImg
    }
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const messagesDiv = this.$refs.messages;
        if (messagesDiv) {
          messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
      });
    }
  },
  watch: {
    messages: {
      handler() {
        this.scrollToBottom();
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  background: #f8f9fa;
}

.message-row {
  width: 100%;
  padding: 0.5rem 0;
}

.message-content {
  display: flex;
  gap: 1rem;
}

.avatar-wrapper {
  width: 43px;
  height: 43px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.avatar-image:hover {
  transform: scale(1.05);
}

.message-body {
  flex: 1;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}

.message-sender {
  font-weight: 600;
  color: #495057;
}

.message-time {
  font-size: 0.8rem;
  color: #adb5bd;
}

.message-text {
  margin: 0;
  line-height: 1.4;
  color: #212529;
}

.system-message {
  text-align: center;
  color: #6c757d;
  font-size: 0.9rem;
  padding: 0.5rem;
  border-top: 1px solid #dee2e6;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.system-message p {
  margin: 0;
}

@media (prefers-color-scheme: dark) {
  .messages {
    background: #2d2d2d;
  }

  .message-row {
    border-color: #3d3d3d;
  }

  .message-row.sent {
    background: rgba(0, 113, 227, 0.1);
    color: #e9ecef;
  }

  .message-row.received {
    background: #3d3d3d;
    color: #e9ecef;
  }

  .message-row.system {
    background: #2d2d2d;
    color: #adb5bd;
    border-color: #3d3d3d;
  }

  .message-time {
    color: #adb5bd;
  }

  .message-sender {
    color: #e9ecef;
  }

  .message-text {
    color: #e9ecef;
  }

  .system-message {
    color: #adb5bd;
    border-color: #3d3d3d;
  }
}
</style> 