import apiClient from '@shared/api/client';

export interface Task {
  id: number;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'pending' | 'assigned' | 'in_progress' | 'completed' | 'cancelled';
  creator_id: number;
  assignee_id?: number;
  assignee_name?: string;
  creator_name?: string;
  due_date?: string;
  extra_data?: Record<string, any>;
  created_at: string;
}

export const getTasks = async (params?: { skip?: number; limit?: number }) => {
  return apiClient.get<Task[]>('/tasks/', { params });
};

export const createTask = async (data: Partial<Task>) => {
  return apiClient.post<Task>('/tasks/', data);
};

export const updateTask = async (id: number, data: Partial<Task>) => {
  return apiClient.put<Task>(`/tasks/${id}`, data);
};

export const assignTask = (taskId: number, assigneeId: number) => {
  return apiClient.post<Task>(`/tasks/${taskId}/assign`, { assignee_id: assigneeId });
};

export const startTask = (taskId: number) => {
  return apiClient.post<Task>(`/tasks/${taskId}/start`);
};

export const completeTask = (taskId: number, result_note?: string) => {
  return apiClient.post<Task>(`/tasks/${taskId}/complete`, null, { params: { result_note } });
};

export const deleteTask = (id: number) => {
  return apiClient.delete(`/tasks/${id}`);
};