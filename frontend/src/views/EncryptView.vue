<template>
  <div class="encrypt-view">
    <div class="view-header">
      <h2>文本加密工作台</h2>
      <p class="subtitle">上传或粘贴文本，配置保护参数，生成受保护页面</p>
    </div>

    <div class="workbench">
      <!-- 左侧：输入与配置 -->
      <div class="left-panel">
        <div class="input-section card">
          <div class="section-header">
            <h3><el-icon><EditPen /></el-icon> 输入文本</h3>
            <div class="section-actions">
              <el-tooltip content="清空文本">
                <el-button size="small" text @click="clearText">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </el-tooltip>
            </div>
          </div>
          <div class="text-input-container">
            <el-input
              v-model="inputText"
              type="textarea"
              :rows="10"
              placeholder="粘贴或输入需要保护的文本内容..."
              resize="none"
              @input="handleTextChange"
            />
            <div class="text-stats">
              <span>{{ inputText.length }} 字符</span>
              <span>{{ Math.ceil(inputText.length / 400) }} 分钟阅读</span>
            </div>
          </div>
        </div>

        <div class="config-section card">
          <div class="section-header">
            <h3><el-icon><Setting /></el-icon> 保护配置</h3>
            <el-button size="small" @click="resetConfig">重置默认</el-button>
          </div>

          <div class="config-items">
            <!-- 页面标题 -->
            <div class="config-item">
              <label class="config-label">页面标题</label>
              <el-input
                v-model="pageTitle"
                placeholder="受保护页面标题"
                size="small"
              />
            </div>

            <!-- 零宽字符注入频率 -->
            <div class="config-item">
              <div class="config-header">
                <label class="config-label">零宽字符注入</label>
                <span class="config-value">{{ (zwFrequency * 100).toFixed(0) }}%</span>
              </div>
              <div class="config-slider">
                <el-slider
                  v-model="zwFrequency"
                  :min="0"
                  :max="1"
                  :step="0.05"
                  :format-tooltip="(v) => `${(v * 100).toFixed(0)}%`"
                  @input="handleConfigChange"
                />
                <div class="config-help">
                  <span class="help-text">稀疏</span>
                  <span class="help-text">适中</span>
                  <span class="help-text">密集</span>
                </div>
              </div>
            </div>

            <!-- 同形字替换比例 -->
            <div class="config-item">
              <div class="config-header">
                <label class="config-label">同形字替换</label>
                <span class="config-value">{{ (homoglyphRatio * 100).toFixed(0) }}%</span>
              </div>
              <div class="config-slider">
                <el-slider
                  v-model="homoglyphRatio"
                  :min="0"
                  :max="1"
                  :step="0.05"
                  :format-tooltip="(v) => `${(v * 100).toFixed(0)}%`"
                  @input="handleConfigChange"
                />
                <div class="config-help">
                  <span class="help-text">低</span>
                  <span class="help-text">中</span>
                  <span class="help-text">高</span>
                </div>
              </div>
            </div>

            <!-- DOM混淆强度 -->
            <div class="config-item">
              <label class="config-label">DOM混淆强度</label>
              <div class="config-options">
                <el-radio-group v-model="domIntensity" @change="handleConfigChange">
                  <el-radio-button label="low">低</el-radio-button>
                  <el-radio-button label="medium">中</el-radio-button>
                  <el-radio-button label="high">高</el-radio-button>
                </el-radio-group>
              </div>
            </div>
          </div>

          <!-- 保护强度指示器 -->
          <div class="protection-level">
            <div class="level-header">
              <span class="level-label">保护强度</span>
              <span class="level-value" :style="{ color: protectionLevel.color }">
                {{ protectionLevel.level }}
              </span>
            </div>
            <div class="level-bar">
              <div
                class="level-fill"
                :style="{
                  width: `${protectionScore}%`,
                  background: protectionLevel.color
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：预览与结果 -->
      <div class="right-panel">
        <!-- 加密结果预览 -->
        <div class="preview-section card">
          <div class="section-header">
            <h3><el-icon><View /></el-icon> 加密预览</h3>
            <div class="section-actions">
              <el-tooltip content="复制加密文本">
                <el-button size="small" :disabled="!encryptedText" @click="copyEncryptedText">
                  <el-icon><CopyDocument /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip content="显示原文">
                <el-switch
                  v-model="showOriginal"
                  size="small"
                  inline-prompt
                  active-text="原文"
                  inactive-text="加密"
                />
              </el-tooltip>
            </div>
          </div>
          <div class="preview-content">
            <div v-if="!encryptedText" class="preview-empty">
              <el-icon><Document /></el-icon>
              <p>输入文本并配置参数后，将在此显示加密结果</p>
            </div>
            <div v-else class="preview-text">
              <div class="text-container">
                <pre :class="{ 'original-view': showOriginal }">
                  {{ showOriginal ? inputText : encryptedText }}
                </pre>
              </div>
              <div class="preview-stats">
                <div class="stat-item">
                  <span class="stat-label">零宽字符</span>
                  <span class="stat-value">{{ encryptionStats?.zero_width_injected || 0 }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">同形字替换</span>
                  <span class="stat-value">{{ encryptionStats?.homoglyphs_replaced || 0 }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">文本膨胀</span>
                  <span class="stat-value">+{{ textExpansionRate }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作面板 -->
        <div class="action-section card">
          <div class="section-header">
            <h3><el-icon><MagicStick /></el-icon> 生成保护</h3>
          </div>
          <div class="action-content">
            <div v-if="loading" class="action-loading">
              <el-icon class="loading-icon"><Loading /></el-icon>
              <span>正在生成保护页面...</span>
            </div>

            <div v-else-if="pageCreated" class="action-success">
              <div class="success-header">
                <el-icon color="#48bb78"><SuccessFilled /></el-icon>
                <span>保护页面创建成功！</span>
              </div>
              <div class="success-content">
                <div class="page-info">
                  <div class="info-item">
                    <span class="info-label">页面ID</span>
                    <span class="info-value">{{ pageResult.page_id }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">访问链接</span>
                    <div class="link-container">
                      <el-input
                        :model-value="pageUrl"
                        readonly
                        size="small"
                        class="link-input"
                      />
                      <el-button size="small" @click="copyPageUrl">
                        <el-icon><CopyDocument /></el-icon>
                      </el-button>
                    </div>
                  </div>
                </div>
                <div class="action-buttons">
                  <el-button @click="openPage">
                    <el-icon><Link /></el-icon>
                    访问页面
                  </el-button>
                  <el-button type="primary" @click="createAnother">
                    <el-icon><Plus /></el-icon>
                    创建新的
                  </el-button>
                </div>
              </div>
            </div>

            <div v-else class="action-form">
              <div class="form-tip">
                <el-icon><InfoFilled /></el-icon>
                <span>生成后获得受保护页面链接，可分享至任何平台</span>
              </div>
              <div class="form-actions">
                <el-button
                  type="primary"
                  size="large"
                  :disabled="!inputText.trim()"
                  @click="generateProtectedPage"
                >
                  <el-icon><MagicStick /></el-icon>
                  生成保护页面
                </el-button>
                <el-button size="large" :disabled="!inputText.trim()" @click="testEncryption">
                  <el-icon><Refresh /></el-icon>
                  测试加密效果
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 最近创建的页面 -->
        <div v-if="recentPages.length > 0" class="recent-section card">
          <div class="section-header">
            <h3><el-icon><Clock /></el-icon> 最近创建</h3>
            <el-button size="small" text @click="gotoPages">查看全部</el-button>
          </div>
          <div class="recent-list">
            <div v-for="page in recentPages.slice(0, 3)" :key="page.id" class="recent-item">
              <div class="recent-info">
                <div class="recent-title">{{ page.title }}</div>
                <div class="recent-meta">{{ formatTime(page.createdAt) }}</div>
              </div>
              <div class="recent-actions">
                <el-tooltip content="复制链接">
                  <el-button size="small" text @click="copyRecentLink(page)">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                </el-tooltip>
                <el-tooltip content="访问">
                  <el-button size="small" text @click="openRecentPage(page)">
                    <el-icon><Link /></el-icon>
                  </el-button>
                </el-tooltip>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  EditPen, Delete, Setting, View, CopyDocument, Document,
  MagicStick, Loading, SuccessFilled, Link, Plus,
  InfoFilled, Refresh, Clock
} from '@element-plus/icons-vue'
import { useConfigStore } from '@/stores/config'
import { encryptText, copyToClipboard, getPageUrl } from '@/api'

const router = useRouter()
const configStore = useConfigStore()

// 输入文本
const inputText = ref('')
// 页面标题
const pageTitle = ref('受保护页面')
// 配置参数
const zwFrequency = ref(0.2)
const homoglyphRatio = ref(0.1)
const domIntensity = ref('medium')

// 状态
const loading = ref(false)
const showOriginal = ref(false)
const pageCreated = ref(false)

// 结果数据
const encryptedText = ref('')
const encryptionStats = ref(null)
const pageResult = ref(null)

// 计算属性
const textExpansionRate = computed(() => {
  if (!encryptionStats.value || !encryptedText.value) return 0
  const originalLen = inputText.value.length
  const encryptedLen = encryptedText.value.length
  return Math.round(((encryptedLen - originalLen) / originalLen) * 100)
})

const protectionScore = computed(() => {
  const zw = zwFrequency.value
  const hg = homoglyphRatio.value
  const dom = domIntensity.value === 'high' ? 0.25 : domIntensity.value === 'medium' ? 0.15 : 0
  return Math.round((zw * 40 + hg * 40 + dom * 100))
})

const protectionLevel = computed(() => {
  const score = protectionScore.value
  if (score >= 80) return { level: '极高', color: '#f56565' }
  if (score >= 60) return { level: '高', color: '#ed8936' }
  if (score >= 40) return { level: '中', color: '#ecc94b' }
  return { level: '低', color: '#48bb78' }
})

const pageUrl = computed(() => {
  if (!pageResult.value) return ''
  return getPageUrl(pageResult.value.page_id)
})

// 格式化加密文本：将零宽字符替换为可见符号
const formattedEncryptedText = computed(() => {
  if (!encryptedText.value) return ''
  // 零宽字符：ZWSP, ZWNJ, ZWJ, WORD JOINER, BOM, LRM, RLM
  return encryptedText.value
    .replace(/\u200B/g, '[ZWSP]')
    .replace(/\u200C/g, '[ZWNJ]')
    .replace(/\u200D/g, '[ZWJ]')
    .replace(/\u2060/g, '[WJ]')
    .replace(/\uFEFF/g, '[BOM]')
    .replace(/\u200E/g, '[LRM]')
    .replace(/\u200F/g, '[RLM]')
})

const recentPages = computed(() => configStore.recentPages)

// 方法
const handleTextChange = () => {
  if (pageCreated.value) {
    pageCreated.value = false
    encryptedText.value = ''
    encryptionStats.value = null
  }
}

const handleConfigChange = () => {
  if (pageCreated.value) {
    pageCreated.value = false
  }
}

const clearText = () => {
  inputText.value = ''
  encryptedText.value = ''
  encryptionStats.value = null
  pageCreated.value = false
}

const resetConfig = () => {
  zwFrequency.value = 0.3
  homoglyphRatio.value = 0.4
  domIntensity.value = 'medium'
  pageTitle.value = '受保护页面'
}

const copyEncryptedText = async () => {
  if (!encryptedText.value) return
  try {
    await copyToClipboard(encryptedText.value)
    ElMessage.success('加密文本已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const copyPageUrl = async () => {
  if (!pageUrl.value) return
  try {
    await copyToClipboard(pageUrl.value)
    ElMessage.success('链接已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const testEncryption = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入文本')
    return
  }

  loading.value = true
  try {
    const response = await encryptText({
      text: inputText.value,
      title: pageTitle.value,
      zw_frequency: zwFrequency.value,
      homoglyph_ratio: homoglyphRatio.value,
      dom_intensity: domIntensity.value,
    })

    encryptedText.value = response.encrypted_text
    encryptionStats.value = response.stats
    ElMessage.success('加密测试完成')
  } catch (error) {
    ElMessage.error('加密测试失败')
  } finally {
    loading.value = false
  }
}

const generateProtectedPage = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入文本')
    return
  }

  loading.value = true
  try {
    const response = await encryptText({
      text: inputText.value,
      title: pageTitle.value,
      zw_frequency: zwFrequency.value,
      homoglyph_ratio: homoglyphRatio.value,
      dom_intensity: domIntensity.value,
    })

    pageResult.value = response
    encryptedText.value = response.encrypted_text
    encryptionStats.value = response.stats
    pageCreated.value = true

    // 保存到最近列表
    configStore.addRecentPage({
      id: response.page_id,
      title: pageTitle.value,
      url: pageUrl.value,
      encryptedText: response.encrypted_text,
    })

    // 保存配置到store
    configStore.updateConfig({
      zwFrequency: zwFrequency.value,
      homoglyphRatio: homoglyphRatio.value,
      domIntensity: domIntensity.value,
      defaultTitle: pageTitle.value,
    })

    ElMessage.success('保护页面创建成功！')
  } catch (error) {
    ElMessage.error('创建失败：' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const openPage = () => {
  if (pageResult.value) {
    window.open(pageUrl.value, '_blank')
  }
}

const createAnother = () => {
  pageCreated.value = false
  pageResult.value = null
  encryptedText.value = ''
  encryptionStats.value = null
}

const gotoPages = () => {
  router.push('/pages')
}

const copyRecentLink = async (page) => {
  try {
    await copyToClipboard(page.url)
    ElMessage.success('链接已复制')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const openRecentPage = (page) => {
  window.open(page.url, '_blank')
}

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// 从store加载配置
onMounted(() => {
  const config = configStore.allConfig
  zwFrequency.value = config.zwFrequency
  homoglyphRatio.value = config.homoglyphRatio
  domIntensity.value = config.domIntensity
  pageTitle.value = config.title
})
</script>

<style lang="scss" scoped>
.encrypt-view {
  max-width: 1400px;
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

.workbench {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
}

.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

// 通用section样式
.card {
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-md);

    h3 {
      display: flex;
      align-items: center;
      gap: var(--spacing-sm);
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--color-text-primary);

      .el-icon {
        color: var(--color-text-accent);
      }
    }
  }
}

// 输入区域
.text-input-container {
  .el-textarea {
    :deep(.el-textarea__inner) {
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid var(--color-border);
      color: var(--color-text-primary);
      font-family: 'Consolas', monospace;
      resize: vertical;

      &::placeholder {
        color: var(--color-text-tertiary);
      }

      &:focus {
        border-color: var(--color-text-accent);
        box-shadow: 0 0 0 2px rgba(99, 179, 237, 0.2);
      }
    }
  }

  .text-stats {
    display: flex;
    justify-content: space-between;
    margin-top: var(--spacing-sm);
    font-size: 0.8rem;
    color: var(--color-text-tertiary);
  }
}

// 配置区域
.config-items {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.config-item {
  .config-label {
    display: block;
    margin-bottom: var(--spacing-sm);
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    font-weight: 500;
  }

  .config-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);

    .config-value {
      font-weight: 600;
      color: var(--color-text-accent);
    }
  }

  .config-slider {
    .el-slider {
      margin: var(--spacing-sm) 0;
    }

    .config-help {
      display: flex;
      justify-content: space-between;
      margin-top: var(--spacing-xs);

      .help-text {
        font-size: 0.8rem;
        color: var(--color-text-tertiary);
      }
    }
  }

  .config-options {
    .el-radio-group {
      width: 100%;

      .el-radio-button {
        flex: 1;

        :deep(.el-radio-button__inner) {
          width: 100%;
          background: rgba(0, 0, 0, 0.2);
          border: 1px solid var(--color-border);
          color: var(--color-text-secondary);

          &:hover {
            color: var(--color-text-primary);
          }
        }

        :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
          background: rgba(99, 179, 237, 0.2);
          border-color: var(--color-text-accent);
          color: var(--color-text-accent);
          box-shadow: none;
        }
      }
    }
  }
}

// 保护强度指示器
.protection-level {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);

  .level-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);

    .level-label {
      font-size: 0.9rem;
      color: var(--color-text-secondary);
    }

    .level-value {
      font-weight: 700;
      font-size: 1rem;
    }
  }

  .level-bar {
    height: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: var(--radius-full);
    overflow: hidden;

    .level-fill {
      height: 100%;
      border-radius: var(--radius-full);
      transition: all var(--transition-base);
    }
  }
}

// 预览区域
.preview-content {
  min-height: 300px;
  max-height: 400px;
  overflow-y: auto;

  .preview-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: var(--color-text-tertiary);

    .el-icon {
      font-size: 3rem;
      margin-bottom: var(--spacing-md);
      opacity: 0.5;
    }

    p {
      font-size: 0.9rem;
    }
  }

  .preview-text {
    .text-container {
      background: rgba(0, 0, 0, 0.2);
      border-radius: var(--radius-md);
      padding: var(--spacing-md);
      margin-bottom: var(--spacing-md);

      pre {
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
        line-height: 1.6;
        color: var(--color-text-primary);
        font-family: 'Consolas', monospace;
        font-size: 0.9rem;

        &.original-view {
          color: var(--color-text-secondary);
        }
      }
    }

    .preview-stats {
      display: flex;
      gap: var(--spacing-xl);
      padding: var(--spacing-md) 0;
      border-top: 1px solid var(--color-border);

      .stat-item {
        flex: 1;
        text-align: center;

        .stat-label {
          display: block;
          font-size: 0.8rem;
          color: var(--color-text-tertiary);
          margin-bottom: var(--spacing-xs);
        }

        .stat-value {
          display: block;
          font-size: 1.2rem;
          font-weight: 700;
          color: var(--color-text-accent);
        }
      }
    }
  }
}

