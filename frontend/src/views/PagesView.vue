<template>
  <div class="pages-view">
    <div class="view-header">
      <h2>我的保护页面</h2>
      <p class="subtitle">查看、管理和访问所有已创建的保护页面</p>
    </div>

    <div class="pages-container">
      <!-- 页面列表 -->
      <div v-if="pages.length > 0" class="pages-grid">
        <div v-for="page in pages" :key="page.id" class="page-card card">
          <div class="page-header">
            <div class="page-title">
              <h3>{{ page.title || '未命名页面' }}</h3>
              <span class="page-id">ID: {{ page.id }}</span>
            </div>
            <div class="page-actions">
              <el-dropdown>
                <el-button size="small" text>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="openPage(page)">
                      <el-icon><Link /></el-icon>
                      访问页面
                    </el-dropdown-item>
                    <el-dropdown-item @click="copyPageLink(page)">
                      <el-icon><CopyDocument /></el-icon>
                      复制链接
                    </el-dropdown-item>
                    <el-dropdown-item @click="showStats(page)">
                      <el-icon><DataLine /></el-icon>
                      查看统计
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="confirmDelete(page)" class="delete-item">
                      <el-icon><Delete /></el-icon>
                      删除页面
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>

          <div class="page-content">
            <div class="page-info">
              <div class="info-row">
                <el-icon><Calendar /></el-icon>
                <span>创建时间: {{ formatDate(page.created_at) }}</span>
              </div>
              <div class="info-row">
                <el-icon><View /></el-icon>
                <span>访问次数: {{ page.view_count || 0 }}</span>
              </div>
            </div>
          </div>

          <div class="page-footer">
            <el-button size="small" @click="openPage(page)">
              <el-icon><Link /></el-icon>
              访问页面
            </el-button>
            <el-button size="small" @click="copyPageLink(page)">
              <el-icon><CopyDocument /></el-icon>
              复制链接
            </el-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <div class="empty-content">
          <el-icon class="empty-icon"><Files /></el-icon>
          <h3>暂无保护页面</h3>
          <p>您还没有创建任何保护页面，快去保护您的第一份文本内容吧！</p>
          <el-button type="primary" @click="gotoEncrypt">
            <el-icon><Plus /></el-icon>
            创建第一个保护页面
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计对话框 -->
    <el-dialog
      v-model="statsDialogVisible"
      title="页面统计"
      width="400px"
      :close-on-click-modal="false"
    >
      <div v-if="selectedPage" class="stats-dialog">
        <div class="stats-header">
          <h4>{{ selectedPage.title || '未命名页面' }}</h4>
          <span class="page-id">ID: {{ selectedPage.id }}</span>
        </div>
        <div class="stats-content">
          <div class="stat-item">
            <div class="stat-label">创建时间</div>
            <div class="stat-value">{{ formatDate(selectedPage.created_at) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">访问次数</div>
            <div class="stat-value">{{ selectedPage.view_count || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">页面链接</div>
            <div class="stat-link">
              <el-input
                :model-value="getPageUrl(selectedPage.id)"
                readonly
                size="small"
                class="link-input"
              />
              <el-button size="small" @click="copyPageLink(selectedPage)">
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="delete-dialog">
        <div class="delete-warning">
          <el-icon color="#f56565"><Warning /></el-icon>
          <p>确定要删除页面 <strong>{{ deletingPage?.title || deletingPage?.id }}</strong> 吗？</p>
        </div>
        <p class="delete-hint">此操作不可撤销，页面链接将立即失效。</p>
        <div class="delete-actions">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="handleDeletePage" :loading="deleting">
            确认删除
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  MoreFilled, Link, CopyDocument, DataLine, Delete,
  Calendar, View, Files, Plus, Warning
} from '@element-plus/icons-vue'
import { getPages, deletePage, getPageUrl } from '@/api'

const router = useRouter()

// 数据
const pages = ref([])
const loading = ref(true)
const selectedPage = ref(null)
const deletingPage = ref(null)

// 对话框状态
const statsDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const deleting = ref(false)

// 方法
const loadPages = async () => {
  loading.value = true
  try {
    const response = await getPages()
    pages.value = response.pages || []
  } catch (error) {
    ElMessage.error('加载页面列表失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const openPage = (page) => {
  window.open(getPageUrl(page.id), '_blank')
}

const copyPageLink = async (page) => {
  try {
    await navigator.clipboard.writeText(getPageUrl(page.id))
    ElMessage.success('链接已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const showStats = (page) => {
  selectedPage.value = page
  statsDialogVisible.value = true
}

const confirmDelete = (page) => {
  deletingPage.value = page
  deleteDialogVisible.value = true
}

const handleDeletePage = async () => {
  if (!deletingPage.value) return

  deleting.value = true
  try {
    await deletePage(deletingPage.value.id)
    ElMessage.success('页面删除成功')
    // 从列表中移除
    pages.value = pages.value.filter(p => p.id !== deletingPage.value.id)
    deleteDialogVisible.value = false
  } catch (error) {
    ElMessage.error('删除失败：' + (error.response?.data?.detail || error.message))
  } finally {
    deleting.value = false
    deletingPage.value = null
  }
}

const gotoEncrypt = () => {
  router.push('/encrypt')
}

// 生命周期
onMounted(() => {
  loadPages()
})
</script>

<style lang="scss" scoped>
.pages-view {
  max-width: 1200px;
  margin: 0 auto;

  .view-header {
    margin-bottom: var(--spacing-xl);

    h2 {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: var(--spacing-sm);
      color: var(--color-text-primary);
    }

    .subtitle {
      color: var(--color-text-secondary);
      font-size: 1rem;
    }
  }
}

.pages-container {
  .pages-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: var(--spacing-lg);

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }
}

.page-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: all var(--transition-base);

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-md);
    border-bottom: 1px solid var(--color-border);

    .page-title {
      flex: 1;

      h3 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: var(--spacing-xs);
        line-height: 1.4;
        word-break: break-word;
      }

      .page-id {
        font-size: 0.75rem;
        color: var(--color-text-tertiary);
        font-family: 'Consolas', monospace;
      }
    }

    .page-actions {
      .delete-item {
        color: #f56565;
      }
    }
  }

  .page-content {
    flex: 1;
    margin-bottom: var(--spacing-md);

    .page-info {
      .info-row {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        padding: var(--spacing-xs) 0;
        color: var(--color-text-secondary);
        font-size: 0.9rem;

        .el-icon {
          font-size: 0.9rem;
          color: var(--color-text-tertiary);
        }
      }
    }
  }

  .page-footer {
    display: flex;
    gap: var(--spacing-sm);
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--color-border);

    .el-button {
      flex: 1;
    }
  }
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;

  .empty-content {
    text-align: center;
    max-width: 400px;

    .empty-icon {
      font-size: 4rem;
      color: var(--color-text-tertiary);
      opacity: 0.5;
      margin-bottom: var(--spacing-lg);
    }

    h3 {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: var(--spacing-sm);
      color: var(--color-text-primary);
    }

    p {
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-xl);
      line-height: 1.6;
    }

    .el-button {
      padding: 0 var(--spacing-xl);
      height: 48px;
      font-size: 1rem;

      .el-icon {
        margin-right: var(--spacing-sm);
      }
    }
  }
}

