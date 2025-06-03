<!-- Profile.vue - 个人中心界面 -->
<template>
  <div class="profile-container">
    <div class="profile-content">
      <div class="profile-header">
        <h2>个人中心</h2>
        <button class="back-button" @click="goBack">返回聊天室</button>
      </div>
      
      <div class="profile-section">
        <div class="avatar-section">
          <div class="avatar-wrapper">
            <img :src="avatarUrl || defaultAvatar" alt="用户头像" class="avatar-image" />
            <div class="avatar-overlay">
              <input 
                type="file" 
                ref="fileInput" 
                accept="image/*" 
                @change="handleAvatarChange" 
                style="display: none"
              />
              <button class="upload-button" @click="triggerFileInput">更换头像</button>
            </div>
          </div>
        </div>

        <div class="nickname-section">
          <div class="input-group">
            <label>昵称</label>
            <div class="nickname-input-group">
              <input 
                v-model="tempNickname" 
                class="nickname-input" 
                placeholder="请输入你的昵称" 
              />
              <button class="save-button" @click="saveNickname">保存</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import defaultAvatarImg from '@/assets/default_avatar.jpg';

export default {
  name: 'Profile',
  data() {
    return {
      nickname: localStorage.getItem('nickname') || '',
      tempNickname: localStorage.getItem('nickname') || '',
      avatarUrl: localStorage.getItem('avatar') || '',
      defaultAvatar: defaultAvatarImg
    }
  },
  methods: {
    goBack() {
      this.$router.push('/chat');
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('avatar', file);
        
        try {
          const response = await axios.post('/api/user/avatar', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            withCredentials: true
          });
          
          if (response.data.success) {
            this.avatarUrl = response.data.avatar_url;
            localStorage.setItem('avatar', this.avatarUrl);
          } else {
            alert('头像上传失败：' + response.data.message);
          }
        } catch (error) {
          console.error('上传头像失败:', error);
          alert('上传头像失败，请稍后重试');
        }
      }
    },
    async saveNickname() {
      if (this.tempNickname.trim()) {
        try {
          const response = await axios.post('/api/user/nickname', {
            nickname: this.tempNickname.trim()
          }, { withCredentials: true });
          
          if (response.data.success) {
            this.nickname = this.tempNickname.trim();
            localStorage.setItem('nickname', this.nickname);
            this.$emit('nickname-changed', this.nickname);
            alert('昵称更新成功');
          } else {
            alert('更新昵称失败：' + response.data.message);
          }
        } catch (error) {
          console.error('更新昵称失败:', error);
          alert('更新昵称失败，请稍后重试');
        }
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  width: 100%;
  max-width: 1500px;
  height: 90vh;
  margin: 0 auto;
  background: #1e90ff;
  border-radius: 5px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-content {
  padding: 2rem;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-header h2 {
  margin: 0;
  color: #495057;
  font-size: 1.5rem;
}

.back-button {
  padding: 0.8rem 1.5rem;
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
}

.profile-section {
  max-width: 600px;
  margin: 0 auto;
}

.avatar-section {
  text-align: center;
  margin-bottom: 2rem;
}

.avatar-wrapper {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  padding: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.upload-button {
  background: #0071e3;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  width: 100%;
}

.nickname-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: 500;
}

.nickname-input-group {
  display: flex;
  gap: 1rem;
}

.nickname-input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.nickname-input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 2px rgba(0, 113, 227, 0.2);
}

.save-button {
  padding: 0.8rem 1.5rem;
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-button:hover {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
}

@media (prefers-color-scheme: dark) {
  .profile-content {
    background: rgba(30, 30, 30, 0.9);
  }

  .profile-header h2 {
    color: #e9ecef;
  }

  .nickname-section {
    background: #2c2c2e;
  }

  .input-group label {
    color: #e9ecef;
  }

  .nickname-input {
    background: #3d3d3d;
    border-color: #4d4d4d;
    color: #e9ecef;
  }
}
</style> 