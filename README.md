# django

#### 介绍
    ● 该网站是一个个人博客网站，具有主页以及一个独立的app功能，项目环境为Manjaro KDE Linux系统。
    ● 前端页面基本使用Bootstrap+layui以及Font Awesome+jQuery等框架。采用响应式布局，为了适配绝大多数浏览器，有做浏览器适配，以及动态效果，考虑用户的使用感受，在网页中很多地方使用了jQuery的ajax功能，来对页面进行局部操作。
    ● 考虑用户需求，我搭建了完整的用户功能：用户登录、用户注册、用户活跃验证、密码找回，用户登录轨迹。考虑用户数据的安全性，数据库采用MySQL8.0用户表中密码采用hash算法加密保存。为了让用户直观的看到自己账户的信息，在个人中心中展示用户的登录信息，以及上次登录信息；用户的行为：博客发文，用户收藏等功能。
    ● 主要APP功能：博客功能，在博客app中，我将Markdown编辑器的功能集成到前端页面中。在用户登录的情况下方可进行博客撰写，同时，博客撰写支持Markdown的所有语法，并且支持前端显示代码高亮等操作。在博客管理中，我定义了搜索功能，可以根据用户名、博客标题、博客内容进行博客查找。
    ● 后台管理系统：后台管理系统采用Simpleui搭建，可以进行对有所对象的增、删、改、查等功能。
    ● 搜索功能：采用了Elasticsearch搜索方案，建立elasticsearch索引进行查询，减小数据库负担。
    ● 采用Redis缓存。设置60S缓存，以缓解高并发带来的服务器负担。

#### 效果展示
![主页](https://images.gitee.com/uploads/images/2021/0512/141620_f3aae8fb_5696074.png "index.png")
![后台管理主页](https://images.gitee.com/uploads/images/2021/0512/142310_fedbc36d_5696074.png "屏幕截图.png")
![博客撰写](https://images.gitee.com/uploads/images/2021/0512/142349_c2102c22_5696074.png "屏幕截图.png")
![博客主页](https://images.gitee.com/uploads/images/2021/0512/142617_1436ffa2_5696074.png "屏幕截图.png")
![文章页](https://images.gitee.com/uploads/images/2021/0512/142852_c4e518db_5696074.png "屏幕截图.png")



#### 项目结构
~~~bash

├── apps
│   ├── blog
│   ├── index
│   ├── search
│   └── user
├── build               环境镜像构建
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── elastic             elasticsearch 文件路径
│   └── data            elasticsearch 数据持久化文件
├── manage.py
├── mysite            
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mysql             mysql 文件路径
│   ├── data          mysql 数据持久化文件
│   └── Dockerfile    mysql 镜像构建
├── README.md
├── redis             redis 文件路径
│   └── data          redis 数据持久化文件
├── requirements.txt  项目依赖
├── static            静态文件
└── templates         模板文件

# 若需要部署使用全部功能需自行配置stmp邮箱相关服务，在不改动mysql和Redis以及ElasticSearch配置的情况下，可直接使用docker-compose up -d 进行启动且无需进行数据库迁移
~~~


#### 常规开发环境搭建
~~~bash
 git clone https://gitee.com/hou_cc/django.git
 
 mkdir vene && cd vene && virtulaenv . && .\scripts\activate
 
 pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
 
 python manage.py makemigrations
 
 python manage.py migrate
 
 python manage.py runserver
~~~


### 一键部署环境
> 使用Docker 进行环境搭建，需提前在电脑中安装docker（Docker for Windows）

- **step 1**
> git clone https://github.com/1347027216/django3-blog.git

- **step 2**(默认已经对Docker环境、镜像Hub进行配置否则请自行百度)

~~~bash
# Docker 环境搭建 (django3-blog文件夹)
docker build -t blog:v1 ./build
~~~

- **step 3启动服务（若使用Docker构建服务环境则无需修改项目中Mysql、redis、Elasticsearch服务地址）**
~~~bash
docker-compose up -d

# 可能会需要手动migrate数据库则依次执行
docker exec -it blog_service /bin/bash
python manage.py makemigrations
python manage.py migrate

# 若出现：django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on '172.21.0.2' (115)"，此异常原因为mysql服务未启动完成，则需要等待mysql服务启动完成后重启blog_service服务
docker restart blog_service
 ~~~


#### Docker 常用命令

~~~bash
# 查看所有容器
docker ps -a

# 查看所有镜像
docker images

# 删除所有容器
docker rm $(docker ps -aq)

# 删除所有镜像
docker rmi $(docker images -q)

# 进入容器
docker exec -it 容器id或容器名称 /bin/bash
ex: docker exec -it blog_service /bin/bash

# docker-compose 查看所有容器ip
docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq)

# docker-compose 查看容器日志
docker-compose logs -f 容器名称
ex: docker-compose logs -f blog_service

# docker-compose 后台启动容器
docker-compose up -d

# docker-compose 停止容器
docker-compose stop

# docker-compose 重启容器
docker-compose restart
~~~