// 统计对话框
.stats-dialog {
  .stats-header {
    margin-bottom: var(--spacing-lg);

    h4 {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--spacing-xs);
    }

    .page-id {
      font-size: 0.85rem;
      color: var(--color-text-tertiary);
      font-family: 'Consolas', monospace;
    }
  }

  .stats-content {
    .stat-item {
      margin-bottom: var(--spacing-lg);

      &:last-child {
        margin-bottom: 0;
      }

      .stat-label {
        font-size: 0.9rem;
        color: var(--color-text-secondary);
        margin-bottom: var(--spacing-xs);
      }

      .stat-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--color-text-primary);
      }

      .stat-link {
        display: flex;
        gap: var(--spacing-sm);

        .link-input {
          flex: 1;

          :deep(.el-input__inner) {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--color-border);
            color: var(--color-text-primary);
            font-size: 0.9rem;
          }
        }
      }
    }
  }
}

// 删除对话框
.delete-dialog {
  .delete-warning {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);

    .el-icon {
      font-size: 1.5rem;
      flex-shrink: 0;
    }

    p {
      color: var(--color-text-primary);
      line-height: 1.5;

      strong {
        color: var(--color-text-accent);
        font-weight: 600;
      }
    }
  }

  .delete-hint {
    color: var(--color-text-tertiary);
    font-size: 0.9rem;
    margin-bottom: var(--spacing-lg);
  }

  .delete-actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-md);
  }
}
</style>
