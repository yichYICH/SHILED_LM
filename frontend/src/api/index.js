import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加认证token等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      const message = data?.detail || data?.message || `请求失败 (${status})`

      // 统一错误提示（可根据需要接入 Element Plus 的 Message 组件）
      console.error(`API Error [${status}]:`, message)

      // 特殊处理 404
      if (status === 404) {
        // 页面不存在
      }
    } else if (error.request) {
      console.error('API Network Error:', error.message)
    } else {
      console.error('API Error:', error.message)
    }

    return Promise.reject(error)
  }
)

// ──────────────────────────────
// API 方法
// ──────────────────────────────

/**
 * 文本加密
 * @param {Object} params 加密参数
 * @returns {Promise} 加密结果
 */
export const encryptText = (params) => {
  return api.post('/encrypt-text', params)
}

/**
 * 获取所有保护页面列表
 * @returns {Promise} 页面列表
 */
export const getPages = () => {
  return api.get('/pages')
}

/**
 * 获取页面统计信息
 * @param {string} pageId 页面ID
 * @returns {Promise} 统计信息
 */
export const getPageStats = (pageId) => {
  return api.get(`/pages/${pageId}/stats`)
}

/**
 * 删除保护页面
 * @param {string} pageId 页面ID
 * @returns {Promise} 删除结果
 */
export const deletePage = (pageId) => {
  return api.delete(`/pages/${pageId}`)
}

/**
 * 健康检查
 * @returns {Promise} 健康状态
 */
export const healthCheck = () => {
  return api.get('/health')
}

/**
 * 获取受保护页面的完整URL
 * @param {string} pageId 页面ID
 * @returns {string} 完整URL
 */
export const getPageUrl = (pageId) => {
  return `${window.location.origin}/page/${pageId}`
}

/**
 * 复制到剪贴板
 * @param {string} text 要复制的文本
 * @returns {Promise} 复制结果
 */
export const copyToClipboard = (text) => {
  return navigator.clipboard.writeText(text)
}

export default api
