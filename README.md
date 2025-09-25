### 列出所有screen会话
screen -ls

### 如果存在，关闭现有会话
screen -X -S gbx_full quit
screen -X -S gbx_server quit

### 运行
先跑开server

npm run start_server

再跑开前端

npm run start
