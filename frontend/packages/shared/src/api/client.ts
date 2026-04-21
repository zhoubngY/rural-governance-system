import axios from 'axios';

// 从环境变量获取后端 API 基址，如果未设置则使用相对路径（开发环境）
const baseURL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config) => {
  // 添加 token
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // 添加租户ID（必须）
  const villageId = localStorage.getItem('village_id');
  if (villageId) {
    config.headers['X-Tenant-ID'] = villageId;
  } else {
    config.headers['X-Tenant-ID'] = '1';
  }
  
  // 登录接口特殊处理（如有需要）
  if (config.url?.includes('/auth/login')) {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  return config;
});

export default apiClient;