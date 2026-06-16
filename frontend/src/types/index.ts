// 任务接口
export interface Task {
  id: number
  title: string
  description: string
  completed: boolean
  priority: 'low' | 'medium' | 'high'
  due_date: string | null
  reminder_time: string | null
  list_id: number | null
  parent_id: number | null
  order: number
  created_at: string
  updated_at: string
  sync_status: 'local' | 'synced' | 'pending'
  last_synced_at: string | null
}

// 清单接口
export interface TaskList {
  id: number
  name: string
  color: string
  icon: string
  user_id: number
  created_at: string
  updated_at: string
}

// 标签接口
export interface Tag {
  id: number
  name: string
  color: string
  user_id: number
  created_at: string
}

// 用户接口
export interface User {
  id: number
  username: string
  email: string
  created_at: string
}

// API 响应类型
export interface ApiResponse<T> {
  data: T
  message: string
  status: number
}

// 分页参数
export interface PaginationParams {
  page: number
  size: number
  sort?: string
  order?: 'asc' | 'desc'
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
}
