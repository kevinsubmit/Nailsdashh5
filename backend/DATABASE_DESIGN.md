# NailsDash 数据库设计文档

## 数据库表结构设计

### 1. users (用户表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 用户ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 邮箱 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| username | VARCHAR(100) | UNIQUE, NOT NULL | 用户名 |
| full_name | VARCHAR(200) | NULL | 全名 |
| avatar_url | VARCHAR(500) | NULL | 头像URL |
| phone | VARCHAR(20) | NULL | 电话号码 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| is_admin | BOOLEAN | DEFAULT FALSE | 是否管理员 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 2. stores (店铺表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 店铺ID |
| name | VARCHAR(200) | NOT NULL | 店铺名称 |
| address | VARCHAR(500) | NOT NULL | 地址 |
| city | VARCHAR(100) | NULL | 城市 |
| state | VARCHAR(50) | NULL | 州 |
| zip_code | VARCHAR(20) | NULL | 邮编 |
| latitude | DECIMAL(10, 8) | NULL | 纬度 |
| longitude | DECIMAL(11, 8) | NULL | 经度 |
| phone | VARCHAR(20) | NULL | 电话 |
| email | VARCHAR(255) | NULL | 邮箱 |
| cover_image | VARCHAR(500) | NULL | 封面图片 |
| description | TEXT | NULL | 描述 |
| rating | DECIMAL(3, 2) | DEFAULT 0.00 | 评分 |
| review_count | INT | DEFAULT 0 | 评论数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否营业 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 3. store_images (店铺图片表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 图片ID |
| store_id | INT | FOREIGN KEY → stores(id) | 店铺ID |
| image_url | VARCHAR(500) | NOT NULL | 图片URL |
| display_order | INT | DEFAULT 0 | 显示顺序 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 4. services (服务项目表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 服务ID |
| store_id | INT | FOREIGN KEY → stores(id) | 店铺ID |
| name | VARCHAR(200) | NOT NULL | 服务名称 |
| description | TEXT | NULL | 服务描述 |
| price | DECIMAL(10, 2) | NOT NULL | 价格 |
| duration_minutes | INT | NOT NULL | 时长（分钟） |
| category | VARCHAR(100) | NULL | 分类 |
| is_available | BOOLEAN | DEFAULT TRUE | 是否可用 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 5. appointments (预约表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 预约ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| store_id | INT | FOREIGN KEY → stores(id) | 店铺ID |
| service_id | INT | FOREIGN KEY → services(id) | 服务ID |
| appointment_date | DATE | NOT NULL | 预约日期 |
| appointment_time | TIME | NOT NULL | 预约时间 |
| status | ENUM | 'pending','confirmed','completed','cancelled' | 预约状态 |
| notes | TEXT | NULL | 备注 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 6. orders (订单表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 订单ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| appointment_id | INT | FOREIGN KEY → appointments(id) | 预约ID |
| order_number | VARCHAR(50) | UNIQUE, NOT NULL | 订单号 |
| total_amount | DECIMAL(10, 2) | NOT NULL | 总金额 |
| discount_amount | DECIMAL(10, 2) | DEFAULT 0.00 | 折扣金额 |
| final_amount | DECIMAL(10, 2) | NOT NULL | 最终金额 |
| payment_status | ENUM | 'pending','paid','refunded' | 支付状态 |
| payment_method | VARCHAR(50) | NULL | 支付方式 |
| paid_at | DATETIME | NULL | 支付时间 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 7. vip_levels (VIP等级配置表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 等级ID |
| level | INT | UNIQUE, NOT NULL | 等级（0-10） |
| name | VARCHAR(100) | NOT NULL | 等级名称 |
| min_spend | DECIMAL(10, 2) | NOT NULL | 最低消费 |
| min_visits | INT | NOT NULL | 最低访问次数 |
| benefit_description | TEXT | NULL | 权益描述 |
| discount_rate | DECIMAL(5, 2) | DEFAULT 0.00 | 折扣率（%） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 8. user_vip_status (用户VIP状态表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| user_id | INT | UNIQUE, FOREIGN KEY → users(id) | 用户ID |
| current_level | INT | DEFAULT 0 | 当前等级 |
| total_spend | DECIMAL(10, 2) | DEFAULT 0.00 | 总消费 |
| total_visits | INT | DEFAULT 0 | 总访问次数 |
| level_updated_at | DATETIME | NULL | 等级更新时间 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 9. points (积分表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| user_id | INT | UNIQUE, FOREIGN KEY → users(id) | 用户ID |
| balance | INT | DEFAULT 0 | 积分余额 |
| total_earned | INT | DEFAULT 0 | 累计获得 |
| total_spent | INT | DEFAULT 0 | 累计消费 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 10. point_transactions (积分交易记录表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 交易ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| amount | INT | NOT NULL | 积分数量（正负） |
| transaction_type | ENUM | 'earn','spend','refund' | 交易类型 |
| description | VARCHAR(500) | NULL | 描述 |
| reference_id | INT | NULL | 关联ID |
| reference_type | VARCHAR(50) | NULL | 关联类型 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 11. coupons (优惠券表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 优惠券ID |
| code | VARCHAR(50) | UNIQUE, NOT NULL | 优惠券代码 |
| name | VARCHAR(200) | NOT NULL | 优惠券名称 |
| description | TEXT | NULL | 描述 |
| discount_type | ENUM | 'percentage','fixed' | 折扣类型 |
| discount_value | DECIMAL(10, 2) | NOT NULL | 折扣值 |
| min_purchase | DECIMAL(10, 2) | DEFAULT 0.00 | 最低消费 |
| max_discount | DECIMAL(10, 2) | NULL | 最大折扣 |
| valid_from | DATETIME | NOT NULL | 有效期开始 |
| valid_until | DATETIME | NOT NULL | 有效期结束 |
| usage_limit | INT | NULL | 使用次数限制 |
| used_count | INT | DEFAULT 0 | 已使用次数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 12. user_coupons (用户优惠券关联表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| coupon_id | INT | FOREIGN KEY → coupons(id) | 优惠券ID |
| status | ENUM | 'available','used','expired' | 状态 |
| used_at | DATETIME | NULL | 使用时间 |
| order_id | INT | NULL, FOREIGN KEY → orders(id) | 订单ID |
| obtained_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 获取时间 |

### 13. gift_cards (礼品卡表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 礼品卡ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| card_number | VARCHAR(50) | UNIQUE, NOT NULL | 卡号 |
| balance | DECIMAL(10, 2) | DEFAULT 0.00 | 余额 |
| initial_amount | DECIMAL(10, 2) | NOT NULL | 初始金额 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| expires_at | DATETIME | NULL | 过期时间 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 14. gift_card_transactions (礼品卡交易记录表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 交易ID |
| gift_card_id | INT | FOREIGN KEY → gift_cards(id) | 礼品卡ID |
| amount | DECIMAL(10, 2) | NOT NULL | 金额（正负） |
| transaction_type | ENUM | 'recharge','use','refund' | 交易类型 |
| description | VARCHAR(500) | NULL | 描述 |
| order_id | INT | NULL, FOREIGN KEY → orders(id) | 订单ID |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 15. deals (优惠活动表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 活动ID |
| title | VARCHAR(200) | NOT NULL | 活动标题 |
| description | TEXT | NULL | 活动描述 |
| discount_amount | DECIMAL(10, 2) | NULL | 折扣金额 |
| discount_percentage | DECIMAL(5, 2) | NULL | 折扣百分比 |
| image_url | VARCHAR(500) | NULL | 活动图片 |
| valid_from | DATETIME | NOT NULL | 有效期开始 |
| valid_until | DATETIME | NOT NULL | 有效期结束 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 16. deal_stores (活动店铺关联表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| deal_id | INT | FOREIGN KEY → deals(id) | 活动ID |
| store_id | INT | FOREIGN KEY → stores(id) | 店铺ID |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 17. pins (Pin内容表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Pin ID |
| user_id | INT | FOREIGN KEY → users(id) | 创建者ID |
| title | VARCHAR(200) | NOT NULL | 标题 |
| description | TEXT | NULL | 描述 |
| image_url | VARCHAR(500) | NOT NULL | 图片URL |
| likes_count | INT | DEFAULT 0 | 点赞数 |
| saves_count | INT | DEFAULT 0 | 保存数 |
| is_public | BOOLEAN | DEFAULT TRUE | 是否公开 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 18. pin_likes (Pin点赞表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| pin_id | INT | FOREIGN KEY → pins(id) | Pin ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| UNIQUE(pin_id, user_id) | | | 唯一约束 |

### 19. pin_saves (Pin保存表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| pin_id | INT | FOREIGN KEY → pins(id) | Pin ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| UNIQUE(pin_id, user_id) | | | 唯一约束 |

### 20. tags (标签表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 标签ID |
| name | VARCHAR(100) | UNIQUE, NOT NULL | 标签名称 |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL友好名称 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 21. pin_tags (Pin标签关联表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| pin_id | INT | FOREIGN KEY → pins(id) | Pin ID |
| tag_id | INT | FOREIGN KEY → tags(id) | 标签ID |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| UNIQUE(pin_id, tag_id) | | | 唯一约束 |

### 22. reviews (评价表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 评价ID |
| user_id | INT | FOREIGN KEY → users(id) | 用户ID |
| store_id | INT | FOREIGN KEY → stores(id) | 店铺ID |
| appointment_id | INT | NULL, FOREIGN KEY → appointments(id) | 预约ID |
| rating | INT | NOT NULL, CHECK(rating BETWEEN 1 AND 5) | 评分 |
| comment | TEXT | NULL | 评论内容 |
| images | JSON | NULL | 图片URL数组 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 23. referrals (推荐记录表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| referrer_id | INT | FOREIGN KEY → users(id) | 推荐人ID |
| referred_id | INT | FOREIGN KEY → users(id) | 被推荐人ID |
| referral_code | VARCHAR(50) | UNIQUE, NOT NULL | 推荐码 |
| status | ENUM | 'pending','completed','rewarded' | 状态 |
| reward_points | INT | DEFAULT 0 | 奖励积分 |
| completed_at | DATETIME | NULL | 完成时间 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

## 索引设计

### 性能优化索引

```sql
-- users表
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- stores表
CREATE INDEX idx_stores_city ON stores(city);
CREATE INDEX idx_stores_rating ON stores(rating);
CREATE INDEX idx_stores_location ON stores(latitude, longitude);

-- appointments表
CREATE INDEX idx_appointments_user_id ON appointments(user_id);
CREATE INDEX idx_appointments_store_id ON appointments(store_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- orders表
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);

-- pins表
CREATE INDEX idx_pins_user_id ON pins(user_id);
CREATE INDEX idx_pins_created_at ON pins(created_at DESC);

-- reviews表
CREATE INDEX idx_reviews_store_id ON reviews(store_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
```

## 数据关系图

```
users (1) ─────── (N) appointments
users (1) ─────── (N) orders
users (1) ─────── (1) user_vip_status
users (1) ─────── (1) points
users (1) ─────── (N) user_coupons
users (1) ─────── (N) gift_cards
users (1) ─────── (N) pins
users (1) ─────── (N) reviews
users (1) ─────── (N) referrals (as referrer)
users (1) ─────── (N) referrals (as referred)

stores (1) ────── (N) store_images
stores (1) ────── (N) services
stores (1) ────── (N) appointments
stores (1) ────── (N) reviews
stores (N) ────── (N) deals (through deal_stores)

services (1) ──── (N) appointments

appointments (1) ─ (1) orders

coupons (N) ───── (N) users (through user_coupons)

pins (N) ──────── (N) users (through pin_likes)
pins (N) ──────── (N) users (through pin_saves)
pins (N) ──────── (N) tags (through pin_tags)
```

## 初始化数据

### VIP等级初始数据

```sql
INSERT INTO vip_levels (level, name, min_spend, min_visits, benefit_description, discount_rate) VALUES
(0, 'Member', 0, 0, 'Member Access', 0.00),
(1, 'Bronze', 35, 1, 'Priority Service (No Waiting)', 0.00),
(2, 'Silver', 2000, 5, 'Free Nail Care Kit', 0.00),
(3, 'Gold', 5000, 15, '5% Discount on Services', 5.00),
(4, 'Platinum', 10000, 30, '10% Discount on Services', 10.00),
(5, 'Diamond', 20000, 50, '15% Discount + Personal Assistant', 15.00),
(6, 'Elite', 35000, 80, '18% Discount + Birthday Gift', 18.00),
(7, 'VIP', 50000, 120, '20% Discount + Exclusive Events', 20.00),
(8, 'SVIP', 80000, 180, '25% Discount + Home Service', 25.00),
(9, 'Royal', 120000, 250, '30% Discount + Quarterly Luxury Gift', 30.00),
(10, 'Black Card', 200000, 350, '40% Discount + Black Card Status', 40.00);
```

### 默认标签数据

```sql
INSERT INTO tags (name, slug) VALUES
('Minimalist', 'minimalist'),
('French', 'french'),
('Y2K', 'y2k'),
('Chrome', 'chrome'),
('Glitter', 'glitter'),
('Acrylic', 'acrylic'),
('Gel', 'gel'),
('Nail Art', 'nail-art');
```

---

**文档作者**: Manus AI  
**创建日期**: 2026-01-01  
**版本**: 1.0
