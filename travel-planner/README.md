# 旅游规划生成器

这是一个基于React开发的旅游规划应用，可以帮助用户根据选择的城市、类别和子类别生成个性化的旅游规划。

## 功能特点

- 📍 城市选择：提供多个城市选项供用户选择
- 🏛️ 类别筛选：按照人文景观、自然景观、饮食文化等类别进行筛选
- 🎯 子类别选择：根据用户兴趣提供更细分的旅游体验
- 📝 规划生成：利用AI技术生成详细的旅游行程规划
- 💾 规划保存：支持下载和保存生成的旅游规划
- 📱 响应式设计：适配各种屏幕尺寸

## 技术栈

- React：前端框架
- TypeScript：类型检查
- Ant Design：UI组件库
- Jotai：轻量级状态管理
- React Router：路由管理
- Axios：HTTP请求
- React Markdown：Markdown渲染

## 运行指南

### 前提条件

确保您的系统已安装以下软件：
- Node.js (v14.0.0 或更高版本)
- npm (v6.0.0 或更高版本)

### 安装依赖

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/travel-planner.git
```

2. 进入项目目录：
```bash
cd travel-planner
```

3. 进入前端目录：
```bash
cd frontend
```

4. 安装依赖：
```bash
npm install
```

### 启动应用

在前端目录中运行：
```bash
npm start
```

应用将会在开发模式下启动，自动打开浏览器并访问 [http://localhost:3000](http://localhost:3000)。

### 构建生产版本

```bash
npm run build
```

这将在 `build` 文件夹中生成应用的生产版本。

## 使用指南

### 1. 首页

首页展示可选择的城市列表。点击任意城市卡片，进入该城市的详情页面。

### 2. 城市详情页

城市详情页展示该城市的旅游类别选项，如人文景观、自然景观、饮食文化等。点击感兴趣的类别，进入类别详情页面。

### 3. 类别详情页

类别详情页展示所选类别的子类别选项，如历史古迹、博物馆、传统建筑等。点击"生成旅游规划"按钮，开始生成旅游规划。

### 4. 规划生成页

系统将根据您选择的城市、类别和子类别生成个性化的旅游规划。页面显示生成进度，完成后将自动跳转到结果页面。

### 5. 结果页面

结果页面展示生成的旅游规划，包括行程安排、景点介绍、餐饮推荐、住宿信息等。您可以：
- 下载规划：将规划保存为Markdown文件
- 复制内容：将规划内容复制到剪贴板
- 保存规划：将规划保存到服务器
- 返回首页：返回首页重新选择城市

## 目录结构

```
travel-planner/
├── frontend/                # 前端代码
│   ├── public/              # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   ├── utils/           # 工具函数
│   │   ├── App.tsx          # 主应用组件
│   │   ├── App.css          # 全局样式
│   │   ├── index.tsx        # 入口文件
│   ├── package.json         # 依赖配置
├── README.md                # 项目说明
```

## 常见问题

### Q: 规划生成过程中如何取消？
A: 在规划生成页面，点击"取消"按钮可以返回上一级页面。

### Q: 如何更改已选择的城市？
A: 点击顶部导航栏的"返回首页"按钮，或者点击页面路径导航中的相应链接。

### Q: 生成的规划是否可以编辑？
A: 当前版本不支持直接编辑生成的规划，但您可以下载规划文件后进行编辑。

## 后续开发计划

- [ ] 添加用户账户系统，支持规划收藏和分享
- [ ] 增加更多城市和景点数据
- [ ] 提供规划定制功能，如天数调整、预算限制等
- [ ] 集成地图功能，直观展示行程路线
- [ ] 增加多语言支持

## 贡献指南

如果您想为项目做出贡献，请：
1. Fork 项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 开源协议

该项目采用 MIT 协议 - 详见 LICENSE 文件。 