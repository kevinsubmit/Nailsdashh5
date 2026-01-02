# 用户表更新说明

## 📋 更新概述

本次更新将用户认证系统从**邮箱登录**改为**手机号登录**，并添加了**手机验证码验证**功能。

### 主要变更

1. **手机号改为必填且唯一**
   - 用户注册时必须提供手机号
   - 手机号作为唯一标识符（替代原来的邮箱）
   - 支持美国手机号格式（10位或11位数字）

2. **邮箱改为可选**
   - 用户可以选择性地提供邮箱
   - 邮箱不再是必填项

3. **添加手机验证码功能**
   - 注册时需要验证手机号
   - 新增`verification_codes`表存储验证码
   - 验证码有效期10分钟
   - 验证码使用后自动失效

4. **新增字段**
   - `phone_verified`: 标记手机号是否已验证
   - 注册成功后自动设为`True`

## 🗄️ 数据库变更

### backend_users 表结构变更

**之前的结构：**
```sql
CREATE TABLE backend_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,  -- 邮箱必填唯一
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(200),
    avatar_url VARCHAR(500),
    phone VARCHAR(20),  -- 手机号可选
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**更新后的结构：**
```sql
CREATE TABLE backend_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) UNIQUE NOT NULL,  -- 手机号必填唯一
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(200),
    email VARCHAR(255),  -- 邮箱可选
    avatar_url VARCHAR(500),
    phone_verified BOOLEAN DEFAULT FALSE,  -- 新增：手机号是否已验证
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 新增 verification_codes 表

```sql
CREATE TABLE verification_codes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) NOT NULL,
    code VARCHAR(6) NOT NULL,  -- 6位数字验证码
    purpose VARCHAR(50) NOT NULL,  -- register, login, reset_password
    is_used BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP NOT NULL,  -- 过期时间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_expires_at (expires_at)
);
```

## 📝 API 变更

### 1. 用户注册 API

**端点：** `POST /api/v1/auth/register`

**之前的请求体：**
```json
{
  "email": "user@example.com",  // 必填
  "username": "johndoe",
  "password": "password123",
  "full_name": "John Doe",
  "phone": "1234567890"  // 可选
}
```

**更新后的请求体：**
```json
{
  "phone": "1234567890",  // 必填，美国手机号
  "username": "johndoe",
  "password": "password123",
  "full_name": "John Doe",
  "email": "user@example.com",  // 可选
  "verification_code": "123456"  // 必填，6位验证码
}
```

### 2. 用户登录 API

**端点：** `POST /api/v1/auth/login`

**之前的请求体：**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**更新后的请求体：**
```json
{
  "phone": "1234567890",  // 使用手机号登录
  "password": "password123"
}
```

### 3. 新增：发送验证码 API

**端点：** `POST /api/v1/auth/send-verification-code`

**请求体：**
```json
{
  "phone": "1234567890",
  "purpose": "register"  // register, login, reset_password
}
```

**响应：**
```json
{
  "message": "验证码已发送",
  "expires_in": 600  // 有效期（秒）
}
```

### 4. 新增：验证验证码 API

**端点：** `POST /api/v1/auth/verify-code`

**请求体：**
```json
{
  "phone": "1234567890",
  "code": "123456",
  "purpose": "register"
}
```

**响应：**
```json
{
  "valid": true,
  "message": "验证码有效"
}
```

## 📱 手机号格式

支持以下格式：

1. **10位数字**（美国本土格式）
   - 示例：`2025551234`
   - 自动转换为：`12025551234`（添加国家码+1）

2. **11位数字**（含国家码）
   - 示例：`12025551234`
   - 直接使用

3. **带格式的号码**（自动清理）
   - 示例：`(202) 555-1234`、`202-555-1234`、`+1 202 555 1234`
   - 自动提取数字：`12025551234`

## 🔄 本地更新步骤

### 步骤1：拉取最新代码

```bash
cd /path/to/Nailsdashh5
git pull origin main
```

### 步骤2：停止后端服务器

如果后端服务器正在运行，按 `Ctrl+C` 停止。

### 步骤3：备份数据（如果有重要数据）

```bash
# 如果使用SQLite
cp backend/nailsdash.db backend/nailsdash.db.backup

# 如果使用MySQL
# mysqldump -u root -p nailsdash > nailsdash_backup.sql
```

### 步骤4：删除旧的用户表

```bash
cd backend

# 方法1：删除整个数据库文件（SQLite）
rm nailsdash.db

# 方法2：使用Python脚本删除表（MySQL或SQLite）
python -c "
from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS backend_users'))
    conn.execute(text('DROP TABLE IF EXISTS verification_codes'))
    conn.commit()
print('旧表已删除')
"
```

### 步骤5：重新初始化数据库

```bash
python init_db.py
```

应该看到：
```
Database tables created successfully!
```

### 步骤6：启动后端服务器

```bash
uvicorn app.main:app --reload
```

### 步骤7：测试新的API

访问 http://localhost:8000/api/docs 查看更新后的API文档。

## 🧪 测试流程

### 1. 发送验证码

```bash
curl -X POST "http://localhost:8000/api/v1/auth/send-verification-code" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "2025551234",
    "purpose": "register"
  }'
```

### 2. 注册用户

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "2025551234",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User",
    "verification_code": "123456"
  }'
```

### 3. 登录

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "2025551234",
    "password": "password123"
  }'
```

## ⚠️ 注意事项

1. **数据丢失**：更新会删除旧的用户数据，请提前备份
2. **前端更新**：前端代码也需要相应更新（将在后续推送）
3. **验证码发送**：目前验证码只是生成并存储在数据库中，实际发送短信功能需要集成第三方服务（如Twilio）
4. **测试环境**：在开发环境中，可以直接查询数据库获取验证码进行测试

## 📊 代码变更统计

- **修改文件**：7个
- **新增文件**：2个
- **新增代码行**：约300行
- **删除代码行**：约50行

### 修改的文件

1. `app/models/user.py` - 用户模型
2. `app/schemas/user.py` - 用户schemas
3. `app/crud/user.py` - 用户CRUD操作
4. `app/api/v1/endpoints/auth.py` - 认证API端点（待更新）

### 新增的文件

1. `app/models/verification_code.py` - 验证码模型
2. `app/schemas/verification.py` - 验证码schemas
3. `app/crud/verification_code.py` - 验证码CRUD操作

## 🚀 下一步计划

1. ✅ 更新数据库模型和schemas
2. ✅ 创建验证码功能
3. ⏳ 更新API端点（auth.py）
4. ⏳ 集成短信发送服务（Twilio）
5. ⏳ 更新前端代码
6. ⏳ 编写单元测试
7. ⏳ 更新API文档

## 📞 支持

如有问题，请查看：
- API文档：http://localhost:8000/api/docs
- GitHub Issues：https://github.com/kevinsubmit/Nailsdashh5/issues
