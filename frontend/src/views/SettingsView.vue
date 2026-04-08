<template>
  <div class="settings-view">
    <div class="view-header">
      <h2>保护配置</h2>
      <p class="subtitle">自定义默认保护参数和偏好设置</p>
    </div>

    <div class="settings-container">
      <div class="settings-grid">
        <!-- 默认保护配置 -->
        <div class="settings-section card">
          <div class="section-header">
            <h3><el-icon><Lock /></el-icon> 默认保护配置</h3>
            <el-button size="small" @click="resetToDefaults">恢复默认</el-button>
          </div>
          <div class="section-content">
            <!-- 零宽字符注入频率 -->
            <div class="config-item">
              <div class="config-header">
                <label class="config-label">零宽字符注入频率</label>
                <span class="config-value">{{ (config.zwFrequency * 100).toFixed(0) }}%</span>
              </div>
              <div class="config-slider">
                <el-slider
                  v-model="config.zwFrequency"
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
              <p class="config-description">
                控制零宽字符（ZWNJ、ZWSP、ZWJ）的注入密度。高频注入可有效破坏大模型分词，但可能影响部分渲染引擎。
              </p>
            </div>

            <!-- 同形字替换比例 -->
            <div class="config-item">
              <div class="config-header">
                <label class="config-label">同形字替换比例</label>
                <span class="config-value">{{ (config.homoglyphRatio * 100).toFixed(0) }}%</span>
              </div>
              <div class="config-slider">
                <el-slider
                  v-model="config.homoglyphRatio"
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
              <p class="config-description">
                将拉丁字母替换为视觉相似的西里尔/希腊字母。高替换比例对大模型词向量干扰更强，但可能在特定字体下暴露。
              </p>
            </div>

            <!-- DOM混淆强度 -->
            <div class="config-item">
              <label class="config-label">DOM混淆强度</label>
              <div class="config-options">
                <el-radio-group v-model="config.domIntensity" @change="handleConfigChange">
                  <el-radio-button label="low">低</el-radio-button>
                  <el-radio-button label="medium">中</el-radio-button>
                  <el-radio-button label="high">高</el-radio-button>
                </el-radio-group>
              </div>
              <p class="config-description">
                控制DOM碎片化与CSS混淆的强度。高强度可有效对抗现代AI爬虫，但可能轻微影响页面性能。
              </p>
            </div>

            <!-- 默认页面标题 -->
            <div class="config-item">
              <label class="config-label">默认页面标题</label>
              <el-input
                v-model="config.defaultTitle"
                placeholder="受保护页面"
                size="small"
                @input="handleConfigChange"
              />
              <p class="config-description">
                创建新保护页面时使用的默认标题。
              </p>
            </div>
          </div>
        </div>

        <!-- 偏好设置 -->
        <div class="settings-section card">
          <div class="section-header">
            <h3><el-icon><Setting /></el-icon> 偏好设置</h3>
          </div>
          <div class="section-content">
            <!-- 自动复制加密文本 -->
            <div class="preference-item">
              <div class="preference-main">
                <label class="preference-label">加密后自动复制文本</label>
                <el-switch
                  v-model="preferences.autoCopyEncrypted"
                  @change="handlePreferenceChange"
                />
              </div>
              <p class="preference-description">
                生成加密文本后自动复制到剪贴板，方便直接使用。
              </p>
            </div>

            <!-- 显示原文预览 -->
            <div class="preference-item">
              <div class="preference-main">
                <label class="preference-label">显示原文预览</label>
                <el-switch
                  v-model="preferences.showOriginalPreview"
                  @change="handlePreferenceChange"
                />
              </div>
              <p class="preference-description">
                在加密工作台中默认显示原文与加密文本的对比预览。
              </p>
            </div>

            <!-- 深色模式 -->
            <div class="preference-item">
              <div class="preference-main">
                <label class="preference-label">深色模式</label>
                <el-switch
                  v-model="preferences.darkMode"
                  @change="handlePreferenceChange"
                />
              </div>
              <p class="preference-description">
                使用深色主题界面，更适合长时间工作。
              </p>
            </div>

            <!-- 字体大小 -->
            <div class="preference-item">
              <label class="preference-label">界面字体大小</label>
              <div class="config-options">
                <el-radio-group v-model="preferences.fontSize" @change="handlePreferenceChange">
                  <el-radio-button label="small">小</el-radio-button>
                  <el-radio-button label="medium">中</el-radio-button>
                  <el-radio-button label="large">大</el-radio-button>
                </el-radio-group>
              </div>
              <p class="preference-description">
                调整界面整体字体大小。
              </p>
            </div>
          </div>
        </div>

        <!-- 保护强度预览 -->
        <div class="settings-section card">
          <div class="section-header">
            <h3><el-icon><DataLine /></el-icon> 保护强度预览</h3>
          </div>
          <div class="section-content">
            <div class="protection-preview">
              <div class="protection-header">
                <span class="protection-label">当前配置的保护强度</span>
                <span class="protection-value" :style="{ color: protectionLevel.color }">
                  {{ protectionLevel.level }}
                </span>
              </div>
              <div class="protection-bar">
                <div
                  class="protection-fill"
                  :style="{
                    width: `${protectionScore}%`,
                    background: protectionLevel.color
                  }"
                ></div>
              </div>
              <div class="protection-breakdown">
                <div class="breakdown-item">
                  <span class="breakdown-label">零宽字符</span>
                  <div class="breakdown-bar">
                    <div class="breakdown-fill" :style="{ width: `${config.zwFrequency * 100}%`, background: '#63b3ed' }"></div>
                  </div>
                  <span class="breakdown-value">{{ (config.zwFrequency * 100).toFixed(0) }}%</span>
                </div>
                <div class="breakdown-item">
                  <span class="breakdown-label">同形字替换</span>
                  <div class="breakdown-bar">
                    <div class="breakdown-fill" :style="{ width: `${config.homoglyphRatio * 100}%`, background: '#9f7aea' }"></div>
                  </div>
                  <span class="breakdown-value">{{ (config.homoglyphRatio * 100).toFixed(0) }}%</span>
                </div>
                <div class="breakdown-item">
                  <span class="breakdown-label">DOM混淆</span>
                  <div class="breakdown-bar">
                    <div class="breakdown-fill" :style="{ width: domIntensityScore, background: '#ed8936' }"></div>
                  </div>
                  <span class="breakdown-value">{{ domIntensityLabel }}</span>
                </div>
              </div>
              <div class="protection-tip">
                <el-icon><InfoFilled /></el-icon>
                <span>保护强度越高，对AI爬虫的干扰效果越强，但也可能轻微影响页面加载性能。</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作区 -->
        <div class="settings-section card">
          <div class="section-header">
            <h3><el-icon><Operation /></el-icon> 操作</h3>
          </div>
          <div class="section-content">
            <div class="action-buttons">
              <el-button type="primary" @click="saveSettings">
                <el-icon><Check /></el-icon>
                保存设置
              </el-button>
              <el-button @click="resetToDefaults">
                <el-icon><Refresh /></el-icon>
                恢复默认
              </el-button>
              <el-button @click="exportSettings">
                <el-icon><Download /></el-icon>
                导出配置
              </el-button>
              <el-button @click="importSettings">
                <el-icon><Upload /></el-icon>
                导入配置
              </el-button>
            </div>
            <div class="action-tips">
              <p><strong>提示：</strong></p>
              <ul>
                <li>配置会自动保存到本地浏览器存储</li>
                <li>不同设备间的配置不会同步</li>
                <li>导出配置可在其他设备或浏览器间迁移设置</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Lock, Setting, DataLine, Operation, Check,
  Refresh, Download, Upload, InfoFilled
} from '@element-plus/icons-vue'
import { useConfigStore } from '@/stores/config'

