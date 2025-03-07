<template>
  <div class="home-container">
    <div class="welcome-section">
      <h1 class="welcome-title">
        <el-icon><ChatLineRound /></el-icon>
        欢迎使用知答
      </h1>
      <p class="welcome-subtitle">让AI为您提供7x24小时的智能服务</p>
    </div>

    <el-row :gutter="24" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <el-icon><ChatDotRound /></el-icon>
              今日对话数
            </div>
          </template>
          <div class="stats-value">
            <span class="number">{{ stats.todayChats }}</span>
            <span class="trend" :class="{ up: stats.chatsTrend > 0 }">
              {{ Math.abs(stats.chatsTrend) }}%
              <el-icon>
                <CaretTop v-if="stats.chatsTrend > 0" />
                <CaretBottom v-else />
              </el-icon>
            </span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <el-icon><MessageBox /></el-icon>
              今日消息数
            </div>
          </template>
          <div class="stats-value">
            <span class="number">{{ stats.todayMessages }}</span>
            <span class="trend" :class="{ up: stats.messagesTrend > 0 }">
              {{ Math.abs(stats.messagesTrend) }}%
              <el-icon>
                <CaretTop v-if="stats.messagesTrend > 0" />
                <CaretBottom v-else />
              </el-icon>
            </span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <el-icon><Timer /></el-icon>
              平均响应时间
            </div>
          </template>
          <div class="stats-value">
            <span class="number">{{ stats.avgResponseTime }}s</span>
            <span class="trend" :class="{ up: stats.responseTimeTrend < 0 }">
              {{ Math.abs(stats.responseTimeTrend) }}%
              <el-icon>
                <CaretTop v-if="stats.responseTimeTrend < 0" />
                <CaretBottom v-else />
              </el-icon>
            </span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <el-icon><Star /></el-icon>
              满意度
            </div>
          </template>
          <div class="stats-value">
            <span class="number">{{ stats.satisfaction }}%</span>
            <span class="trend" :class="{ up: stats.satisfactionTrend > 0 }">
              {{ Math.abs(stats.satisfactionTrend) }}%
              <el-icon>
                <CaretTop v-if="stats.satisfactionTrend > 0" />
                <CaretBottom v-else />
              </el-icon>
            </span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" class="features-row">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card" @click="startChat">
          <el-icon class="feature-icon"><ChatRound /></el-icon>
          <h3>开始对话</h3>
          <p>与AI助手进行实时对话，获取智能解答</p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card" @click="viewHistory">
          <el-icon class="feature-icon"><Document /></el-icon>
          <h3>历史记录</h3>
          <p>查看历史对话记录和数据统计</p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card class="feature-card" @click="openSettings">
          <el-icon class="feature-icon"><Setting /></el-icon>
          <h3>系统设置</h3>
          <p>自定义系统参数和偏好设置</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import {
  ChatLineRound,
  ChatDotRound,
  MessageBox,
  Timer,
  Star,
  CaretTop,
  CaretBottom,
  ChatRound,
  Document,
  Setting
} from '@element-plus/icons-vue'

const router = useRouter()

const stats = reactive({
  todayChats: 128,
  chatsTrend: 15,
  todayMessages: 1024,
  messagesTrend: 8,
  avgResponseTime: 1.5,
  responseTimeTrend: -12,
  satisfaction: 98,
  satisfactionTrend: 2
})

const startChat = () => {
  router.push('/chat')
}

const viewHistory = () => {
  router.push('/chat')
}

const openSettings = () => {
  // 待实现
}
</script>

<style scoped>
.home-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 48px;
}

.welcome-title {
  font-size: 36px;
  color: var(--el-text-color-primary);
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.welcome-title .el-icon {
  font-size: 40px;
  color: var(--el-color-primary);
}

.welcome-subtitle {
  margin: 16px 0 0;
  font-size: 16px;
  color: var(--el-text-color-secondary);
}

.stats-row {
  margin-bottom: 24px;
}

.stats-card {
  height: 100%;
  transition: transform 0.3s;
}

.stats-card:hover {
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.stats-value {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.number {
  font-size: 32px;
  font-weight: bold;
  color: var(--el-text-color-primary);
}

.trend {
  font-size: 14px;
  color: var(--el-color-danger);
  display: flex;
  align-items: center;
  gap: 4px;
}

.trend.up {
  color: var(--el-color-success);
}

.features-row {
  margin-top: 48px;
}

.feature-card {
  height: 100%;
  text-align: center;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  font-size: 48px;
  color: var(--el-color-primary);
  margin-bottom: 16px;
}

.feature-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: var(--el-text-color-primary);
}

.feature-card p {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

@media (max-width: 768px) {
  .home-container {
    padding: 16px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .welcome-title .el-icon {
    font-size: 32px;
  }
  
  .welcome-subtitle {
    font-size: 14px;
  }
  
  .stats-row {
    margin-bottom: 16px;
  }
  
  .stats-card {
    margin-bottom: 16px;
  }
  
  .features-row {
    margin-top: 32px;
  }
  
  .feature-card {
    margin-bottom: 16px;
  }
}
</style>