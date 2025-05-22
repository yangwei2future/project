# 旅游规划生成器 - 一键启动指南

本文档提供了使用一键启动脚本运行旅游规划生成器的详细说明。

## 启动方式

### Windows系统

1. 双击 `start_project.bat` 文件
2. 或在命令提示符中执行：
   ```
   python start_project.py
   ```

### macOS/Linux系统

1. 在终端中执行：
   ```
   ./start_project.sh
   ```
   
2. 或直接执行：
   ```
   python3 start_project.py
   ```

## 功能说明

启动脚本会自动完成以下操作：

1. 检查环境依赖（Python版本、必要的Python包、Node.js等）
2. 设置必要的项目目录（images、plans等）
3. 启动后端服务（main.py或travel-planner/backend/app.py）
4. 启动前端服务（如果存在travel-planner/frontend目录）
5. 自动打开浏览器访问应用

## 系统要求

- Python 3.6+
- 必要的Python包：flask, requests, pillow
- 如需运行前端：Node.js v14+, npm v6+

## 常见问题

### 1. 启动失败，提示缺少Python包

按照提示选择"y"安装缺失的包，或手动执行：
```
pip install flask requests pillow
```

### 2. 前端启动失败

确保已安装Node.js，并且在travel-planner/frontend目录下执行过：
```
npm install
```

### 3. 如何停止服务

在启动脚本的命令行窗口中按 `Ctrl+C` 可以停止所有服务。

### 4. 如何配置API密钥

编辑项目根目录下的 `config.json` 文件，添加您的DeepSeek API密钥：
```json
{
    "deepseek_api_key": "您的API密钥"
}
```

## 目录结构

```
project/
├── start_project.py     # 一键启动脚本
├── start_project.bat    # Windows批处理文件
├── start_project.sh     # macOS/Linux Shell脚本
├── main.py              # 主程序入口
├── config.json          # 配置文件
├── images/              # 图片存储目录
├── plans/               # 生成的旅游规划存储目录
└── travel-planner/      # 项目子目录
    ├── backend/         # 后端代码
    └── frontend/        # 前端代码
```

## 注意事项

- 首次启动时，脚本会检查环境并提示安装缺失的依赖
- 如果您的系统中没有安装Node.js，前端将无法启动
- 默认情况下，后端服务运行在5000端口，前端服务运行在3000端口
- 确保这些端口没有被其他应用占用 