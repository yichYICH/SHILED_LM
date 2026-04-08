<template>
  <div class="home-view">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="text-gradient">主动防御</span>你的知识产权
          </h1>
          <p class="hero-subtitle">
            零宽字符注入 · 同形字替换 · 动态字体映射<br>
            三重新防线，让AI爬虫无功而返
          </p>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="gotoEncrypt">
              <el-icon><Lock /></el-icon>
              立即保护文本
            </el-button>
            <el-button size="large" @click="gotoPages">
              <el-icon><Files /></el-icon>
              查看已保护页面
            </el-button>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <div class="stat-value">0</div>
              <div class="stat-label">已保护页面</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">100%</div>
              <div class="stat-label">爬虫干扰成功率</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">0ms</div>
              <div class="stat-label">用户端延迟</div>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="visual-card">
            <div class="code-preview">
              <div class="code-header">
                <div class="code-dots">
                  <span class="dot red"></span>
                  <span class="dot yellow"></span>
                  <span class="dot green"></span>
                </div>
                <span class="code-title">protected.html</span>
              </div>
              <pre class="code-content"><code>{
  "original": "这是一段重要文本",
  "protected": "这\u200b是一\u200c段\u200d重\u200b要\u200c文\u200d本",
  "font_mapping": {"U+8FD9": "U+E001"},
  "shield_level": "HIGH"
}</code></pre>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 功能特性 -->
    <section class="features-section">
      <div class="section-header">
        <h2>三重防护体系</h2>
        <p class="section-subtitle">从文本层到渲染层的纵深防御</p>
      </div>
      <div class="features-grid">
        <div class="feature-card card">
          <div class="feature-icon">
            <el-icon><Hide /></el-icon>
          </div>
          <h3 class="feature-title">文本层混淆</h3>
          <p class="feature-description">
            注入零宽字符（ZWNJ, ZWSP, ZWJ）破坏大模型分词逻辑，
            同时用视觉同形字符替换关键字母，对人眼透明但对AI爬虫致命。
          </p>
          <ul class="feature-list">
            <li>零宽字符注入</li>
            <li>同形字替换</li>
            <li>违禁指令融合</li>
          </ul>
        </div>
        <div class="feature-card card">
          <div class="feature-icon">
            <el-icon><EditPen /></el-icon>
          </div>
          <h3 class="feature-title">动态字体映射</h3>
          <p class="feature-description">
            每次访问生成随机的字体映射方案，HTML源码中的字符与显示结果完全不同。
            爬虫抓取到的是乱码，只有浏览器执行JS后才能还原。
          </p>
          <ul class="feature-list">
            <li>动态字体生成</li>
            <li>字符编码混淆</li>
            <li>缓存防逆向</li>
          </ul>
        </div>
        <div class="feature-card card">
          <div class="feature-icon">
            <el-icon><MagicStick /></el-icon>
          </div>
          <h3 class="feature-title">DOM碎片化</h3>
          <p class="feature-description">
            将文本拆分为随机顺序的DOM片段，通过CSS重新排序显示。
            爬虫解析DOM得到的文本顺序是乱的，需要计算CSS才能还原。
          </p>
          <ul class="feature-list">
            <li>DOM顺序打乱</li>
            <li>CSS布局混淆</li>
            <li>伪元素干扰</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 使用流程 -->
    <section class="workflow-section">
      <div class="section-header">
        <h2>三步完成保护</h2>
        <p class="section-subtitle">简单、快速、强大</p>
      </div>
      <div class="workflow-steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>粘贴文本</h3>
            <p>输入或粘贴需要保护的原创内容</p>
          </div>
        </div>
        <div class="step-arrow">
          <el-icon><Right /></el-icon>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>配置参数</h3>
            <p>调整零宽字符、同形字、DOM混淆强度</p>
          </div>
        </div>
        <div class="step-arrow">
          <el-icon><Right /></el-icon>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>生成分享</h3>
            <p>获得受保护页面链接，可分享至任何平台</p>
          </div>
        </div>
      </div>
      <div class="workflow-cta">
        <el-button type="primary" size="large" @click="gotoEncrypt">
          开始使用
          <el-icon><Right /></el-icon>
        </el-button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { House, Lock, Files, Hide, EditPen, MagicStick, Right, DocumentChecked } from '@element-plus/icons-vue'

const router = useRouter()

const gotoEncrypt = () => {
  router.push('/encrypt')
}

const gotoPages = () => {
  router.push('/pages')
}
</script>