const configStore = useConfigStore()

// 配置数据
const config = ref({
  zwFrequency: 0.3,
  homoglyphRatio: 0.4,
  domIntensity: 'medium',
  defaultTitle: '受保护页面',
})

const preferences = ref({
  autoCopyEncrypted: false,
  showOriginalPreview: true,
  darkMode: true,
  fontSize: 'medium',
})

// 计算属性
const protectionScore = computed(() => {
  const zw = config.value.zwFrequency
  const hg = config.value.homoglyphRatio
  const dom = config.value.domIntensity === 'high' ? 0.25 : config.value.domIntensity === 'medium' ? 0.15 : 0
  return Math.round((zw * 40 + hg * 40 + dom * 100))
})

const protectionLevel = computed(() => {
  const score = protectionScore.value
  if (score >= 80) return { level: '极高', color: '#f56565' }
  if (score >= 60) return { level: '高', color: '#ed8936' }
  if (score >= 40) return { level: '中', color: '#ecc94b' }
  return { level: '低', color: '#48bb78' }
})

const domIntensityScore = computed(() => {
  switch (config.value.domIntensity) {
    case 'low': return '25%'
    case 'medium': return '50%'
    case 'high': return '100%'
    default: return '50%'
  }
})

const domIntensityLabel = computed(() => {
  switch (config.value.domIntensity) {
    case 'low': return '低'
    case 'medium': return '中'
    case 'high': return '高'
    default: return '中'
  }
})

// 方法
const loadSettings = () => {
  configStore.loadFromStorage()
  const storeConfig = configStore.allConfig
  const storePrefs = configStore.preferences

  config.value = {
    zwFrequency: storeConfig.zwFrequency,
    homoglyphRatio: storeConfig.homoglyphRatio,
    domIntensity: storeConfig.domIntensity,
    defaultTitle: storeConfig.title,
  }

  preferences.value = { ...storePrefs }
}

