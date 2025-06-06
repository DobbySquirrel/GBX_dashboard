import { io } from 'socket.io-client';

// 创建Socket.IO连接
const socket = io('http://110.41.178.82:3000', {
  autoConnect: false,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  timeout: 10000
});

// 连接事件处理
socket.on('connect', () => {
  console.log('已连接到Socket.IO服务器');
});

socket.on('disconnect', () => {
  console.log('与Socket.IO服务器断开连接');
});

socket.on('connect_error', (error) => {
  console.error('Socket.IO连接错误:', error);
});

export default socket; 