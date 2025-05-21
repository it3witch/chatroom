<template>
  <div class="content">
      <div class="wrapper">
          <div class="form-wrapper">
              <!-- 登录表单 -->
              <div class="login-form" v-show="isLoginFormVisible">
                  <div class="tips">
                      <h1>Login in this platform.</h1>
                      <span>No account?</span>
                      <span class="signup-into" @click="toggleForm">Create</span>
                  </div>
                  <div class="form-wrapper">
                      <div class="input-wrapper user">
                          <input type="text" class="inputs" v-model="username" placeholder="..." />
                      </div>
                      <div class="input-wrapper pwd">
                          <input type="password" class="inputs" v-model="password" placeholder="..." />
                      </div>
                      <div class="error-message" v-if="errorMsg">{{ errorMsg }}</div>
                      <div class="btn-wrapper">
                          <button class="form-btn login-btn" @click="login">Login</button>
                      </div>
                  </div>
              </div>

              <!-- 注册表单 -->
              <div class="signup-form" v-show="!isLoginFormVisible">
                  <div class="tips">
                      <h1>Create new account.</h1>
                      <span>Already A Member?</span>
                      <span class="login-into" @click="toggleForm">Log in</span>
                  </div>
                  <div class="form-wrapper">
                      <div class="input-wrapper user">
                          <input type="text" class="inputs" v-model="username" placeholder="..." />
                      </div>
                      <div class="input-wrapper pwd">
                          <input type="password" class="inputs" v-model="password" placeholder="..." />
                      </div>
                      <div class="input-wrapper nickname">
                          <input type="text" class="inputs" v-model="nickname" placeholder="..." />
                      </div>
                      <div class="error-message" v-if="errorMsg">{{ errorMsg }}</div>
                      <button class="form-btn" @click="register">Create account</button>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLoginFormVisible: true,
      username: '',
      password: '',
      nickname: '',
      errorMsg: '',
      isAnimating: false,
    };
  },
  methods: {
    toggleForm() {
      if (this.isAnimating) return;
      
      this.isAnimating = true;
      
      const currentForm = this.isLoginFormVisible ? 
                           document.querySelector('.login-form') : 
                           document.querySelector('.signup-form');
      
      currentForm.style.opacity = '0';
      currentForm.style.transform = 'translateY(-30px)';
      
      setTimeout(() => {
        this.username = '';
        this.password = '';
        this.nickname = '';
        this.errorMsg = '';
        
        this.isLoginFormVisible = !this.isLoginFormVisible;
        
        setTimeout(() => {
          const newForm = this.isLoginFormVisible ? 
                         document.querySelector('.login-form') : 
                         document.querySelector('.signup-form');
          
          newForm.style.opacity = '1';
          newForm.style.transform = 'translateY(0)';
          
          this.isAnimating = false;
        }, 100);
      }, 300);
    },
    async register() {
      // 表单验证
      if (!this.username || !this.password) {
        this.errorMsg = '请填写所有必填字段';
        return;
      }
      
      try {
        // 注册请求
        const response = await axios.post('/api/register', {
          username: this.username,
          password: this.password,
          nickname: this.nickname || this.username
        }, { withCredentials: true });
        
        if (response.data.success) {
          // 注册成功后自动切换到登录
          this.isLoginFormVisible = true;
          this.errorMsg = '';
          alert('注册成功，请登录');
        } else {
          this.errorMsg = response.data.message;
        }
      } catch (error) {
        console.error('请求错误:', error);
        this.errorMsg = '服务器错误，请稍后再试';
      }
    },
    async login() {
      // 表单验证
      if (!this.username || !this.password) {
        this.errorMsg = '请填写所有必填字段';
        return;
      }
      
      try {
        // 登录请求
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password
        }, { withCredentials: true });
        
        if (response.data.success) {
          // 存储用户信息
          localStorage.setItem('user', JSON.stringify(response.data.user));
          localStorage.setItem('nickname', response.data.user.nickname);
          
          // 登录成功后，先获取房间列表
          try {
            console.log('登录成功，尝试获取房间列表');
            const roomsResponse = await axios.get('/api/user/rooms', { withCredentials: true });
            console.log('登录后获取的房间列表:', roomsResponse.data);
          } catch (error) {
            console.error('登录后获取房间列表失败:', error);
          }
          
          // 跳转到聊天页面
          this.$router.push('/chat');
        } else {
          this.errorMsg = response.data.message;
        }
      } catch (error) {
        console.error('请求错误:', error);
        this.errorMsg = '服务器错误，请稍后再试';
      }
    }
  }
};
</script>

<style scoped>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.error-message {
  color: #ff4d4f;
  font-size: 0.9rem;
  margin: 5px 0;
  margin-left: 20px;
}

