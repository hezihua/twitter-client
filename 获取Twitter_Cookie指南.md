# 🍪 获取Twitter Cookie详细指南

## 🎯 目标
获取Twitter Cookie以便使用真实F2项目拉取真实推文数据

## 📋 步骤详解

### 1️⃣ 登录Twitter
- 打开浏览器（推荐Chrome/Edge）
- 访问 https://x.com 
- 使用您的Twitter账号登录

### 2️⃣ 打开开发者工具
- 按 `F12` 键打开开发者工具
- 或者右键页面 → 选择"检查"或"Inspect"

### 3️⃣ 获取Cookie（方法A：Network标签）
1. 点击 **Network**（网络）标签
2. 刷新页面（按F5）
3. 在请求列表中选择任意一个请求（建议选择第一个）
4. 在右侧面板找到 **Request Headers**（请求头）
5. 找到 **Cookie** 字段
6. 复制整个Cookie值（很长的一串）

### 4️⃣ 获取Cookie（方法B：Application标签）
1. 点击 **Application**（应用程序）标签
2. 左侧展开 **Cookies** 
3. 点击 **https://x.com**
4. 复制所有Cookie值，格式：`name1=value1; name2=value2; ...`

## 🔍 Cookie示例格式
```
auth_token=xxxxx; ct0=xxxxx; _ga=xxxxx; _gid=xxxxx; guest_id=xxxxx; ...
```

## ⚙️ 设置Cookie环境变量

### Linux/Mac/WSL：
```bash
export TWITTER_COOKIE='你复制的Cookie完整内容'
```

### Windows CMD：
```cmd
set TWITTER_COOKIE=你复制的Cookie完整内容
```

### Windows PowerShell：
```powershell
$env:TWITTER_COOKIE='你复制的Cookie完整内容'
```

## ✅ 验证Cookie设置
```bash
cd /home/zhe/workspace/my-projects/twitter-client
python test_real_f2.py
```

## 🔑 重要Cookie字段
确保Cookie中包含这些关键字段：
- `auth_token=` - 认证令牌
- `ct0=` - CSRF令牌 
- `guest_id=` - 访客ID

## ⚠️ 注意事项
1. **安全性**：不要分享Cookie给他人
2. **有效期**：Cookie会过期，需要定期更新
3. **隐私**：仅在可信环境中使用
4. **合规性**：遵守Twitter使用条款

## 🚀 测试成功后
设置完Cookie后运行：
```bash
# 测试配置
python test_real_f2.py

# 获取真实推文
python examples/simple_usage.py
```

## 🛠️ 故障排除
- 如果Cookie无效：重新获取最新Cookie
- 如果请求失败：检查网络连接
- 如果格式错误：确保复制完整的Cookie字符串
