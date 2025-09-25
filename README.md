### 列出所有screen会话
screen -ls

### 如果存在，关闭现有会话
screen -X -S gbx_full quit
screen -X -S gbx_server quit

### 填写.env 
实例填在.env.example
obs接口可以忽略。最新版代码都通过stock服务器接收db内容。 

主界面存在于/root/GBX_dashboard/src/views

界面中的子界面存在于/root/GBX_dashboard/src/components_vertical

### 运行
先开server, 再开前端

npm run start_server

npm run start
