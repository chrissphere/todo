import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Task } from '@/types'
import * as taskApi from '@/api/task'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const currentListId = ref<number | null>(null)
  const filterCompleted = ref<boolean>(false)

  // 计算属性
  const filteredTasks = computed(() => {
    let result = tasks.value
    
    if (currentListId.value !== null) {
      result = result.filter(t => t.list_id === currentListId.value)
    }
    
    if (!filterCompleted.value) {
      result = result.filter(t => !t.completed)
    }
    
    return result.sort((a, b) => a.order - b.order)
  })

  const completedCount = computed(() => {
    return tasks.value.filter(t => t.completed).length
  })

  const pendingCount = computed(() => {
    return tasks.value.filter(t => !t.completed).length
  })

  // 方法
  async function fetchTasks() {
    loading.value = true
    try {
      const response = await taskApi.getTasks({
        page: 1,
        size: 100,
        list_id: currentListId.value || undefined,
        completed: filterCompleted.value
      })
      tasks.value = response.items
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      loading.value = false
    }
  }

  async function addTask(task: Partial<Task>) {
    try {
      const newTask = await taskApi.createTask(task)
      tasks.value.push(newTask)
      return newTask
    } catch (error) {
      console.error('Failed to create task:', error)
      throw error
    }
  }

  async function updateTaskFn(id: number, updates: Partial<Task>) {
    try {
      const updatedTask = await taskApi.updateTask(id, updates)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
      return updatedTask
    } catch (error) {
      console.error('Failed to update task:', error)
      throw error
    }
  }

  async function removeTask(id: number) {
    try {
      await taskApi.deleteTask(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
    } catch (error) {
      console.error('Failed to delete task:', error)
      throw error
    }
  }

  async function toggleComplete(id: number, completed: boolean) {
    try {
      const task = completed
        ? await taskApi.completeTask(id)
        : await taskApi.uncompleteTask(id)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = task
      }
      return task
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
      throw error
    }
  }

  function setCurrentList(listId: number | null) {
    currentListId.value = listId
  }

  function setFilterCompleted(completed: boolean) {
    filterCompleted.value = completed
  }

  return {
    tasks,
    loading,
    currentListId,
    filterCompleted,
    filteredTasks,
    completedCount,
    pendingCount,
    fetchTasks,
    addTask,
    updateTaskFn,
    removeTask,
    toggleComplete,
    setCurrentList,
    setFilterCompleted
  }
})
