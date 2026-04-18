export interface User {
  id: number;
  username: string;
  full_name: string;
  role: 'villager' | 'staff' | 'admin';
  village_id: number;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'assigned' | 'in_progress' | 'completed';
  creator_id: number;
  assignee_id?: number;
  created_at: string;
  result_note?: string;
}

export interface Policy {
  id: number;
  title: string;
  content: string;
  category?: string;
  published_at?: string;
  created_at: string;
}

export interface Note {
  id: number;
  type: string;
  title: string;
  content?: string;
  user_id: number;
  created_at: string;
  updated_at?: string;
}
