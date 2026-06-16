<template>
  <el-container class="layout-container">
    <el-aside width="240px">
      <div class="logo">
        <el-icon size="24"><Check-List /></el-icon>
        <span>待办事项</span>
      </div>
      
      <el-menu :default-active="activeMenu" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
        <el-menu-item index="/tasks">
          <el-icon><List /></el-icon>
          <span>任务列表</span>
        </el-menu-item>
        
        <el-menu-item index="/lists">
          <el-icon><Folder /></el-icon>
          <span>清单管理</span>
        </el-menu-item>
        
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-content">
          <breadcrumb />
          <div class="user-info">
            <el-dropdown>
              <span class="user-name">
                <el-avatar :size="32" icon="User" />
                <span>用户</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">
                    <el-icon><Switch-Button /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  localStorage.removeItem('token')
  ElMessage.success('已退出登录')
  router.push({ name: 'Login' })
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  
  .el-aside {
    background-color: #304156;
    color: #fff;
    
    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 18px;
      font-weight: 600;
      color: #fff;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .el-menu {
      border-right: none;
    }
  }
  
  .el-header {
    background-color: #fff;
    border-bottom: 1px solid #e6e6e6;
    padding: 0 20px;
    
    .header-content {
      height: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .user-info {
      .user-name {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        
        span {
          margin-left: 8px;
        }
      }
    }
  }
  
  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
  }
}
</style>
