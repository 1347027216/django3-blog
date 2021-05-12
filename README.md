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

    
    


#### 安装教程

    1.  git clone https://gitee.com/hou_cc/django.git
    2.  安装虚拟环境 安装依赖【需删除掉项目所带venv文件夹，重新创建虚拟环境】
    3.  运行项目
