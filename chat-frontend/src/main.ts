import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import axios from 'axios'

// 配置axios默认值
axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.withCredentials = true

const app = createApp(App)
app.use(router)
app.mount('#app')
