<template>
  <div class="chat-container">
    <div class="chat-sidebar">
      <div class="chat-history">
        <h3 class="sidebar-title">
          <el-icon><Timer /></el-icon>
          会话历史
        </h3>
        <div class="history-list">
          <div
            v-for="(chat, index) in chatHistory"
            :key="index"
            class="history-item"
            :class="{ active: currentChat === index }"
            @click="switchChat(index)"
          >
            <el-icon><ChatDotSquare /></el-icon>
            <span class="chat-title">会话 {{ index + 1 }}</span>
            <el-icon class="delete-icon" @click.stop="deleteChat(index)"><Delete /></el-icon>
          </div>
        </div>
        <el-button type="primary" class="new-chat-btn" @click="newChat">
          <el-icon><Plus /></el-icon>
          新建会话
        </el-button>
      </div>
    </div>

    <div class="chat-main">
      <div class="message-container" ref="messageContainer">
        <template v-if="messages.length">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="message.role"
          >
            <el-avatar
              :size="36"
              :icon="message.role === 'user' ? User : Service"
              :class="message.role"
            />
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(message.content)" />
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
        </template>
        <div v-else class="empty-state">
          <el-icon class="empty-icon"><ChatLineRound /></el-icon>
          <p>开始新的对话吧！</p>
        </div>
      </div>

      <div class="input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="输入您的问题..."
          :disabled="loading"
          @keydown.enter.prevent="sendMessage"
        />
        <el-button
          type="primary"
          :loading="loading"
          class="send-button"
          @click="sendMessage"
        >
          <template #icon>
            <el-icon><Position /></el-icon>
          </template>
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { 
  Timer,
  ChatDotSquare,
  Delete,
  Plus,
  Position,
  User,
  Service,
  ChatLineRound
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { sendMessage as apiSendMessage, getChatHistory } from '../api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

const loading = ref(false)
const inputMessage = ref('')
const messages = ref<Message[]>([])
const messageContainer = ref<HTMLElement>()
const chatHistory = ref<Message[][]>([[]])
const currentChat = ref(0)

const formatMessage = (content: string) => {
  return DOMPurify.sanitize(marked(content))
}

const formatTime = (timestamp: number) => {
  return dayjs(timestamp).format('HH:mm')
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  const userMessage: Message = {
    role: 'user',
    content: inputMessage.value,
    timestamp: Date.now()
  }
  
  messages.value.push(userMessage)
  chatHistory.value[currentChat.value] = [...messages.value]
  inputMessage.value = ''
  await scrollToBottom()
  
  loading.value = true
  try {
    const response = await apiSendMessage(userMessage.content)
    const assistantMessage: Message = {
      role: 'assistant',
      content: response.response,
      timestamp: Date.now()
    }
    messages.value.push(assistantMessage)
    chatHistory.value[currentChat.value] = [...messages.value]
    await scrollToBottom()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '发送消息失败，请重试')
  } finally {
    loading.value = false
  }
}

const loadChatHistory = async () => {
  try {
    const history = await getChatHistory()
    if (history && history.length > 0) {
      messages.value = history.map((msg: any) => ({
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.timestamp).getTime()
      }))
      chatHistory.value[currentChat.value] = [...messages.value]
    }
  } catch (error: any) {
    ElMessage.error('加载聊天记录失败')
  }
}

const newChat = () => {
  currentChat.value = chatHistory.value.length
  chatHistory.value.push([])
  messages.value = []
}

const switchChat = (index: number) => {
  currentChat.value = index
  messages.value = [...chatHistory.value[index]]
  scrollToBottom()
}

const deleteChat = (index: number) => {
  if (chatHistory.value.length === 1) {
    ElMessage.warning('至少保留一个会话')
    return
  }
  
  chatHistory.value.splice(index, 1)
  if (currentChat.value === index) {
    currentChat.value = Math.max(0, index - 1)
    messages.value = [...chatHistory.value[currentChat.value]]
  } else if (currentChat.value > index) {
    currentChat.value--
  }
}

onMounted(async () => {
  await loadChatHistory()
  scrollToBottom()
})
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 112px);
  display: flex;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-sidebar {
  width: 260px;
  border-right: 1px solid var(--el-border-color-light);
  background: var(--el-bg-color-page);
  display: flex;
  flex-direction: column;
}

.chat-history {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px;
  color: var(--el-text-color-primary);
  font-size: 16px;
}

.history-list {
  flex: 1;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.history-item:hover {
  background: var(--el-color-primary-light-9);
}

.history-item.active {
  background: var(--el-color-primary-light-8);
  color: var(--el-color-primary);
}

.chat-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.delete-icon {
  opacity: 0;
  transition: opacity 0.3s;
}

.history-item:hover .delete-icon {
  opacity: 1;
}

.new-chat-btn {
  margin-top: 16px;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.message-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--el-color-primary-light-9);
  margin-bottom: 4px;
}

.message.assistant .message-text {
  background: white;
  border: 1px solid var(--el-border-color-light);
}

.message-text :deep(pre) {
  background: var(--el-bg-color);
  padding: 12px;
  border-radius: 6px;
  margin: 8px 0;
  overflow-x: auto;
}

.message-text :deep(code) {
  background: var(--el-bg-color);
  padding: 2px 4px;
  border-radius: 4px;
}

.message-text :deep(p:first-child) {
  margin-top: 0;
}

.message-text :deep(p:last-child) {
  margin-bottom: 0;
}

.message-time {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--el-text-color-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.input-area {
  border-top: 1px solid var(--el-border-color-light);
  padding: 16px 24px;
  display: flex;
  gap: 16px;
}

.send-button {
  align-self: flex-end;
}

@media (max-width: 768px) {
  .chat-sidebar {
    width: 200px;
  }
  
  .chat-title {
    font-size: 14px;
  }
  
  .message-container {
    padding: 16px;
  }
  
  .input-area {
    padding: 12px 16px;
  }
}

@media (max-width: 576px) {
  .chat-sidebar {
    display: none;
  }
  
  .message-text {
    max-width: 100%;
  }
}
</style>