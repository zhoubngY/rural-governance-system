import request from './client'

// 大事记
export const memorialApi = {
  list: () => request.get('/memorials'),
  create: (data: any) => request.post('/memorials', data),
  update: (id: number, data: any) => request.put(`/memorials/${id}`, data),
  delete: (id: number) => request.delete(`/memorials/${id}`)
}

// 通知
export const noticeApi = {
  list: () => request.get('/notices'),
  create: (data: any) => request.post('/notices', data),
  update: (id: number, data: any) => request.put(`/notices/${id}`, data),
  delete: (id: number) => request.delete(`/notices/${id}`)
}

// 办事指南
export const guideApi = {
  list: () => request.get('/guides'),
  create: (data: any) => request.post('/guides', data),
  update: (id: number, data: any) => request.put(`/guides/${id}`, data),
  delete: (id: number) => request.delete(`/guides/${id}`)
}

// 村民申请（管理员）
export const applicationApi = {
  list: () => request.get('/applications/admin'),
  review: (id: number, data: { status: string; admin_reply?: string }) => 
    request.put(`/applications/${id}/review`, data)
}

// 在线咨询（管理员）
export const consultationApi = {
  list: () => request.get('/consultations/admin'),
  answer: (id: number, data: { answer: string }) => 
    request.put(`/consultations/${id}/answer`, data)
}