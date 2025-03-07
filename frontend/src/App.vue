<template>
  <el-container class="layout-container" v-if="isAuthenticated">
    <el-header class="header">
      <div class="logo">
        <el-icon class="logo-icon"><ChatLineRound /></el-icon>
        知答
      </div>
      <el-menu
        mode="horizontal"
        :router="true"
        class="nav-menu"
        :ellipsis="false"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          首页
        </el-menu-item>
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          对话
        </el-menu-item>
      </el-menu>
      <div class="user-actions">
        <el-dropdown @command="handleCommand" trigger="click">
          <el-button type="primary" class="user-dropdown">
            <el-avatar :size="24" class="user-avatar">{{ username.charAt(0) }}</el-avatar>
            {{ username }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    <el-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
  </el-container>
  <router-view v-else />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ArrowDown,
  HomeFilled,
  ChatDotRound,
  ChatLineRound,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const username = ref(localStorage.getItem('username') || '用户')

const isAuthenticated = computed(() => {
  return localStorage.getItem('isAuthenticated') === 'true'
})

const handleCommand = (command: string) => {
  if (command === 'logout') {
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('username')
    router.push('/login')
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

#app {
  height: 100vh;
}

.layout-container {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 0 24px;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  height: 64px;
  position: relative;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--el-color-primary);
  margin-right: 2rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.02);
}

.logo-icon {
  font-size: 24px;
}

.nav-menu {
  flex: 1;
  border: none;
}

.nav-menu .el-menu-item {
  font-size: 1rem;
  height: 64px;
  line-height: 64px;
}

.nav-menu .el-icon {
  margin-right: 4px;
  font-size: 18px;
}

.user-actions {
  margin-left: auto;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 16px;
}

.user-avatar {
  background: var(--el-color-primary-light-3);
  color: white;
  text-transform: uppercase;
}

.el-main {
  background-color: var(--el-bg-color-page);
  padding: 24px;
}

/* 添加过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    padding: 0 16px;
  }
  
  .logo {
    font-size: 1.2rem;
    margin-right: 1rem;
  }

  .nav-menu .el-menu-item {
    padding: 0 12px;
  }
  
  .el-main {
    padding: 16px;
  }
}

@media (max-width: 576px) {
  .logo {
    font-size: 1rem;
  }
  
  .nav-menu .el-menu-item span {
    display: none;
  }
  
  .user-dropdown span:not(.user-avatar) {
    display: none;
  }
}
</style>