import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
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
    // 如果尚未存储（比如登录页面），可设置默认租户ID（例如1）
    config.headers['X-Tenant-ID'] = '1';
  }
  
  // 登录接口特殊处理（如有需要）
  if (config.url?.includes('/auth/login')) {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  return config;
});

export default apiClient;