const handleConfigChange = () => {
  // 实时更新store中的配置
  configStore.updateConfig(config.value)
}

const handlePreferenceChange = () => {
  configStore.updatePreferences(preferences.value)
}

const saveSettings = () => {
  configStore.saveToStorage()
  ElMessage.success('设置已保存')
}

const resetToDefaults = () => {
  config.value = {
    zwFrequency: 0.3,
    homoglyphRatio: 0.4,
    domIntensity: 'medium',
    defaultTitle: '受保护页面',
  }

  preferences.value = {
    autoCopyEncrypted: false,
    showOriginalPreview: true,
    darkMode: true,
    fontSize: 'medium',
  }

  configStore.updateConfig(config.value)
  configStore.updatePreferences(preferences.value)
  ElMessage.success('已恢复默认设置')
}

const exportSettings = () => {
  const data = {
    config: config.value,
    preferences: preferences.value,
    version: '1.0',
    exportDate: new Date().toISOString(),
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ip-shield-config-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)

  ElMessage.success('配置已导出')
}

const importSettings = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'application/json'
  input.onchange = (event) => {
    const file = event.target.files[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result)
        if (data.config) {
          config.value = { ...config.value, ...data.config }
          configStore.updateConfig(config.value)
        }
        if (data.preferences) {
          preferences.value = { ...preferences.value, ...data.preferences }
          configStore.updatePreferences(preferences.value)
        }
        ElMessage.success('配置已导入')
      } catch (error) {
        ElMessage.error('配置文件格式错误')
      }
    }
    reader.readAsText(file)
  }
  input.click()
}

// 生命周期
onMounted(() => {
  loadSettings()
})
</script>

<style lang="scss" scoped>
.settings-view {
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

.settings-container {
  .settings-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-lg);

    @media (max-width: 992px) {
      grid-template-columns: 1fr;
    }
  }

  .settings-section {
    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: var(--spacing-lg);

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

    .section-content {
      .config-item,
      .preference-item {
        margin-bottom: var(--spacing-xl);

        &:last-child {
          margin-bottom: 0;
        }
      }
    }
  }
}

// 配置项样式
.config-item {
  .config-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);

    .config-label {
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--color-text-primary);
    }

    .config-value {
      font-weight: 600;
      color: var(--color-text-accent);
    }
  }

  .config-slider {
    margin-bottom: var(--spacing-sm);

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
    margin-bottom: var(--spacing-sm);

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

  .config-description {
    font-size: 0.85rem;
    color: var(--color-text-tertiary);
    line-height: 1.5;
    margin-top: var(--spacing-xs);
  }
}

// 偏好项样式
.preference-item {
  .preference-main {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-xs);

    .preference-label {
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--color-text-primary);
    }
  }

  .preference-description {
    font-size: 0.85rem;
    color: var(--color-text-tertiary);
    line-height: 1.5;
  }
}

// 保护强度预览
.protection-preview {
  .protection-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);

    .protection-label {
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--color-text-primary);
    }

    .protection-value {
      font-weight: 700;
      font-size: 1rem;
    }
  }

  .protection-bar {
    height: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: var(--radius-full);
    overflow: hidden;
    margin-bottom: var(--spacing-lg);

    .protection-fill {
      height: 100%;
      border-radius: var(--radius-full);
      transition: all var(--transition-base);
    }
  }

  .protection-breakdown {
    .breakdown-item {
      display: flex;
      align-items: center;
      gap: var(--spacing-md);
      margin-bottom: var(--spacing-md);

      &:last-child {
        margin-bottom: 0;
      }

      .breakdown-label {
        width: 80px;
        font-size: 0.9rem;
        color: var(--color-text-secondary);
      }

      .breakdown-bar {
        flex: 1;
        height: 4px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: var(--radius-full);
        overflow: hidden;

        .breakdown-fill {
          height: 100%;
          border-radius: var(--radius-full);
          transition: all var(--transition-base);
        }
      }

      .breakdown-value {
        width: 50px;
        text-align: right;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--color-text-accent);
      }
    }
  }

  .protection-tip {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-lg);
    padding: var(--spacing-md);
    background: rgba(99, 179, 237, 0.05);
    border-radius: var(--radius-md);
    color: var(--color-text-secondary);
    font-size: 0.85rem;

    .el-icon {
      color: var(--color-text-accent);
      flex-shrink: 0;
    }
  }
}

// 操作区
.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);

  .el-button {
    .el-icon {
      margin-right: var(--spacing-sm);
    }
  }
}

.action-tips {
  background: rgba(0, 0, 0, 0.1);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);

  p {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-sm);
  }

  ul {
    margin: 0;
    padding-left: var(--spacing-lg);
    color: var(--color-text-tertiary);
    font-size: 0.85rem;
    line-height: 1.6;

    li {
      margin-bottom: var(--spacing-xs);
    }
  }
}
</style>
