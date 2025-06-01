<template>
  <div class="chat-container">
    <chat-sidebar 
      :joined-rooms="joinedRooms"
      :current-room="room"
      @switch-room="switchRoom"
    />
    <div class="main-content">
      <chat-header 
        :nickname="nickname"
        @nickname-changed="handleNicknameChange"
        @join-room="joinRoom"
        @leave-room="leaveRoom"
      />

      <chat-messages :messages="messages" />

      <chat-input 
        v-if="nickname"
        @send-message="sendMessage"
      />
    </div>

    <online-users 
      :online-users="onlineUsers"
      :current-user="user"
    />
  </div>
</template>

<script>
import socket from '@/socket';
import axios from 'axios';
import ChatSidebar from '@/components/ChatSidebar.vue';
import ChatHeader from '@/components/ChatHeader.vue';
import ChatMessages from '@/components/ChatMessages.vue';
import ChatInput from '@/components/ChatInput.vue';
import OnlineUsers from '@/components/OnlineUsers.vue';

export default {
  components: {
    ChatSidebar,
    ChatHeader,
    ChatMessages,
    ChatInput,
    OnlineUsers
  },
  data() {
    return {
      messages: [],
      room: '',
      nickname: localStorage.getItem('nickname') || '',
      joinedRooms: [],
      onlineUsers: [],
      loading: false,
      user: null,
      defaultAvatar: 'https://via.placeholder.com/50'
    };
  },
  methods: {
    addPrivateRoom(roomName, otherUser) {
      if (!this.joinedRooms.includes(roomName)) {
        this.joinedRooms.push(roomName);
      }
    },

    handleNicknameChange(newNickname) {
      this.nickname = newNickname;
    },
    sendMessage(message) {
      if (!message.trim()) return;
      
      const messageData = {
        id: Date.now(),
        content: message,
        sender: this.nickname,
        time: new Date().toLocaleTimeString(),
        type: 'message',
        avatar: localStorage.getItem('avatar') || this.defaultAvatar
      };
      
      // 发送消息到服务器
      socket.emit('sendMsg', {
        msg: message,
        nickname: this.nickname,
        time: messageData.time,
        room: this.room
      });
      
      // 添加到本地消息列表
      this.messages.push(messageData);
    },
    async joinRoom(roomName) {
      if (roomName.trim() === '') return;

      socket.emit('joinRoom', {
        room: roomName,
        nickname: this.nickname
      });
      this.messages = [];
      this.room = roomName;

      try {
        if (this.user) {
          await axios.post('/api/rooms/join', {
            room: roomName
          }, { withCredentials: true });

          await this.fetchJoinedRooms();
        } else {
          if (!this.joinedRooms.includes(roomName)) {
            this.joinedRooms.push(roomName);
            localStorage.setItem('joinedRooms', JSON.stringify(this.joinedRooms));
          }
        }
      } catch (error) {
        console.error('保存房间失败:', error);
      }
    },
    async leaveRoom(roomName) {
      if (roomName.trim() === '') return;

      socket.emit('leaveRoom', {
        room: roomName,
        nickname: this.nickname
      });
      this.messages = [];

      try {
        if (this.user) {
          await axios.post('/api/rooms/leave', {
            room: roomName
          }, { withCredentials: true });

          await this.fetchJoinedRooms();
        } else {
          const index = this.joinedRooms.indexOf(roomName);
          if (index !== -1) {
            this.joinedRooms.splice(index, 1);
            localStorage.setItem('joinedRooms', JSON.stringify(this.joinedRooms));
          }
        }
      } catch (error) {
        console.error('更新房间失败:', error);
      }

      this.room = '';
    },
    switchRoom(roomName) {
      if (this.room === roomName) return;

      if (this.room) {
        socket.emit('leaveRoom', {
          room: this.room,
          nickname: this.nickname
        });
      }

      this.messages = [];
      this.room = roomName;
      socket.emit('joinRoom', {
        room: roomName,
        nickname: this.nickname
      });

      if (!this.user) {
        localStorage.setItem('lastActiveRoom', roomName);
      }
    },
    async fetchJoinedRooms() {
      if (!this.user) return;

      this.loading = true;
      try {
        const response = await axios.get('/api/user/rooms', {
          withCredentials: true
        });

        if (response.data.success) {
          const roomNames = response.data.rooms.map(room => room.name);
          this.joinedRooms = roomNames;

          if (!this.room && this.joinedRooms.length > 0) {
            const lastActiveRoom = localStorage.getItem('lastActiveRoom');
            if (lastActiveRoom && this.joinedRooms.includes(lastActiveRoom)) {
              this.switchRoom(lastActiveRoom);
            } else {
              this.switchRoom(this.joinedRooms[0]);
            }
          }
        }
      } catch (error) {
        console.error('获取房间列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    loadUserData() {
      const userData = localStorage.getItem('user');
      if (userData) {
        try {
          this.user = JSON.parse(userData);
        } catch (e) {
          console.error('解析用户数据失败:', e);
          this.user = null;
        }
      }
    }
  },
  async created() {
    this.loadUserData();

    try {
      await axios.get('/api/user/rooms', { withCredentials: true });
    } catch (error) {
      console.error('Session检查失败:', error);
    }

    if (this.user) {
      await this.fetchJoinedRooms();
    } else {
      const storedRooms = localStorage.getItem('joinedRooms');
      if (storedRooms) {
        try {
          this.joinedRooms = JSON.parse(storedRooms);
        } catch (e) {
          console.error('解析本地存储的房间列表失败:', e);
          this.joinedRooms = [];
        }
      }
    }

    socket.on('sendToAll', (message) => {
      if (message.user !== socket.id) {
        this.messages.push({
          id: Date.now(),
          sender: message.nickname,
          content: message.msg,
          time: message.time || new Date().toLocaleTimeString(),
          type: 'message',
          avatar: localStorage.getItem('avatar') || this.defaultAvatar
        });
      }
    });

    socket.on('roomJoined', (message) => {
      if (message.type === 'system') {
        this.messages.push({
          id: Date.now(),
          type: 'system',
          content: message.message,
          time: new Date().toLocaleTimeString()
        });
        
        if (this.user && message.message.includes('加入房间')) {
          this.fetchJoinedRooms();
        }
      }
    });

    socket.on('roomLeft', (message) => {
      this.messages.push({
        id: Date.now(),
        type: 'system',
        content: `${message.nickname} 离开了房间`,
        time: new Date().toLocaleTimeString()
      });
    });

    socket.on('roomLeftPersonal', (message) => {
      if (this.user) {
        this.fetchJoinedRooms();
      }
    });

    socket.on('update_online_users', (onlineUsers) => {
      if (this.user) {
        this.onlineUsers = onlineUsers;
      }
    });

    socket.on('private_chat_invite', (data) => {
    this.addPrivateRoom(data.room, data.from);
    });

    socket.on('private_chat_started', (data) => {
    this.addPrivateRoom(data.room, data.to);
    });
    
    window.addEventListener('load', () => {
      if (this.room) {
        socket.emit('joinRoom', {
          room: this.room,
          nickname: this.nickname
        });
      }
    });
  }
};
</script>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 1500px;
  height: 90vh;
  margin: 0 auto;
  display: flex;
  flex-direction: row;
  background: #1e90ff;
  border-radius: 5px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@media (prefers-color-scheme: dark) {
  .chat-container {
    background: #1a1a1a;
  }
}
</style>
