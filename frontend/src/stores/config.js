import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useConfigStore = defineStore('config', () => {
  // 保护配置
  const zwFrequency = ref(0.3)      // 零宽字符注入频率 0-1
  const homoglyphRatio = ref(0.4)   // 同形字替换比例 0-1
  const domIntensity = ref('medium') // DOM碎片化强度 low/medium/high

  // 页面默认标题
  const defaultTitle = ref('受保护页面')

  // 最近创建的页面列表
  const recentPages = ref([])

  // 用户偏好
  const preferences = ref({
    autoCopyEncrypted: false,      // 加密后自动复制
    showOriginalPreview: true,     // 显示原文预览
    darkMode: true,                // 深色模式
    fontSize: 'medium',            // 字体大小 small/medium/large
  })

  // 计算属性：获取所有配置
  const allConfig = computed(() => ({
    zwFrequency: zwFrequency.value,
    homoglyphRatio: homoglyphRatio.value,
    domIntensity: domIntensity.value,
    title: defaultTitle.value,
    preferences: preferences.value,
  }))

  // 计算属性：保护强度描述
  const protectionLevel = computed(() => {
    const zw = zwFrequency.value
    const hg = homoglyphRatio.value
    const dom = domIntensity.value

    let score = zw * 40 + hg * 40
    if (dom === 'medium') score += 15
    if (dom === 'high') score += 25

    if (score >= 80) return { level: '极高', color: '#f56565' }
    if (score >= 60) return { level: '高', color: '#ed8936' }
    if (score >= 40) return { level: '中', color: '#ecc94b' }
    return { level: '低', color: '#48bb78' }
  })

  // 操作：更新配置
  function updateConfig(newConfig) {
    if (newConfig.zwFrequency !== undefined) {
      zwFrequency.value = Math.max(0, Math.min(1, newConfig.zwFrequency))
    }
    if (newConfig.homoglyphRatio !== undefined) {
      homoglyphRatio.value = Math.max(0, Math.min(1, newConfig.homoglyphRatio))
    }
    if (newConfig.domIntensity !== undefined) {
      domIntensity.value = ['low', 'medium', 'high'].includes(newConfig.domIntensity)
        ? newConfig.domIntensity
        : 'medium'
    }
    if (newConfig.defaultTitle !== undefined) {
      defaultTitle.value = newConfig.defaultTitle
    }
  }

  // 操作：更新偏好设置
  function updatePreferences(newPrefs) {
    preferences.value = { ...preferences.value, ...newPrefs }
  }

  // 操作：添加最近创建的页面
  function addRecentPage(pageData) {
    recentPages.value.unshift({
      id: pageData.id,
      title: pageData.title,
      url: pageData.url,
      encryptedText: pageData.encryptedText,
      createdAt: new Date().toISOString(),
    })
    // 只保留最近10个
    if (recentPages.value.length > 10) {
      recentPages.value = recentPages.value.slice(0, 10)
    }
  }

  // 操作：从最近列表中移除页面
  function removeRecentPage(pageId) {
    recentPages.value = recentPages.value.filter(page => page.id !== pageId)
  }

  // 操作：重置配置
  function resetConfig() {
    zwFrequency.value = 0.3
    homoglyphRatio.value = 0.4
    domIntensity.value = 'medium'
    defaultTitle.value = '受保护页面'
  }

  // 操作：保存到 localStorage
  function saveToStorage() {
    const data = {
      config: {
        zwFrequency: zwFrequency.value,
        homoglyphRatio: homoglyphRatio.value,
        domIntensity: domIntensity.value,
        defaultTitle: defaultTitle.value,
      },
      preferences: preferences.value,
    }
    localStorage.setItem('ipShieldConfig', JSON.stringify(data))
  }

  // 操作：从 localStorage 加载
  function loadFromStorage() {
    const saved = localStorage.getItem('ipShieldConfig')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        if (data.config) {
          updateConfig(data.config)
        }
        if (data.preferences) {
          updatePreferences(data.preferences)
        }
      } catch (error) {
        console.error('加载配置失败:', error)
      }
    }
  }

  return {
    // 状态
    zwFrequency,
    homoglyphRatio,
    domIntensity,
    defaultTitle,
    recentPages,
    preferences,

    // 计算属性
    allConfig,
    protectionLevel,

    // 操作
    updateConfig,
    updatePreferences,
    addRecentPage,
    removeRecentPage,
    resetConfig,
    saveToStorage,
    loadFromStorage,
  }
})
