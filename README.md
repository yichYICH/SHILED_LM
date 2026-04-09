# SHIELD-LM (Shielding High-value Information from Extraction by Large Models) - 知识产权主动防护平台

基于文本隐写与动态字体混淆的主动防御式知识产权保护系统，防止AI爬虫采集原创内容用于大模型训练。

## 🌟 核心功能

- **文本层混淆**: 零宽字符注入 + 同形字替换 + 违禁指令融合
- **动态字体映射**: 每次访问随机字符映射，HTML源码与渲染结果分离
- **DOM碎片化**: 文本顺序与DOM顺序不一致，增加爬虫逆向难度
- **CSS伪元素干扰**: 注入不可见干扰文本，污染爬虫采集结果
- **一键外链分享**: 生成受保护页面链接，可分享至任何平台

## 🛠 技术架构

### 后端技术栈

- **框架**: FastAPI (Python)
- **算法**: 零宽字符注入、同形字替换、字体映射生成
- **数据库**: SQLite (存储保护页面数据)
- **API**: RESTful API 设计，支持跨域请求

### 前端技术栈

- **框架**: Vue.js 3 + Vite
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios

## 📁 项目结构

```
project/
├── backend/                    # FastAPI 后端
│   ├── algorithms/            # 核心算法模块
│   │   ├── text_obfuscator.py # 文本混淆算法
│   │   ├── font_generator.py  # 动态字体映射
│   │   ├── html_generator.py  # HTML页面生成
│   │   └── __init__.py
│   ├── main.py                # FastAPI主程序
│   ├── database.py            # SQLite数据库操作
│   └── requirements.txt       # Python依赖
│
├── frontend/                  # Vue.js前端
│   ├── src/
│   │   ├── views/            # 页面视图
│   │   │   ├── HomeView.vue   # 首页
│   │   │   ├── EncryptView.vue # 加密工作台
│   │   │   ├── PagesView.vue  # 页面管理
│   │   │   └── SettingsView.vue # 配置设置
│   │   ├── components/        # 公共组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia状态管理
│   │   ├── api/              # API接口封装
│   │   └── assets/           # 静态资源
│   ├── index.html            # HTML入口
│   ├── vite.config.js        # Vite配置
│   └── package.json          # 前端依赖
│
└── README.md                  # 项目说明
```

## 🚀 快速启动

### 环境要求

- Python 3.9+
- Node.js 16+
- 现代浏览器 (Chrome 90+, Firefox 88+, Safari 14+)

### 后端启动

1. 进入后端目录并安装依赖：

```bash
cd backend
pip install -r requirements.txt
```

2. 启动FastAPI服务器：

```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务器将在 `http://127.0.0.1:8000` 启动，API文档可在 `http://127.0.0.1:8000/docs` 查看。

### 前端启动

1. 进入前端目录并安装依赖：

```bash
cd frontend
npm install
```

2. 启动开发服务器：

```bash
npm run dev
```

前端将在 `http://127.0.0.1:5173` 启动，并自动代理后端API请求。

## 🔧 配置说明

### 后端配置

后端使用SQLite数据库，数据库文件将自动创建在 `backend/protected_pages.db`。

主要配置参数（在 `backend/main.py` 中）：

- CORS设置：允许的源域名
- 服务器端口：默认8000
- 数据库路径：自动管理

### 前端配置

前端配置通过Vite配置文件 `frontend/vite.config.js` 管理：

- 开发服务器端口：5173
- 代理设置：自动代理API请求到后端
- 构建配置：生产环境优化

### 保护强度配置

用户可动态调整的参数：

- **零宽字符注入频率**: 0-100%，控制不可见字符的注入密度
- **同形字替换比例**: 0-100%，控制视觉相似字符的替换比例
- **DOM混淆强度**: 低/中/高，控制DOM碎片化程度

## 📊 防护效果

### 针对的爬虫类型

1. **基础HTML解析爬虫**：直接解析HTML源码，获得乱码文本
2. **JavaScript执行爬虫**：执行JS后可获得正确文本，但受DOM碎片化干扰
3. **OCR识别爬虫**：受动态字体映射与CSS干扰层影响

### 防护层次

1. **第一层**：文本混淆（零宽字符 + 同形字）
2. **第二层**：字体映射（字符编码随机化）
3. **第三层**：DOM混淆（顺序打乱 + 伪元素干扰）
4. **第四层**：用户端还原（浏览器执行JS后正常显示）

## 🔍 API接口

### 主要端点

- `POST /api/encrypt-text` - 文本加密，创建保护页面
- `GET /api/pages` - 获取所有保护页面列表
- `DELETE /api/pages/{page_id}` - 删除保护页面
- `GET /page/{page_id}` - 访问受保护页面（返回HTML）
- `GET /api/pages/{page_id}/stats` - 获取页面访问统计

### 请求示例

```bash
# 文本加密
curl -X POST "http://127.0.0.1:8000/api/encrypt-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一段重要文本",
    "title": "示例页面",
    "zw_frequency": 0.3,
    "homoglyph_ratio": 0.4,
    "dom_intensity": "medium"
  }'
```

## 🧪 测试方案

### 功能测试

1. **文本加密工作台**: 输入文本 → 配置参数 → 生成保护页面
2. **页面管理**: 查看列表 → 访问页面 → 删除页面
3. **配置保存**: 修改配置 → 保存 → 恢复默认

### 防护效果测试

使用以下工具模拟爬虫攻击：

- **Scrapy**: 基础HTML解析
- **Playwright/Puppeteer**: JavaScript执行爬虫
- **OCR工具**: 文字识别测试

## 🔒 安全特性

- **无用户认证**: 简化使用流程，专注核心防护功能
- **本地存储**: 配置保存于浏览器localStorage
- **无外部API依赖**: 核心算法纯本地执行
- **防缓存攻击**: 动态字体映射，每次访问生成新方案

## 📈 性能指标

- **页面加载时间**: < 2秒（含动态字体加载）
- **API响应时间**: < 200ms
- **数据库操作**: SQLite，轻量高效
- **前端资源**: 压缩后 < 2MB

## 🧩 扩展开发

### 添加新的混淆算法

1. 在 `backend/algorithms/` 中创建新的算法模块
2. 实现算法接口，集成到 `text_obfuscator.py`
3. 在前端配置面板中添加对应的调节参数

### 集成外部服务

- **CDN字体托管**: 将动态字体托管至CDN加速
- **访问统计**: 集成Google Analytics或自建统计
- **用户系统**: 添加JWT认证与多用户支持

## 📚 技术原理

### 零宽字符注入

利用Unicode中的不可见字符（ZWNJ, ZWSP, ZWJ）注入文本，破坏大模型的分词逻辑。

### 同形字替换

将拉丁字母替换为视觉相似的西里尔/希腊字母，对人眼透明但对词向量编码产生偏移。

### 动态字体映射

每次访问生成随机字符映射，HTML源码存储代理字符，浏览器通过JS还原显示正确内容。

### DOM碎片化

将文本拆分为乱序DOM片段，通过CSS重新排序，增加爬虫解析难度。

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 技术支持

如遇问题，请：

1. 查看API文档 `http://127.0.0.1:8000/docs`
2. 检查浏览器控制台错误信息
3. 查看后端服务器日志

---

**🛡️ 让创作更安全，让保护更智能**
