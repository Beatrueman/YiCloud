# YiCloud-Save Everything

一个简易的个人网盘系统

**技术栈**：

前端：HTML + CSS + JavaScript

后端：Python Flask

数据库：MySQL

**持续开发......**

## 页面展示

![image-20240213223544046](https://gitee.com/beatrueman/images/raw/master/img/202402132235196.png)

![image-20240213223525005](https://gitee.com/beatrueman/images/raw/master/img/202402132235140.png)

## 功能介绍

### 注册与登录

可完成基本的注册与登录功能。

当密码不正确时会出现提示：”用户名或密码错误，请重试！“

![image-20240213222738338](https://gitee.com/beatrueman/images/raw/master/img/202402132227510.png)

注册时会提示密码规范，不符合规范的密码无法进行注册。

![image-20240213222929577](https://gitee.com/beatrueman/images/raw/master/img/202402132229882.png)

![image-20240213222956448](https://gitee.com/beatrueman/images/raw/master/img/202402132229562.png)

### 登出

点击红色按钮：`退出登录`即可登出当前用户。

### 文件上传

用户登录后，点击蓝色按钮：`上传文件`即可选择本地文件进行上传。

上传成功与否都会出现弹窗反馈。

### 文件下载

用户成功上传的文件都会生成一个超链接，只需点击超链接即可下载对应文件。

### 文件删除

用户可点击每个文件后的红色删除按钮，即可删除对应文件。

### 文件分页

每个页面固定展示7个文件，用户可点击右下角的分页按钮选择对应文件所在页面。

## 如何安装？

### 本机部署

```
chmod +x install.sh
./install.sh # 按要求填写数据库相关信息即可
```

### Docker-Compose部署

首先需要安装好docker和docker-compose

```
docker-compose up -d
```

相关设置可在`docker-comppose.yml`中修改

```
version: '3'

services:
  db:
    image: mysql 
    environment: 
      MYSQL_ROOT_PASSWORD: YiCloud*123456
      MYSQL_DATABASE: cloud
      MYSQL_USER: cloud
      MYSQL_PASSWORD: YiCloud*123456
    volumes:
      - /root/data:/var/lib/mysql # 持久化mysql数据目录
      - /root/init:/docker-entrypoint-initdb.d/ # 挂载init目录，需要包含init.sql保证数据库初始化
  web:
    image: beatrueman/yicloud:v1 
    volumes:
      - /root/cloud/data:/YiCloud/data # 持久化data目录（保存了每个用户的文件夹）
    ports:
      - "6666:6666"
    depends_on:
      - db
    environment: # 以下设置不要更改，否则数据库会出问题
      - HOST=db:3306 
      - USER=cloud 
      - PASSWORD=YiCloud*123456 
      - DATABASE=cloud

```

## 目录文件夹介绍

```
tree .
.
├── config.py # 数据库配置信息
├── data # 每个用户的文件夹
├── database # 用于建表
│   └── cloud_user.sql
├── database_init.py # 数据库初始化（用于检查表，执行建表语句）
├── docker-compose.yml # docker-compose部署
├── Dockerfile # 打包镜像
├── init.sql # 数据库初始化（用于创建用户，database等）
├── install.sh # 本机部署安装脚本
├── main.py # 项目主文件
├── main.sh # 脚本执行启动项目（先数据库初始化再启动本项目）
├── README.md
├── requirements.txt # 依赖文件
├── routes # 路由
│   ├── dashboard.py # 主功能路哟
│   ├── index.py # 注册登录路由
│   ├── __init__.py
├── static # 静态文件
│   ├── 1.jpg # 图标文件
│   ├── 1.svg
│   ├── 2.png
│   ├── blog.png
│   ├── css # 样式文件
│   │   └── index.css
│   ├── disk.png
│   └── github.png
└── templates # 模板
    ├── dashboard.html # 主页面
    ├── index.html # 登录页面
    └── regist.html # 注册页面

9 directories, 32 files


```

## 安全防范

### 密码规范

采用正则匹配，对用户密码进行规范，避免弱口令。

![image-20240213225723349](https://gitee.com/beatrueman/images/raw/master/img/202402132257400.png)

用户注册后的密码会经过`bcrypt`加密后存入数据库，即使被撞库也无法得知真实密码。

![image-20240213225938131](https://gitee.com/beatrueman/images/raw/master/img/202402132259162.png)

### SQL注入防范

使用`flask_sqlalchemy`进行参数化查询而不是字符串插值。参数化查询会将用户输入视为参数，而不是 SQL 代码的一部分，从而防止攻击者注入恶意代码。

![image-20240213230412984](https://gitee.com/beatrueman/images/raw/master/img/202402132304036.png)

此处`.filter_by(username=username)`将username视为参数而不是直接拼接到SQL查询语句中。
