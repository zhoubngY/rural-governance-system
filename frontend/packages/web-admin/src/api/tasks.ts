import request from './client';   // 注意导入默认导出的 request

export interface Assignment {
  id: number;
  task_id: number;
  user_id: number;
  user_name?: string;
  status: 'pending' | 'assigned' | 'in_progress' | 'completed' | 'cancelled';
  feedback?: string;
  assigned_at: string;
  started_at?: string;
  completed_at?: string;
  updated_at?: string;
}

export interface Attachment {
  id: number;
  task_id: number;
  filename: string;
  file_path: string;
  file_size?: number;
  mime_type?: string;
  uploaded_by?: number;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  priority: 'medium' | 'urgent';
  status: 'pending' | 'assigned' | 'in_progress' | 'completed' | 'cancelled';
  creator_id: number;
  creator_name?: string;
  assignee_id?: number;
  assignee_name?: string;
  assignee_ids?: number[];      // 新增：多负责人ID数组
  assignee_names?: string[];    // 新增：多负责人姓名数组
  due_date?: string;
  extra_data?: Record<string, any>;
  created_at: string;
  assignments?: Assignment[];
  attachments?: Attachment[];
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: string;
  due_date?: string | null;
  extra_data?: Record<string, any>;
  assignee_ids?: number[];
}

export const getTasks = async (params?: { skip?: number; limit?: number; status?: string; priority?: string; title_contains?: string }) => {
  return request.get<Task[]>('/tasks/', { params });
};

export const getTaskDetail = async (id: number) => {
  return request.get<Task>(`/tasks/${id}`);
};

export const createTask = async (data: TaskCreate) => {
  return request.post<Task>('/tasks/', data);
};

export const updateTask = async (id: number, data: Partial<Task>) => {
  return request.put<Task>(`/tasks/${id}`, data);
};

export const assignTask = (taskId: number, assigneeId: number) => {
  return request.post<Task>(`/tasks/${taskId}/assign`, { assignee_id: assigneeId });
};

export const updateAssignment = (assignmentId: number, data: { status?: string; feedback?: string }) => {
  return request.patch<Assignment>(`/tasks/assignments/${assignmentId}`, data);
};

export const startTask = (taskId: number) => {
  return request.post<Task>(`/tasks/${taskId}/start`);
};

export const completeTask = (taskId: number, result_note?: string) => {
  return request.post<Task>(`/tasks/${taskId}/complete`, null, { params: { result_note } });
};

export const deleteTask = (id: number) => {
  return request.delete(`/tasks/${id}`);
};

export const uploadAttachment = (taskId: number, file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return request.post<Attachment>(`/tasks/${taskId}/attachments`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteAttachment = (attachmentId: number) => {
  return request.delete(`/tasks/attachments/${attachmentId}`);
};

export const getAttachmentDownloadUrl = (attachmentId: number) => {
  return `/api/v1/tasks/attachments/${attachmentId}/download`;
};