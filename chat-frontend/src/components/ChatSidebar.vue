<!-- ChatSidebar.vue - 处理侧边栏和房间列表 -->
<template>
  <div class="sidebar">
    <h3>#CHAT</h3>
    <!-- 显示已加入的房间列表 -->
    <div class="joined-rooms">
      <h4>已加入房间</h4>
      <ul class="room-list" v-if="joinedRooms.length > 0">
        <li v-for="joinedRoom in joinedRooms" :key="joinedRoom" :class="{ 'active': joinedRoom === currentRoom }"
          @click="$emit('switch-room', joinedRoom)">
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
</template>

<script>
export default {
  name: 'ChatSidebar',
  props: {
    joinedRooms: {
      type: Array,
      required: true
    },
    currentRoom: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
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