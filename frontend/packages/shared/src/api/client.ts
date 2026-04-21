import axios from 'axios';

// 强制使用环境变量，如果未定义则报错
const baseURL = import.meta.env.VITE_API_BASE_URL;
if (!baseURL) {
  console.error('VITE_API_BASE_URL is not defined!');
}

const apiClient = axios.create({
  baseURL: baseURL || '/api/v1',
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