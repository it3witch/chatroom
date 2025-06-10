<!-- ChatHeader.vue - 处理聊天室头部和加入离开 -->
<template>
  <div class="chat-header">
    <div class="header-content">
      <h2>CHAT ROOM</h2>
      <user-profile @nickname-changed="$emit('nickname-changed', $event)" />
      <div class="room-selector" v-if="nickname">
        <input v-model="roomName" class="room-input" placeholder="Search for a channel..." @keyup.enter="joinRoom" />
        <button class="room-button" @click="joinRoom">
          JOIN
        </button>
        <button class="room-button" @click="leaveRoom" v-if="currentRoom">
          LEAVE
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import UserProfile from '@/components/UserProfile.vue';

export default {
  name: 'ChatHeader',
  components: {
    UserProfile
  },
  props: {
    nickname: {
      type: String,
      required: true
    },
    currentRoom: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      roomName: ''
    }
  },
  methods: {
    joinRoom() {
      if (this.roomName.trim() === '') return;
      this.$emit('join-room', this.roomName);
      this.roomName = '';
    },
    leaveRoom() {
      if (this.currentRoom) {
        this.$emit('leave-room', this.currentRoom);
      }
    }
  }
}
</script>

<style scoped>
.chat-header {
  background: #ffffff;
  padding: 1rem;
  color: #484d53;
  border-bottom: 1px solid #dee2e6;
}

.header-content {
  max-width: 900px;
  margin: 0 auto;
}

.chat-header h2 {
  margin: 0 0 1rem 0;
  font-weight: 600;
  font-size: 1.5rem;
  color: #495057;
}

.room-selector {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.room-input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  color: #212529;
  transition: all 0.3s ease;
}

.room-input::placeholder {
  color: #adb5bd;
}

.room-input:focus {
  outline: none;
  border-color: #adb5bd;
  box-shadow: 0 0 0 2px rgba(173, 181, 189, 0.2);
}

.room-button {
  background: white;
  color: #495057;
  border: 1px solid #dee2e6;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.room-button:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
  transform: translateY(-1px);
}

.room-button:active {
  transform: translateY(0);
}

@media (prefers-color-scheme: dark) {
  .chat-header {
    background: #2d2d2d;
    border-color: #3d3d3d;
  }

  .chat-header h2 {
    color: #e9ecef;
  }

  .room-input {
    background: #3d3d3d;
    border-color: #4d4d4d;
    color: #e9ecef;
  }

  .room-input::placeholder {
    color: #adb5bd;
  }

  .room-button {
    background: #3d3d3d;
    color: #e9ecef;
    border-color: #4d4d4d;
  }

  .room-button:hover {
    background: #4d4d4d;
    border-color: #5d5d5d;
  }
}
</style> 