.content {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(to right, #374357, #1f2b3e);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.content .wrapper {
  width: 70%;
  height: 80%;
  border-radius: 20px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background-image: linear-gradient(to right top, rgba(40, 42, 55, 0.9) 0%, rgba(40, 42, 55, 0.7) 20%, rgba(40, 42, 55, 0.3) 60%, rgba(40, 42, 55, 0.2) 100%), url('@/assets/bg1.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 80px;
}

.content .wrapper .form-wrapper {
  width: 100%;
  height: 50vh;
  position: relative;
  top: -10px;
}

.content .wrapper .form-wrapper .login-form,
.content .wrapper .form-wrapper .signup-form {
  position: absolute;
  transition: all 0.3s ease-in-out;
  width: 100%;
}

.content .wrapper .form-wrapper .login-form {
  opacity: 1;
  transform: translateY(0);
  z-index: 1;
}

.content .wrapper .form-wrapper .signup-form {
  opacity: 0;
  transform: translateY(30px);
  z-index: 0;
}

/* 当注册表单显示时的样式 */
.content .wrapper .form-wrapper .signup-form:not([style*="display: none"]) {
  z-index: 1;
}

/* 当登录表单隐藏时的样式 */
.content .wrapper .form-wrapper .login-form[style*="display: none"] {
  z-index: 0;
}

.content .wrapper .form-wrapper .login-form .tips,
.content .wrapper .form-wrapper .signup-form .tips {
  color: #fff;
}

.content .wrapper .form-wrapper .login-form .tips h1,
.content .wrapper .form-wrapper .signup-form .tips h1 {
  font-size: 46px;
  margin: 20px 0;
  font-family: "Poppins", sans-serif;
  font-weight: 900;
  letter-spacing: 0px;
}

.content .wrapper .form-wrapper .login-form .tips span,
.content .wrapper .form-wrapper .signup-form .tips span {
  margin: 0 0 25px 0;
  font-family: "Century Gothic", Times, serif;
}

.content .wrapper .form-wrapper .login-form .tips span:first-child,
.content .wrapper .form-wrapper .signup-form .tips span:first-child {
  color: #d1d1d1;
}

.content .wrapper .form-wrapper .login-form .tips span:last-child,
.content .wrapper .form-wrapper .signup-form .tips span:last-child {
  color: rgb(29, 144, 245);
  cursor: pointer;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .input-wrapper,
.content .wrapper .form-wrapper .signup-form .form-wrapper .input-wrapper {
  position: relative;
  margin: 30px 0;
  transition: 0.5s;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .input-wrapper .inputs,
.content .wrapper .form-wrapper .signup-form .form-wrapper .input-wrapper .inputs {
  width: 85%;
  height: 70px;
  display: block;
  border-radius: 18px;
  border: 0;
  background-color: rgb(50, 54, 69);
  color: #fff;
  padding: 20px 60px 0px 30px;
  box-sizing: border-box;
  outline: none;
  font-size: 15px;
  font-weight: 600;
  font-family: "Century Gothic", Times, serif;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .input-wrapper .inputs:focus,
.content .wrapper .form-wrapper .signup-form .form-wrapper .input-wrapper .inputs:focus {
  border: 1px solid rgb(21, 139, 243);
  box-shadow: 0 0 1px 1px rgb(21, 139, 243);
}

.content .wrapper .form-wrapper .login-form .form-wrapper .input-wrapper::before,
.content .wrapper .form-wrapper .signup-form .form-wrapper .input-wrapper::before {
  display: inline-block;
  width: 50px;
  height: 10px;
  color: rgb(113, 114, 119);
  position: absolute;
  top: 10px;
  left: 30px;
  white-space: nowrap;
  font-family: "Century Gothic", Times, serif;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .input-wrapper::after,
.content .wrapper .form-wrapper .signup-form .form-wrapper .input-wrapper::after {
  content: "";
  display: inline-block;
  width: 40px;
  height: 40px;
  position: absolute;
  top: 36px;
  right: 90px;
  background-size: 50%;
  background-repeat: no-repeat;
  z-index: 1;
  white-space: nowrap;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .user::before,
.content .wrapper .form-wrapper .signup-form .form-wrapper .user::before {
  content: "Email";
}

.content .wrapper .form-wrapper .login-form .form-wrapper .user::after,
.content .wrapper .form-wrapper .signup-form .form-wrapper .user::after {
  background-image: url(@/assets/email.png);
}

.content .wrapper .form-wrapper .login-form .form-wrapper .pwd input,
.content .wrapper .form-wrapper .signup-form .form-wrapper .pwd input {
  letter-spacing: 2px;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .pwd::before,
.content .wrapper .form-wrapper .signup-form .form-wrapper .pwd::before {
  content: "Password";
}

.content .wrapper .form-wrapper .login-form .form-wrapper .pwd::after,
.content .wrapper .form-wrapper .signup-form .form-wrapper .pwd::after {
  background-image: url(@/assets//password.png);
}

.content .wrapper .form-wrapper .login-form .form-wrapper .veri-code,
.content .wrapper .form-wrapper .signup-form .form-wrapper .veri-code {
  opacity: 0;
  z-index: -1;
  position: relative;
  transition: 0.5s;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .veri-code .veri-code-input,
.content .wrapper .form-wrapper .signup-form .form-wrapper .veri-code .veri-code-input {
  padding-right: 200px;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .veri-code .veri-code-tips,
.content .wrapper .form-wrapper .signup-form .form-wrapper .veri-code .veri-code-tips {
  position: absolute; 
  right: 110px;
  top: 36px;
  color: rgb(39, 150, 247);
  cursor: pointer;
  transition: color 0.3s ease;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .veri-code::before,
.content .wrapper .form-wrapper .signup-form .form-wrapper .veri-code::before {
  content: "Verification Code";
}

.content .wrapper .form-wrapper .login-form .form-wrapper .nickname::before,
.content .wrapper .form-wrapper .signup-form .form-wrapper .nickname::before {
  content: "nickname";
}

.content .wrapper .form-wrapper .login-form .form-btn,
.content .wrapper .form-wrapper .signup-form .form-btn {
  width: 85%;
  height: 60px;
  background-color: rgb(0, 129, 241);
  color: #fff;
  border-radius: 50px;
  border: 0;
  font-size: 20px;
  font-weight: 600;
  margin: 15px auto;
  cursor: pointer;
  font-family: "Century Gothic", Times, serif;
}

.content .wrapper .form-wrapper .login-form .btn-wrapper {
  display: flex;
  width: 85%;
  transform: none;
}

.content .wrapper .form-wrapper .login-form .btn-wrapper .login-btn {
  flex: 1;
  transition: 0.5s;
  margin-top: 20px;
}

.content .wrapper .form-wrapper .login-form .btn-wrapper .login-btn:hover {
  background-color: rgb(39, 150, 247);
}

.content .wrapper .form-wrapper .login-form .btn-wrapper .other-login-btn {
  flex: 1;
  margin-right: 10px;
  transition: 0.5s;
  background-color: rgb(85, 91, 105);
}

.content .wrapper .form-wrapper .login-form .btn-wrapper .other-login-btn:hover {
  background-color: rgb(101, 109, 126);
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login {
  transform: translate(0, -60%);
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .divider {
  width: 85%;
  margin: 20px 0;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .divider .line {
  display: inline-block;
  max-width: 45%;
  width: 45%;
  flex: 1;
  height: 1px;
  background-color: #fff;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .divider .divider-text {
  vertical-align: middle;
  margin: 0px 20px;
  line-height: 0;
  display: inline-block;
  width: 40px;
  color: #fff;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .other-login-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .other-login-wrapper .other-login-item {
  border: 1px solid #fff;
  padding: 10px;
  text-align: center;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  color: rgb(51, 49, 116);
  margin: 0 10px;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .other-login-wrapper .other-login-item img {
  width: 30px;
  height: 30px;
  vertical-align: middle;
}

.content .wrapper .form-wrapper .login-form .form-wrapper .other-login .other-login-wrapper .other-login-item span {
  vertical-align: middle;
}

.content .wrapper .form-wrapper .signup-form .form-wrapper {
  margin-top: 30px;
}

.content .wrapper .form-wrapper .signup-form .form-btn {
  margin-top: 30px;
  transition: 0.3s;
}

.content .wrapper .form-wrapper .signup-form .form-btn:hover {
  background-color: rgb(39, 150, 247);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* 确保密码输入框正常显示 */
.content .wrapper .form-wrapper .login-form .form-wrapper .pwd,
.content .wrapper .form-wrapper .signup-form .form-wrapper .pwd {
  position: relative;
  opacity: 1;
  z-index: 1;
}

/* 适应不同屏幕尺寸 */
@media screen and (min-width: 1440px) {
  .content .wrapper {
    width: 60%;
    max-width: 1200px;
  }
  
  .content .wrapper .form-wrapper .login-form,
  .content .wrapper .form-wrapper .signup-form {
    max-width: 600px;
  }
}

@media screen and (max-width: 768px) {
  .content .wrapper {
    width: 90%;
    padding: 40px 20px;
  }
  
  .content .wrapper .form-wrapper .login-form .tips h1,
  .content .wrapper .form-wrapper .signup-form .tips h1 {
    font-size: 32px;
  }
}
</style>