<template>
  <div id="app">
    <header class="main-header">
      <div class="header-container">
        <div class="logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke-linejoin="round"/>
          </svg>
          <h1>IP Shield</h1>
          <span class="tag">Beta</span>
        </div>
        <nav class="nav-menu">
          <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </router-link>
          <router-link to="/encrypt" class="nav-item" :class="{ active: $route.path === '/encrypt' }">
            <el-icon><Lock /></el-icon>
            <span>文本加密</span>
          </router-link>
          <router-link to="/pages" class="nav-item" :class="{ active: $route.path === '/pages' }">
            <el-icon><Files /></el-icon>
            <span>我的页面</span>
          </router-link>
          <router-link to="/settings" class="nav-item" :class="{ active: $route.path === '/settings' }">
            <el-icon><Setting /></el-icon>
            <span>保护配置</span>
          </router-link>
        </nav>
        <div class="header-actions">
          <el-button type="primary" size="small" @click="gotoEncrypt">
            <el-icon><Plus /></el-icon>
            新建保护
          </el-button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="main-footer">
      <div class="footer-container">
        <div class="footer-left">
          <div class="brand">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#63b3ed" stroke-width="2">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke-linejoin="round"/>
            </svg>
            <span>IP Shield</span>
          </div>
          <p class="slogan">主动防御式知识产权保护 · 让AI爬虫无功而返</p>
        </div>
        <div class="footer-right">
          <p class="copyright">
            © 2026 IP Shield 知识产权主动防护平台<br>
            基于零宽字符、同形字替换与动态字体映射技术
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { House, Lock, Files, Setting, Plus } from '@element-plus/icons-vue'

const router = useRouter()

const gotoEncrypt = () => {
  router.push('/encrypt')
}
</script>

<style lang="scss" scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #0a0e1a;
  color: #e2e8f0;
}

.main-header {
  background: rgba(10, 14, 26, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(99, 179, 237, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 0 24px;

  .header-container {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
    user-select: none;

    h1 {
      font-size: 1.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #63b3ed, #4299e1);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      letter-spacing: 0.05em;
    }

    .tag {
      background: rgba(99, 179, 237, 0.1);
      border: 1px solid rgba(99, 179, 237, 0.3);
      color: #63b3ed;
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 12px;
      margin-left: 8px;
    }
  }

  .nav-menu {
    display: flex;
    gap: 32px;
    margin-left: 48px;

    .nav-item {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #718096;
      text-decoration: none;
      font-size: 0.95rem;
      padding: 8px 12px;
      border-radius: 8px;
      transition: all 0.2s ease;

      &:hover {
        color: #e2e8f0;
        background: rgba(99, 179, 237, 0.05);
      }

      &.active {
        color: #63b3ed;
        background: rgba(99, 179, 237, 0.1);
      }

      .el-icon {
        font-size: 1.1rem;
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 12px;
  }
}

.main-content {
  flex: 1;
  padding: 32px 24px;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
}

.main-footer {
  background: rgba(10, 14, 26, 0.95);
  border-top: 1px solid rgba(99, 179, 237, 0.1);
  padding: 32px 24px;
  margin-top: auto;

  .footer-container {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 24px;
  }

  .footer-left {
    display: flex;
    flex-direction: column;
    gap: 8px;

    .brand {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 1.1rem;
      font-weight: 600;
      color: #63b3ed;
    }

    .slogan {
      color: #718096;
      font-size: 0.9rem;
    }
  }

  .footer-right {
    .copyright {
      color: #4a5568;
      font-size: 0.8rem;
      line-height: 1.5;
      text-align: right;
    }
  }
}

// 页面切换动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
