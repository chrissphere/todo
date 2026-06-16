import request from './request'
import type { Tag } from '@/types'

// 获取所有标签
export function getTags() {
  return request<any, Tag[]>({
    url: '/tags',
    method: 'get'
  })
}

// 创建标签
export function createTag(data: { name: string; color?: string }) {
  return request<any, Tag>({
    url: '/tags',
    method: 'post',
    data
  })
}

// 更新标签
export function updateTag(id: number, data: Partial<Tag>) {
  return request<any, Tag>({
    url: `/tags/${id}`,
    method: 'put',
    data
  })
}

// 删除标签
export function deleteTag(id: number) {
  return request<any, void>({
    url: `/tags/${id}`,
    method: 'delete'
  })
}
