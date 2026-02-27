# ihui_public 项目数据库使用情况分析

## 📊 数据库配置概览

### 数据库连接信息

**主数据库（ihui_public）**
- 数据库类型：MySQL
- 连接方式：SQLAlchemy ORM
- 连接池：QueuePool
- 默认连接字符串：`mysql+pymysql://root:password@localhost:3306/ihui_public?charset=utf8mb4`

**中心库（zhs_center_project）**
- 用于访问特定表（users、user_margin、user_auth_info）
- 通过 DATASOURCE_2_TABLES 配置识别

---

## 📋 涉及的数据表

### 1. 用户相关表（中心库）

#### users 表
- **用途**：存储用户基本信息
- **数据源**：datasource_2（中心库）
- **关键字段**：
  - user_uuid：用户唯一标识
  - username：用户名
  - email：邮箱
  - created_at：创建时间

#### user_margin 表
- **用途**：存储用户余额/Token信息
- **数据源**：datasource_2（中心库）
- **关键字段**：
  - user_uuid：用户唯一标识
  - balance：余额
  - tokens：Token数量
  - updated_at：更新时间

#### user_auth_info 表
- **用途**：存储用户认证信息
- **数据源**：datasource_2（中心库）
- **关键字段**：
  - user_uuid：用户唯一标识
  - auth_token：认证令牌
  - expires_at：过期时间

### 2. 对话记录表（主数据库）

#### zhs_conversation_history 表
- **用途**：存储AI对话历史记录
- **数据源**：datasource_1（ihui_public库）
- **关键字段**：
  - id：主键
  - user_uuid：用户唯一标识
  - model_name：使用的模型名称
  - problem：用户问题
  - answer：模型回答
  - chat_id：聊天会话ID
  - agent_id：智能体ID
  - summary：思考过程
  - field1：自定义字段1（存储Token消耗等）
  - agent_url：文件URL（图片、视频等）
  - created_at：创建时间

---

## 🔧 数据库配置参数

### 连接池配置
```python
POOL_SIZE = 10              # 连接池大小
MAX_OVERFLOW = 20            # 最大溢出连接数
POOL_TIMEOUT = 30            # 连接超时时间（秒）
POOL_RECYCLE = 3600          # 连接回收时间（秒）
```

### 连接参数
```python
{
    "charset": "utf8mb4",          # 字符集
    "connect_timeout": 10,          # 连接超时
    "read_timeout": 30,             # 读取超时
    "write_timeout": 30,            # 写入超时
    "autocommit": False            # 自动提交
}
```

---

## 📝 数据库操作

### 1. Token验证和扣减

**函数**：`check_user_token_sufficient()`
- **用途**：验证用户Token余额是否充足
- **当前状态**：简化处理，返回固定结果
- **未来实现**：需要查询 user_margin 表验证余额

**函数**：`calculate_and_deduct_tokens_by_cost()`
- **用途**：根据费用计算并扣减Token
- **当前状态**：简化处理，不实际扣减
- **未来实现**：需要更新 user_margin 表余额

### 2. 对话记录保存

**函数**：`save_conversation_to_db()`
- **用途**：保存AI对话历史
- **当前状态**：已实现数据库插入
- **表名**：zhs_conversation_history
- **字段**：user_uuid, model_name, problem, answer, chat_id, agent_id, summary, field1, agent_url, created_at

---

## 🎯 数据库使用场景

### 1. 用户认证
- 查询 users 表验证用户身份
- 查询 user_auth_info 表验证Token

### 2. Token管理
- 查询 user_margin 表获取余额
- 更新 user_margin 表扣减Token

### 3. 对话记录
- 插入 zhs_conversation_history 表保存对话
- 支持多种模型（豆包、通义千问、智谱、DeepSeek等）

### 4. 多数据源支持
- 主数据库（ihui_public）：存储对话历史
- 中心库（zhs_center_project）：存储用户信息
- 自动根据表名选择数据源

---

## ⚠️ 注意事项

### 1. 当前简化处理

**Token验证和扣减**
- `check_user_token_sufficient()`：返回固定结果，未实际查询数据库
- `deduct_user_tokens()`：返回固定结果，未实际扣减

**原因**：简化项目复杂度，便于快速启动

**未来改进**：
- 实现真实的数据库查询和更新
- 添加事务处理
- 添加余额不足异常处理

### 2. 数据库配置

**需要配置的参数**（在 config.py 中）：
- `DATABASE_URL`：数据库连接字符串
- `DATABASE_ECHO`：是否打印SQL语句（开发环境建议True）
- `TOKEN_BASE_MULTIPLIER`：Token基础倍率

### 3. 表结构要求

**必需的表**：
1. users（中心库）
2. user_margin（中心库）
3. user_auth_info（中心库）
4. zhs_conversation_history（主库）

---

## 🚀 数据库初始化建议

### 1. 创建数据库

```sql
-- 创建主数据库
CREATE DATABASE IF NOT EXISTS ihui_public 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 创建中心库（如果不存在）
CREATE DATABASE IF NOT EXISTS zhs_center_project 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 2. 创建表结构

```sql
-- 用户表（中心库）
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(64) UNIQUE NOT NULL,
    username VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户余额表（中心库）
CREATE TABLE IF NOT EXISTS user_margin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(64) UNIQUE NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0,
    tokens INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 用户认证表（中心库）
CREATE TABLE IF NOT EXISTS user_auth_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(64) NOT NULL,
    auth_token VARCHAR(255),
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 对话历史表（主库）
CREATE TABLE IF NOT EXISTS zhs_conversation_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(64) NOT NULL,
    model_name VARCHAR(50),
    problem TEXT,
    answer TEXT,
    chat_id VARCHAR(64),
    agent_id VARCHAR(64),
    summary TEXT,
    field1 VARCHAR(255),
    agent_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_uuid (user_uuid),
    INDEX idx_chat_id (chat_id),
    INDEX idx_created_at (created_at)
);
```

### 3. 配置数据库连接

编辑 `config.py`，设置正确的数据库连接信息：
```python
DATABASE_URL = "mysql+pymysql://username:password@host:port/database?charset=utf8mb4"
```

---

## 📊 总结

### 数据库数量
- **主数据库**：1个（ihui_public）
- **中心库**：1个（zhs_center_project）

### 数据表数量
- **用户相关表**：3个（users, user_margin, user_auth_info）
- **对话记录表**：1个（zhs_conversation_history）

### 数据库功能
- ✅ 多数据源支持
- ✅ 连接池管理
- ✅ 智能表路由
- ✅ Token验证（简化版）
- ✅ 对话记录保存

---

**📝 数据库使用情况分析完成！**
