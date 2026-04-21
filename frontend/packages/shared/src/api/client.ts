import axios from 'axios';

// 临时硬编码后端地址
const baseURL = 'https://my-dev--main-ebtk.diploi.me/api/v1';

const apiClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

// 以下代码保持不变
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