// 操作区域
.action-content {
  .action-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-2xl) 0;

    .loading-icon {
      font-size: 2rem;
      color: var(--color-text-accent);
      margin-bottom: var(--spacing-md);
      animation: spin 1s linear infinite;
    }

    span {
      color: var(--color-text-secondary);
    }
  }

  .action-success {
    .success-header {
      display: flex;
      align-items: center;
      gap: var(--spacing-sm);
      margin-bottom: var(--spacing-lg);
      color: #48bb78;
      font-weight: 600;

      .el-icon {
        font-size: 1.2rem;
      }
    }

    .success-content {
      .page-info {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-lg);

        .info-item {
          .info-label {
            display: block;
            font-size: 0.8rem;
            color: var(--color-text-tertiary);
            margin-bottom: var(--spacing-xs);
          }

          .info-value {
            font-family: 'Consolas', monospace;
            color: var(--color-text-primary);
          }

          .link-container {
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

      .action-buttons {
        display: flex;
        gap: var(--spacing-md);
      }
    }
  }

  .action-form {
    .form-tip {
      display: flex;
      align-items: center;
      gap: var(--spacing-sm);
      padding: var(--spacing-md);
      background: rgba(99, 179, 237, 0.05);
      border-radius: var(--radius-md);
      margin-bottom: var(--spacing-lg);
      color: var(--color-text-secondary);
      font-size: 0.9rem;

      .el-icon {
        color: var(--color-text-accent);
      }
    }

    .form-actions {
      display: flex;
      gap: var(--spacing-md);

      .el-button {
        flex: 1;
        padding: var(--spacing-lg);
        font-size: 1rem;
        font-weight: 500;

        .el-icon {
          margin-right: var(--spacing-sm);
        }
      }
    }
  }
}

// 最近创建区域
.recent-list {
  .recent-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md) 0;
    border-bottom: 1px solid var(--color-border);

    &:last-child {
      border-bottom: none;
    }

    .recent-info {
      flex: 1;

      .recent-title {
        font-weight: 500;
        color: var(--color-text-primary);
        margin-bottom: var(--spacing-xs);
      }

      .recent-meta {
        font-size: 0.8rem;
        color: var(--color-text-tertiary);
      }
    }

    .recent-actions {
      display: flex;
      gap: var(--spacing-xs);
    }
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
