<template>
  <div class="tasks-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>任务列表</h3>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            新建任务
          </el-button>
        </div>
      </template>
      
      <!-- 过滤器 -->
      <div class="filters">
        <el-radio-group v-model="filterCompleted" @change="handleFilterChange">
          <el-radio-button :label="false">未完成</el-radio-button>
          <el-radio-button :label="true">已完成</el-radio-button>
          <el-radio-button :label="null">全部</el-radio-button>
        </el-radio-group>
      </div>
      
      <!-- 任务列表 -->
      <el-table :data="filteredTasks" v-loading="loading" style="width: 100%" :show-header="false">
        <el-table-column width="50">
          <template #default="{ row }">
            <el-checkbox :model-value="row.completed" @change="handleToggleComplete(row, $event)" />
          </template>
        </el-table-column>
        
        <el-table-column>
          <template #default="{ row }">
            <div class="task-item" :class="{ completed: row.completed }" @click="handleViewDetail(row.id)">
              <span class="task-title">{{ row.title }}</span>
              <el-tag v-if="row.priority === 'high'" type="danger" size="small">高</el-tag>
              <el-tag v-if="row.priority === 'medium'" type="warning" size="small">中</el-tag>
              <el-tag v-if="row.priority === 'low'" type="success" size="small">低</el-tag>
              <span class="task-date" v-if="row.due_date">{{ formatDate(row.due_date) }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column width="100" align="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑任务对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑任务' : '新建任务'" width="500px">
      <el-form :model="taskForm" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="taskForm.title" placeholder="任务标题" />
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input v-model="taskForm.description" type="textarea" :rows="3" placeholder="任务描述" />
        </el-form-item>
        
        <el-form-item label="优先级">
          <el-select v-model="taskForm.priority" placeholder="选择优先级">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="截止日期">
          <el-date-picker v-model="taskForm.due_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" />
        </el-form-item>
        
        <el-form-item label="提醒时间">
          <el-time-picker v-model="taskForm.reminder_time" placeholder="选择时间" value-format="HH:mm" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTaskStore } from '@/stores/task'
import { storeToRefs } from 'pinia'
import type { Task } from '@/types'

const router = useRouter()
const taskStore = useTaskStore()
const { filteredTasks, loading } = storeToRefs(taskStore)

const filterCompleted = ref<boolean | null>(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)

const taskForm = reactive<Partial<Task>>({
  title: '',
  description: '',
  priority: 'medium',
  due_date: null,
  reminder_time: null
})

const handleFilterChange = (value: boolean | null) => {
  taskStore.setFilterCompleted(value !== false)
  taskStore.fetchTasks()
}

const handleToggleComplete = async (task: Task, checked: boolean) => {
  try {
    await taskStore.toggleComplete(task.id, checked)
    ElMessage.success(checked ? '任务已完成' : '任务已取消完成')
  } catch (error) {
    console.error('Failed to toggle task:', error)
  }
}

const handleViewDetail = (id: number) => {
  router.push(`/task/${id}`)
}

const handleEdit = (task: Task) => {
  isEdit.value = true
  taskForm.title = task.title
  taskForm.description = task.description || ''
  taskForm.priority = task.priority
  taskForm.due_date = task.due_date
  taskForm.reminder_time = task.reminder_time
  // @ts-ignore
  taskForm.id = task.id
  dialogVisible.value = true
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await taskStore.removeTask(id)
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('Failed to delete task:', error)
    }
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.assign(taskForm, {
    title: '',
    description: '',
    priority: 'medium',
    due_date: null,
    reminder_time: null
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!taskForm.title) {
    ElMessage.warning('请输入任务标题')
    return
  }
  
  submitLoading.value = true
  try {
    if (isEdit.value) {
      // @ts-ignore
      await taskStore.updateTaskFn(taskForm.id, taskForm)
      ElMessage.success('更新成功')
    } else {
      await taskStore.addTask(taskForm)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    taskStore.fetchTasks()
  } catch (error) {
    console.error('Failed to submit task:', error)
  } finally {
    submitLoading.value = false
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  taskStore.fetchTasks()
})
</script>

<style scoped lang="scss">
.tasks-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h3 {
      margin: 0;
    }
  }
  
  .filters {
    margin-bottom: 16px;
  }
  
  .task-item {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    
    &.completed {
      .task-title {
        text-decoration: line-through;
        color: #999;
      }
    }
    
    .task-title {
      flex: 1;
    }
    
    .task-date {
      font-size: 12px;
      color: #999;
    }
  }
}
</style>
