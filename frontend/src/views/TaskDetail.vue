<template>
  <el-card v-loading="loading">
    <template #header>
      <div class="card-header">
        <el-button @click="goBack">
          <el-icon><Arrow-Left /></el-icon>
          返回
        </el-button>
        <h3>任务详情</h3>
        <el-button type="primary" @click="handleEdit">编辑</el-button>
      </div>
    </template>
    
    <el-descriptions :column="1" border v-if="task">
      <el-descriptions-item label="标题">{{ task.title }}</el-descriptions-item>
      <el-descriptions-item label="描述">{{ task.description || '无' }}</el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="task.completed ? 'success' : 'info'">
          {{ task.completed ? '已完成' : '未完成' }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="优先级">
        <el-tag v-if="task.priority === 'high'" type="danger">高</el-tag>
        <el-tag v-if="task.priority === 'medium'" type="warning">中</el-tag>
        <el-tag v-if="task.priority === 'low'" type="success">低</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="截止日期">{{ task.due_date || '无' }}</el-descriptions-item>
      <el-descriptions-item label="提醒时间">{{ task.reminder_time || '无' }}</el-descriptions-item>
      <el-descriptions-item label="创建时间">{{ formatDate(task.created_at) }}</el-descriptions-item>
      <el-descriptions-item label="更新时间">{{ formatDate(task.updated_at) }}</el-descriptions-item>
    </el-descriptions>
    
    <el-empty v-else description="任务不存在" />
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import type { Task } from '@/types'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const task = ref<Task | null>(null)
const loading = ref(false)

const goBack = () => {
  router.back()
}

const handleEdit = () => {
  // TODO: 打开编辑对话框
  console.log('Edit task:', task.value?.id)
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) return
  
  loading.value = true
  try {
    task.value = await taskStore.fetchTasks() // TODO: 改用 getTask
  } catch (error) {
    console.error('Failed to fetch task:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h3 {
    margin: 0;
  }
}
</style>
