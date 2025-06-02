# 在线投票应用

这是一个基于Flask的在线投票Web应用的python实训项目，允许用户创建、分享和参与投票。

## 功能特点

- 用户注册和登录系统
- 创建自定义投票
- 生成唯一分享链接
- 实时查看投票结果
- 防止重复投票机制

## 技术栈

- 后端：Python Flask
- 前端：Bootstrap 5、HTML5、CSS3、JavaScript
- 数据库：MySQL

## 安装与运行

1. 克隆仓库
   ```
   git clone https://github.com/neptune-yako/python_flask_voting.git
   cd python_flask_voting
   ```

2. 创建并激活虚拟环境
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖
   ```
   pip install -r requirements.txt
   ```

4. 配置环境变量
   创建 `.env` 文件，包含以下内容：
   ```
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=mysql://username:password@localhost/voting_app
   ```
   注意：用你自己的数据库凭据替换上述内容

5. 创建MySQL数据库
   ```
   # 登录MySQL
   mysql -u root -p
   
   # 在MySQL中创建数据库
   CREATE DATABASE voting_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. 初始化数据库
   ```
   # 初始化迁移仓库
   flask db init
   
   # 创建迁移脚本
   flask db migrate -m "初始化数据库"
   
   # 应用迁移
   flask db upgrade
   ```

7. 运行应用
   ```
   # 方法1
   flask run
   
   # 方法2
   python run.py
   ```

8. 访问应用
   打开浏览器，访问 http://127.0.0.1:5000

## 项目结构

```
/
├── app/                    # 应用主目录
│   ├── __init__.py         # 应用初始化
│   ├── models.py           # 数据模型
│   ├── auth/               # 认证相关模块
│   ├── main/               # 主页相关模块
│   ├── polls/              # 投票相关模块
│   ├── static/             # 静态文件
│   └── templates/          # HTML模板
├── migrations/             # 数据库迁移文件
├── .env                    # 环境变量（需自行创建）
├── .flaskenv               # Flask环境配置
├── config.py               # 配置文件
├── requirements.txt        # 项目依赖
└── run.py                  # 应用入口
```
