import request from './request'
import type { TaskList } from '@/types'

// 获取所有清单
export function getLists() {
  return request<any, TaskList[]>({
    url: '/lists',
    method: 'get'
  })
}

// 获取清单详情
export function getList(id: number) {
  return request<any, TaskList>({
    url: `/lists/${id}`,
    method: 'get'
  })
}

// 创建清单
export function createList(data: { name: string; color?: string; icon?: string }) {
  return request<any, TaskList>({
    url: '/lists',
    method: 'post',
    data
  })
}

// 更新清单
export function updateList(id: number, data: Partial<TaskList>) {
  return request<any, TaskList>({
    url: `/lists/${id}`,
    method: 'put',
    data
  })
}

// 删除清单
export function deleteList(id: number) {
  return request<any, void>({
    url: `/lists/${id}`,
    method: 'delete'
  })
}
