import request from './request'
import type { Task, PaginatedResponse, PaginationParams } from '@/types'

// 获取任务列表
export function getTasks(params: PaginationParams & { list_id?: number; completed?: boolean }) {
  return request<any, PaginatedResponse<Task>>({
    url: '/tasks',
    method: 'get',
    params
  })
}

// 获取任务详情
export function getTask(id: number) {
  return request<any, Task>({
    url: `/tasks/${id}`,
    method: 'get'
  })
}

// 创建任务
export function createTask(data: Partial<Task>) {
  return request<any, Task>({
    url: '/tasks',
    method: 'post',
    data
  })
}

// 更新任务
export function updateTask(id: number, data: Partial<Task>) {
  return request<any, Task>({
    url: `/tasks/${id}`,
    method: 'put',
    data
  })
}

// 删除任务
export function deleteTask(id: number) {
  return request<any, void>({
    url: `/tasks/${id}`,
    method: 'delete'
  })
}

// 完成任务
export function completeTask(id: number) {
  return request<any, Task>({
    url: `/tasks/${id}/complete`,
    method: 'post'
  })
}

// 取消完成
export function uncompleteTask(id: number) {
  return request<any, Task>({
    url: `/tasks/${id}/uncomplete`,
    method: 'post'
  })
}
