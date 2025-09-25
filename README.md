## GBX Dashboard

一个基于 Vue 3 + Vite 的可视化看板，集成了实时数据（Socket.IO）、数据库浏览接口（Express + MySQL）、以及可选的华为云 OBS 文件读取能力。前端使用 Element Plus 与 ECharts 进行展示，地图相关能力基于百度地图。

### 功能特性
- 实时数据展示（Socket.IO 客户端）
- 数据库浏览页面（查看表、结构、分页数据）
- 图表与卡片式指标展示（Element Plus + ECharts）
- 可选的 OBS 对象存储读取（CSV 等）
- 地图场景（百度地图 API）


## 开发环境准备

### 1) 安装依赖
```bash
npm install
```

### 2) 配置环境变量
请新建 `.env` 文件（不要提交到 Git），可参考仓库中的 `.env.example`：
```bash
# 服务器端口
PORT=3000

# 数据库配置（后端）
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=gbx
DB_CHARSET=utf8

# 前端环境变量（以 VITE_ 开头）
VITE_BAIDU_MAP_AK=your_baidu_map_api_key
# 可选：OBS 访问配置（如不使用 OBS，可不配置）
VITE_OBS_ACCESS_KEY_ID=your_obs_access_key
VITE_OBS_SECRET_ACCESS_KEY=your_obs_secret_key
```


## 启动与调试

项目分为后端 API 与前端两部分，需先启动后端再启动前端：

```bash
# 关闭指定会话（示例）
screen -X -S gbx_full quit
screen -X -S gbx_server quit
```
---

# 1) 启动后端（Express + Socket.IO + MySQL）
npm run start_server

# 2) 启动前端（Vite 开发服务器）
npm run start
```

启动后：
- 前端开发服务器默认运行在 `http://localhost:5173`
- 后端默认监听 `http://localhost:3000`
- Vite 代理将把 `/api` 转发到后端；地图相关的 `/mapv` 会转发到 `https://mapv.baidu.com`



## 目录结构
```text
GBX_dashboard/
  ├─ public/                # 开发时直接可访问的静态资源（/ 路径）
  ├─ src/
  │  ├─ api/                # 前端 API 封装（数据库、OBS、socket 客户端等）
  │  ├─ components_vertical/# 大屏组件
  │  ├─ views/              # 页面视图（主界面入口在此）
  │  ├─ assets/             # 本地静态资源
  │  └─ main.js             # 前端入口
  ├─ server/                # 后端（Express + Socket.IO + MySQL）
  ├─ vite.config.js         # Vite 配置（含代理与插件）
  ├─ vercel.json            # Vercel 部署配置（outputDirectory: dist）
  ├─ .env.example           # 环境变量模板（不要包含真实密钥）
  └─ README.md
```

关键文件：
- `src/api/database.js`：前端通过 `/api` 访问后端数据库接口
- `server/api_db.js`：后端 Express 路由，提供 `/api/test`, `/api/tables`, `/api/tables/:tableName/structure`, `/api/tables/:tableName`
- `src/api/socket.js`：Socket.IO 客户端（默认连接 `http://110.41.178.82:3000`，可按需改为环境变量）
- `src/api/obs_chart.js`：OBS 读取（可选）



## 部署说明
- 前端打包：`npm run build`，产物在 `dist/`
- Vercel：已配置 `vercel.json`，`outputDirectory: dist`
- 静态资源：开发时放 `public/`，构建后会拷贝到 `dist/`
- 后端部署：将 `server/` 作为 Node 服务部署（需 `.env` 中数据库与端口配置）

## 其他
tools为svg map路径匹配代码，可忽略。

## 版权与许可
本项目仅用于内部演示和研究用途。
