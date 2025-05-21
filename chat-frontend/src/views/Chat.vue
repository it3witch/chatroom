<template>
  <div class="chat-container">
    <div class="sidebar">
      <h3>#CHAT</h3>
      <!-- 显示已加入的房间列表 -->
      <div class="joined-rooms">
        <h4>已加入房间</h4>
        <ul class="room-list" v-if="joinedRooms.length > 0">
          <li v-for="joinedRoom in joinedRooms" :key="joinedRoom" :class="{ 'active': joinedRoom === room }"
            @click="switchRoom(joinedRoom)">
            <span class="room-icon">#</span>
            <span class="room-name">{{ joinedRoom }}</span>
          </li>
        </ul>
        <div class="no-rooms" v-else>
          <p>暂无加入的房间</p>
          <p class="hint">输入房间名并点击JOIN加入</p>
        </div>
      </div>
    </div>
    <div class="main-content">
      <div class="chat-header">
        <div class="header-content">
          <h2>CHAT ROOM</h2>
          <user-profile @nickname-changed="handleNicknameChange" />
          <div class="room-selector" v-if="nickname">
            <input v-model="room" class="room-input" placeholder="Search for a channel..." @keyup.enter="joinRoom" />
            <button class="room-button" @click="joinRoom">
              JOIN
            </button>
            <button class="room-button" @click="leaveRoom">
              LEAVE
            </button>
          </div>
        </div>
      </div>

      <div class="messages" ref="messages">
        <div v-for="message in messages" :key="message.id"
          :class="['message-row', message.type === 'system' ? 'system' : '']">
          <div class="message-content" v-if="message.type !== 'system'">
            <div class="avatar-placeholder"></div>
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

      <div class="input-area" v-if="nickname">
        <input v-model="newMessage" class="message-input" placeholder="Message here..." @keyup.enter="sendMessage" />
        <button class="send-button" @click="sendMessage">
          Send
        </button>
      </div>
    </div>

    <div class="online-user">
      <h3># Online Users ({{ onlineUsers.length}})</h3>
      <ul class="user-list" v-if="onlineUsers.length > 0">
        <li v-for="onlineUser in onlineUsers" :key="onlineUser" v-if="onlineUser !== user">
          {{ onlineUser }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import socket from '@/socket';
import UserProfile from '@/components/UserProfile.vue';
import axios from 'axios';

export default {
  components: {
    UserProfile
  },
  data() {
    return {
      messages: [],
      newMessage: '',
      room: '',
      nickname: localStorage.getItem('nickname') || '',
      joinedRooms: [],
      onlineUsers: [],
      loading: false,
      user: null
    };
  },
  methods: {
    handleNicknameChange(newNickname) {
      this.nickname = newNickname;
    },
    sendMessage() {
      if (this.newMessage.trim() === '') return;

      const message = {
        room: this.room,
        msg: this.newMessage,
        nickname: this.nickname
      };
      socket.emit('sendMsg', message);

      this.messages.push({
        id: Date.now(),
        sender: this.nickname,
        content: this.newMessage,
        time: new Date().toLocaleTimeString()
      });

      this.newMessage = '';
      this.scrollToBottom();
    },
    async joinRoom() {
      if (this.room.trim() === '') return;

      // 加入房间
      socket.emit('joinRoom', {
        room: this.room,
        nickname: this.nickname
      });
      this.messages = [];

      try {
        // 如果用户已登录，将房间关系保存到数据库
        if (this.user) {
          // 调用API保存房间关系
          await axios.post('/api/rooms/join', {
            room: this.room
          }, { withCredentials: true });

          // 重新获取房间列表
          await this.fetchJoinedRooms();
        } else {
          // 未登录用户仍使用本地存储
          if (!this.joinedRooms.includes(this.room)) {
            this.joinedRooms.push(this.room);
            localStorage.setItem('joinedRooms', JSON.stringify(this.joinedRooms));
          }
        }
      } catch (error) {
        console.error('保存房间失败:', error);
      }
    },
    async leaveRoom() {
      if (this.room.trim() === '') return;

      // 离开房间
      socket.emit('leaveRoom', {
        room: this.room,
        nickname: this.nickname
      });
      this.messages = [];

      try {
        // 如果用户已登录，更新数据库中的房间关系
        if (this.user) {
          // 调用API删除房间关系
          await axios.post('/api/rooms/leave', {
            room: this.room
          }, { withCredentials: true });

          // 重新获取房间列表
          await this.fetchJoinedRooms();
        } else {
          // 未登录用户仍使用本地存储
          const index = this.joinedRooms.indexOf(this.room);
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
      // 如果已经在该房间，不做任何操作
      if (this.room === roomName) return;

      // 如果当前在其他房间，先离开当前房间的socket连接
      if (this.room) {
        socket.emit('leaveRoom', {
          room: this.room,
          nickname: this.nickname
        });
      }

      // 清空当前房间的消息
      this.messages = [];

      // 更新当前房间并加入
      this.room = roomName;
      socket.emit('joinRoom', {
        room: roomName,
        nickname: this.nickname
      });

      // 保存最后活跃的房间信息
      if (this.user) {
        // 如果用户已登录，这个信息会由后端处理
      } else {
        // 未登录用户使用本地存储
        localStorage.setItem('lastActiveRoom', roomName);
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const messagesDiv = this.$refs.messages;
        if (messagesDiv) {
          messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
      });
    },
    async fetchJoinedRooms() {
      if (!this.user) return;

      this.loading = true;
      try {
        console.log('开始获取用户已加入的房间...');
        const response = await axios.get('/api/user/rooms', {
          withCredentials: true
        });

        console.log('获取到的房间数据:', response.data);

        if (response.data.success) {
          // 将从数据库获取的房间列表转换为与当前格式兼容的数组
          const roomNames = response.data.rooms.map(room => room.name);
          console.log('处理后的房间列表:', roomNames);

          // 保存房间列表
          this.joinedRooms = roomNames;

          // 如果当前没有选中房间但有可用房间，选择第一个房间
          if (!this.room && this.joinedRooms.length > 0) {
            const lastActiveRoom = localStorage.getItem('lastActiveRoom');
            if (lastActiveRoom && this.joinedRooms.includes(lastActiveRoom)) {
              console.log(`恢复上次活跃的房间: ${lastActiveRoom}`);
              this.switchRoom(lastActiveRoom);
            } else {
              console.log(`选择第一个可用房间: ${this.joinedRooms[0]}`);
              this.switchRoom(this.joinedRooms[0]);
            }
          }
        } else {
          console.error('获取房间列表失败:', response.data.message);
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
    // 加载用户数据
    this.loadUserData();
    console.log('用户数据:', this.user);

    // 检查用户登录状态
    try {
      const sessionCheckResponse = await axios.get('/api/user/rooms', { withCredentials: true });
      console.log('Session检查结果:', sessionCheckResponse.data);
    } catch (error) {
      console.error('Session检查失败:', error);
    }

    // 如果用户已登录，从数据库获取已加入的房间
    if (this.user) {
      await this.fetchJoinedRooms();
    } else {
      // 未登录用户使用本地存储
      const storedRooms = localStorage.getItem('joinedRooms');
      if (storedRooms) {
        try {
          this.joinedRooms = JSON.parse(storedRooms);
          console.log('从本地存储恢复房间列表:', this.joinedRooms);
        } catch (e) {
          console.error('解析本地存储的房间列表失败:', e);
          this.joinedRooms = [];
        }
      }
    }

    // 监听消息
    socket.on('sendToAll', (message) => {
      console.log('收到消息:', message);  // 添加调试日志
      if (message.user !== socket.id) {
        this.messages.push({
          id: Date.now(),
          sender: message.nickname,
          content: message.msg,
          time: message.time || new Date().toLocaleTimeString()
        });
        this.scrollToBottom();
      }
    });

    // 监听房间加入事件
    socket.on('roomJoined', (message) => {
      console.log('收到房间加入消息:', message);  // 添加调试日志
      
      // 如果是系统消息，直接添加到消息列表
      if (message.type === 'system') {
        this.messages.push({
          id: Date.now(),
          type: 'system',
          content: message.message,
          time: new Date().toLocaleTimeString()
        });
        
        // 如果是加入房间成功的消息，刷新房间列表
        if (this.user && message.message.includes('加入房间')) {
          this.fetchJoinedRooms();
        }
        
        this.scrollToBottom();
      }
    });

    // 监听房间离开事件
    socket.on('roomLeft', (message) => {
      console.log(`${message.nickname} has left room ${message.room}`);
      this.messages.push({
        id: Date.now(),
        type: 'system',
        content: `${message.nickname} 离开了房间`,
        time: new Date().toLocaleTimeString()
      });
      this.scrollToBottom();
    });

    // 监听个人房间离开事件
    socket.on('roomLeftPersonal', (message) => {
      console.log(`You left room ${message.room}`);

      // 如果是自己离开房间，刷新房间列表
      if (this.user) {
        this.fetchJoinedRooms();
      }
    });

    // 监听在线用户列表
    socket.on('update_online_users', (onlineUsers) => {
      if (this.user) {
        this.onlineUsers = onlineUsers;  // 用后端传来的用户列表更新数据
      }
    })
    
    // 重新连接时恢复房间状态
    window.addEventListener('load', () => {
      // 如果在刷新前已加入房间，则重新加入
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

.online-user {
  width: 200px;
  height: 100%;
  background: #232222;
  border-right: 1px solid #232323;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  flex-shrink: 0;
  border-radius: 5px;
}

.sidebar {
  width: 200px;
  height: 100%;
  background: #232222;
  border-right: 1px solid #232323;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  flex-shrink: 0;
  border-radius: 5px;
}

.sidebar h3 {
  margin: 0 0 20px 0;
  color: #ffffff;
  font-size: 1.2rem;
}

/* 已加入房间列表样式 */
.joined-rooms {
  width: 100%;
  padding: 0 15px;
}

.joined-rooms h4 {
  color: #adb5bd;
  font-size: 0.9rem;
  margin-bottom: 10px;
  font-weight: 500;
}

.room-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 100%;
}

.room-list li {
  padding: 8px 12px;
  border-radius: 4px;
  color: #e9ecef;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
}

.room-icon {
  color: #adb5bd;
  font-weight: bold;
}

.room-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.room-list li:hover {
  background: rgba(42, 42, 42, 0.1);
}

.room-list li.active {
  background: #2c2c2c;
  color: white;
}

.room-list li.active .room-icon {
  color: white;
}

.user-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-list li {
  padding: 6px;
  font-size: 14px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

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

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

.nickname-input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  color: #212529;
  transition: all 0.3s ease;
}

.nickname-input:focus {
  outline: none;
  border-color: #adb5bd;
  box-shadow: 0 0 0 2px rgba(173, 181, 189, 0.2);
}

.nickname-button {
  padding: 0.8rem 1.5rem;
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nickname-button:hover {
  background: #0071e3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
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

.avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  background: #e9ecef;
  flex-shrink: 0;
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

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
  .chat-container {
    background: #1a1a1a;
  }

  .chat-header {
    background: #2d2d2d;
    border-color: #3d3d3d;
  }

  .chat-header h2 {
    color: #e9ecef;
  }

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

  .input-area {
    background: #1a1a1a;
    border-color: #3d3d3d;
  }

  .message-input {
    background: #3d3d3d;
    border-color: #4d4d4d;
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

  .nickname-input {
    background: #3d3d3d;
    border-color: #4d4d4d;
    color: #e9ecef;
  }

  .messages {
    background: #2d2d2d;
  }

  .avatar-placeholder {
    background: #3d3d3d;
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

/* 删除旧的气泡样式 */
.message {
  display: none;
}

.message-row.sent,
.message-row.received {
  background: transparent;
}

.no-rooms {
  padding: 10px;
  text-align: center;
  color: #adb5bd;
  font-size: 0.85rem;
}

.no-rooms .hint {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 5px;
}
</style>
