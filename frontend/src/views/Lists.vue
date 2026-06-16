<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>清单管理</h3>
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新建清单
        </el-button>
      </div>
    </template>
    
    <el-table :data="lists" v-loading="loading" style="width: 100%">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="color" label="颜色" width="100">
        <template #default="{ row }">
          <div class="color-preview" :style="{ backgroundColor: row.color }"></div>
        </template>
      </el-table-column>
      <el-table-column prop="icon" label="图标" width="100" />
      <el-table-column label="操作" width="200" align="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑清单' : '新建清单'" width="500px">
      <el-form :model="listForm" label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="listForm.name" placeholder="清单名称" />
        </el-form-item>
        
        <el-form-item label="颜色">
          <el-color-picker v-model="listForm.color" />
        </el-form-item>
        
        <el-form-item label="图标">
          <el-input v-model="listForm.icon" placeholder="图标名称" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useListStore } from '@/stores/list'
import { storeToRefs } from 'pinia'
import type { TaskList } from '@/types'

const listStore = useListStore()
const { lists, loading } = storeToRefs(listStore)

const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)

const listForm = reactive<Partial<TaskList>>({
  name: '',
  color: '#409EFF',
  icon: 'Folder'
})

const handleEdit = (list: TaskList) => {
  isEdit.value = true
  listForm.name = list.name
  listForm.color = list.color
  listForm.icon = list.icon
  // @ts-ignore
  listForm.id = list.id
  dialogVisible.value = true
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个清单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await listStore.removeList(id)
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('Failed to delete list:', error)
    }
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.assign(listForm, {
    name: '',
    color: '#409EFF',
    icon: 'Folder'
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!listForm.name) {
    ElMessage.warning('请输入清单名称')
    return
  }
  
  submitLoading.value = true
  try {
    if (isEdit.value) {
      // @ts-ignore
      await listStore.updateListFn(listForm.id, listForm)
      ElMessage.success('更新成功')
    } else {
      await listStore.addList(listForm)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    listStore.fetchLists()
  } catch (error) {
    console.error('Failed to submit list:', error)
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  listStore.fetchLists()
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

.color-preview {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
</style>
