import axios from 'axios';

// 使用相对路径，让 Vite 代理转发到本地后端
// 开发环境下，Vite 会将 /api 代理到 http://localhost:8000
const baseURL = '/api/v1';

const apiClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  const villageId = localStorage.getItem('village_id');
  if (villageId) {
    config.headers['X-Tenant-ID'] = villageId;
  } else {
    config.headers['X-Tenant-ID'] = '1';
  }
  
  if (config.url?.includes('/auth/login')) {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  return config;
});

export default apiClient;