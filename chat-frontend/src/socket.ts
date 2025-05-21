import { io, Socket } from 'socket.io-client';

const URL = 'http://localhost:5000';

const socket: Socket = io(URL, {
  autoConnect: true,
  transports: ['websocket'], // 强制使用 WebSocket，避免轮询问题
  withCredentials: true      // 可选：允许跨域 Cookie（如果你后端做了身份认证）
});

// 添加连接事件监听
socket.on('connect', () => {
  console.log('WebSocket连接成功');
});

socket.on('connect_error', (error) => {
  console.error('WebSocket连接错误:', error);
});

socket.on('disconnect', (reason) => {
  console.log('WebSocket断开连接:', reason);
});

export default socket;
