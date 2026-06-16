<template>
  <el-card>
    <template #header>
      <h3>设置</h3>
    </template>
    
    <el-form label-width="120px">
      <el-form-item label="主题">
        <el-radio-group v-model="theme">
          <el-radio-button label="light">浅色</el-radio-button>
          <el-radio-button label="dark">深色</el-radio-button>
          <el-radio-button label="auto">跟随系统</el-radio-button>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="语言">
        <el-select v-model="language" placeholder="选择语言">
          <el-option label="简体中文" value="zh-CN" />
          <el-option label="English" value="en" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="提醒音效">
        <el-switch v-model="soundEnabled" />
      </el-form-item>
      
      <el-form-item label="桌面通知">
        <el-switch v-model="notificationEnabled" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSave">保存设置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const theme = ref('light')
const language = ref('zh-CN')
const soundEnabled = ref(true)
const notificationEnabled = ref(true)

const handleSave = () => {
  localStorage.setItem('theme', theme.value)
  localStorage.setItem('language', language.value)
  localStorage.setItem('soundEnabled', String(soundEnabled.value))
  localStorage.setItem('notificationEnabled', String(notificationEnabled.value))
  
  ElMessage.success('设置已保存')
}

onMounted(() => {
  theme.value = localStorage.getItem('theme') || 'light'
  language.value = localStorage.getItem('language') || 'zh-CN'
  soundEnabled.value = localStorage.getItem('soundEnabled') !== 'false'
  notificationEnabled.value = localStorage.getItem('notificationEnabled') !== 'false'
})
</script>
