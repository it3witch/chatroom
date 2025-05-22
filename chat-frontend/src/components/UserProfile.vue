<!-- ChatInput.vue - 处理消息输入 -->
<template>
  <div class="user-profile">
    <div class="user-info" v-if="!nickname">
      <input 
        v-model="tempNickname" 
        class="nickname-input" 
        placeholder="请输入你的昵称" 
        @keyup.enter="setNickname"
      />
      <button class="nickname-button" @click="setNickname">设置昵称</button>
    </div>
    <div class="user-display" v-else>
      <span class="nickname-display">{{ nickname }}</span>
      <button class="change-nickname" @click="resetNickname">修改昵称</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  data() {
    return {
      nickname: localStorage.getItem('nickname') || '',
      tempNickname: '',
    }
  },
  methods: {
    setNickname() {
      if (this.tempNickname.trim()) {
        this.nickname = this.tempNickname.trim();
        localStorage.setItem('nickname', this.nickname);
        this.$emit('nickname-changed', this.nickname);
      }
    },
    resetNickname() {
      this.nickname = '';
      this.tempNickname = '';
      localStorage.removeItem('nickname');
      this.$emit('nickname-changed', '');
    }
  }
}
</script>

<style scoped>
.user-profile {
  padding: 1rem;
}

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
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
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
}

.user-display {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nickname-display {
  font-size: 1.1rem;
  font-weight: 500;
  color: #495057;
}

.change-nickname {
  padding: 0.5rem 1rem;
  background: #e9ecef;
  color: #495057;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.change-nickname:hover {
  background: #dee2e6;
}

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
  .nickname-input {
    background: #3d3d3d;
    border-color: #4d4d4d;
    color: #e9ecef;
  }

  .nickname-display {
    color: #e9ecef;
  }

  .change-nickname {
    background: #3d3d3d;
    color: #e9ecef;
  }

  .change-nickname:hover {
    background: #4d4d4d;
  }
}
</style> 