<style lang="scss" scoped>
.home-view {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

// 英雄区域
.hero-section {
  padding: var(--spacing-2xl) 0;
  margin-bottom: var(--spacing-2xl);

  .hero-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-2xl);
    align-items: center;

    @media (max-width: 992px) {
      grid-template-columns: 1fr;
      gap: var(--spacing-xl);
    }
  }

  .hero-content {
    .hero-title {
      font-size: 3rem;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: var(--spacing-lg);
      letter-spacing: -0.02em;

      .text-gradient {
        font-size: inherit;
        font-weight: inherit;
      }
    }

    .hero-subtitle {
      font-size: 1.2rem;
      color: var(--color-text-secondary);
      line-height: 1.6;
      margin-bottom: var(--spacing-xl);
    }

    .hero-actions {
      display: flex;
      gap: var(--spacing-md);
      margin-bottom: var(--spacing-2xl);

      .el-button {
        padding: 0 var(--spacing-xl);
        height: 48px;
        font-size: 1rem;

        .el-icon {
          margin-right: var(--spacing-sm);
        }
      }
    }

    .hero-stats {
      display: flex;
      align-items: center;
      gap: var(--spacing-xl);
      padding: var(--spacing-lg) 0;
      border-top: 1px solid var(--color-border);

      .stat-item {
        flex: 1;
        text-align: center;

        .stat-value {
          font-size: 2rem;
          font-weight: 700;
          color: var(--color-text-accent);
          margin-bottom: var(--spacing-xs);
        }

        .stat-label {
          font-size: 0.9rem;
          color: var(--color-text-tertiary);
        }
      }

      .stat-divider {
        width: 1px;
        height: 40px;
        background: var(--color-border);
      }
    }
  }

  .hero-visual {
    .visual-card {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--spacing-lg);
      box-shadow: var(--shadow-xl);
    }

    .code-preview {
      background: #1a1d28;
      border-radius: var(--radius-md);
      overflow: hidden;

      .code-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--spacing-md);
        background: #2d3748;
        border-bottom: 1px solid var(--color-border);

        .code-dots {
          display: flex;
          gap: var(--spacing-xs);

          .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;

            &.red { background: #f56565; }
            &.yellow { background: #ecc94b; }
            &.green { background: #48bb78; }
          }
        }

        .code-title {
          font-size: 0.9rem;
          color: var(--color-text-tertiary);
          font-family: 'Consolas', monospace;
        }
      }

      .code-content {
        padding: var(--spacing-lg);
        margin: 0;
        overflow-x: auto;
        color: #e2e8f0;
        font-family: 'Consolas', monospace;
        font-size: 0.9rem;
        line-height: 1.6;

        code {
          color: inherit;
        }
      }
    }
  }
}

// 特性区域
.features-section {
  margin-bottom: var(--spacing-2xl);

  .section-header {
    text-align: center;
    margin-bottom: var(--spacing-2xl);

    h2 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: var(--spacing-sm);
    }

    .section-subtitle {
      font-size: 1.1rem;
      color: var(--color-text-secondary);
    }
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-xl);
  }

  .feature-card {
    padding: var(--spacing-xl);
    height: 100%;
    transition: transform var(--transition-base);

    &:hover {
      transform: translateY(-4px);
    }

    .feature-icon {
      width: 64px;
      height: 64px;
      background: linear-gradient(135deg, rgba(99,179,237,0.1), rgba(99,179,237,0.2));
      border-radius: var(--radius-lg);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: var(--spacing-lg);

      .el-icon {
        font-size: 1.8rem;
        color: var(--color-text-accent);
      }
    }

    .feature-title {
      font-size: 1.3rem;
      font-weight: 600;
      margin-bottom: var(--spacing-md);
      color: var(--color-text-primary);
    }

    .feature-description {
      color: var(--color-text-secondary);
      line-height: 1.6;
      margin-bottom: var(--spacing-lg);
    }

    .feature-list {
      list-style: none;
      padding: 0;
      margin: 0;

      li {
        padding: var(--spacing-xs) 0;
        color: var(--color-text-tertiary);
        position: relative;
        padding-left: var(--spacing-lg);

        &::before {
          content: '✓';
          position: absolute;
          left: 0;
          color: var(--color-text-accent);
          font-weight: bold;
        }
      }
    }
  }
}

// 工作流区域
.workflow-section {
  .section-header {
    text-align: center;
    margin-bottom: var(--spacing-2xl);

    h2 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: var(--spacing-sm);
    }

    .section-subtitle {
      font-size: 1.1rem;
      color: var(--color-text-secondary);
    }
  }

  .workflow-steps {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-xl);
    margin-bottom: var(--spacing-2xl);

    @media (max-width: 768px) {
      flex-direction: column;
      gap: var(--spacing-lg);
    }
  }

  .step {
    flex: 1;
    text-align: center;
    min-width: 200px;

    .step-number {
      width: 64px;
      height: 64px;
      background: var(--gradient-primary);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      font-weight: 700;
      color: white;
      margin: 0 auto var(--spacing-md);
      box-shadow: var(--shadow-md);
    }

    .step-content {
      h3 {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: var(--spacing-xs);
        color: var(--color-text-primary);
      }

      p {
        color: var(--color-text-secondary);
        line-height: 1.5;
      }
    }
  }

  .step-arrow {
    color: var(--color-text-tertiary);

    .el-icon {
      font-size: 1.5rem;
    }

    @media (max-width: 768px) {
      transform: rotate(90deg);
    }
  }

  .workflow-cta {
    text-align: center;

    .el-button {
      padding: 0 var(--spacing-2xl);
      height: 56px;
      font-size: 1.1rem;

      .el-icon {
        margin-left: var(--spacing-sm);
      }
    }
  }
}
</style>
