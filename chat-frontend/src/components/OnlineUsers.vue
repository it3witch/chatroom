<!-- OnlineUsers.vue - 处理在线用户列表 -->
<template>
  <div class="online-user">
    <h3># Online Users ({{ onlineUsers.length}})</h3>
    <ul class="user-list" v-if="onlineUsers.length > 0">
      <li v-for="onlineUser in onlineUsers" :key="onlineUser" v-if="onlineUser !== currentUser">
        <button class="user-button" @click="startPrivateChat(onlineUser)">
          {{ onlineUser }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import socket from '@/socket';

export default {
  name: 'OnlineUsers',
  props: {
    onlineUsers: {
      type: Array,
      required: true
    },
    currentUser: {
      type: Array,
      required: true
    }
  },
  methods: {
    startPrivateChat(user) {
      console.log('准备发起私聊：', user);
      socket.emit('start_private_chat', { to: user, from: this.currentUser.nickname });
      // 这里将来写具体的私聊逻辑
    }
  }
}
</script>

<style scoped>
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

.user-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-list li {
  padding: 6px;
  font-size: 14px;
}

.user-button {
  background: none;
  border: none;
  color: #e9ecef;
  padding: 10px 50px;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.3s;
}

.user-button:hover {
  color: #4695e4;
}
</style> 