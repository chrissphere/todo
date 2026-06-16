import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TaskList } from '@/types'
import * as listApi from '@/api/list'

export const useListStore = defineStore('list', () => {
  const lists = ref<TaskList[]>([])
  const loading = ref(false)

  async function fetchLists() {
    loading.value = true
    try {
      lists.value = await listApi.getLists()
    } catch (error) {
      console.error('Failed to fetch lists:', error)
    } finally {
      loading.value = false
    }
  }

  async function addList(data: { name: string; color?: string; icon?: string }) {
    try {
      const newList = await listApi.createList(data)
      lists.value.push(newList)
      return newList
    } catch (error) {
      console.error('Failed to create list:', error)
      throw error
    }
  }

  async function updateListFn(id: number, updates: Partial<TaskList>) {
    try {
      const updatedList = await listApi.updateList(id, updates)
      const index = lists.value.findIndex(l => l.id === id)
      if (index !== -1) {
        lists.value[index] = updatedList
      }
      return updatedList
    } catch (error) {
      console.error('Failed to update list:', error)
      throw error
    }
  }

  async function removeList(id: number) {
    try {
      await listApi.deleteList(id)
      lists.value = lists.value.filter(l => l.id !== id)
    } catch (error) {
      console.error('Failed to delete list:', error)
      throw error
    }
  }

  return {
    lists,
    loading,
    fetchLists,
    addList,
    updateListFn,
    removeList
  }
})
