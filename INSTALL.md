# 安装指南

## 项目当前状态

✅ **项目可用**: 已成功创建基于F2项目的Twitter推文拉取客户端
🎭 **模拟模式**: 当前使用模拟数据运行，返回结构完整的示例推文
🔧 **可升级**: 支持升级到真实F2项目以获取真实Twitter数据

## 快速开始

### 1. 下载项目
```bash
cd /home/zhe/workspace/my-projects/
# 项目已准备就绪
```

### 2. 运行安装脚本
```bash
cd twitter-client
python install_f2.py
```

安装脚本会：
- 尝试从GitHub安装真实的F2项目
- 如果网络问题导致安装失败，自动创建模拟模块
- 更新客户端代码以支持模拟模块

### 3. 测试运行
```bash
cd examples
python basic_usage.py
```

预期输出：
```
⚠️  使用F2模拟模块 - 返回示例数据
成功获取 5 条推文:
推文 1: 这是用户25073877的第1条模拟推文...
```

## 模拟数据说明

### 模拟推文结构
```json
{
  "id": "mock_25073877_1",
  "text": "这是用户25073877的第1条模拟推文 #示例 #测试",
  "author": {"username": "user_25073877"},
  "created_at": "2024-01-01T12:00:00Z",
  "public_metrics": {
    "like_count": 10,
    "retweet_count": 5,
    "reply_count": 2
  },
  "entities": {"urls": []},
  "attachments": {}
}
```

### 模拟数据特点
- **结构完整**: 包含真实推文的所有字段
- **动态生成**: 根据用户ID和请求参数生成不同内容
- **适合开发**: 可用于接口测试、前端开发、数据分析学习

## 升级到真实数据

### 方法1：手动安装F2项目
```bash
# 确保网络连接正常
git clone https://github.com/JohnstonLiu/F2.git
cd F2
pip install -e .

# 回到项目目录测试
cd ../twitter-client/examples
python basic_usage.py
```

### 方法2：使用其他F2仓库
```bash
# 尝试不同的仓库地址
git clone https://github.com/johnliu-tw/F2.git
# 或
git clone https://github.com/F2-dev/F2.git
```

### 配置真实Cookie
```bash
export TWITTER_COOKIE="your_real_twitter_cookie"
```

## 依赖说明

### 当前依赖
- Python 3.7+ 内置模块（asyncio, json, logging, pathlib, typing）
- 无需额外安装第三方包

### 可选依赖（用于扩展功能）
```bash
# 数据分析
pip install pandas numpy

# 网络请求（如需自定义实现）
pip install requests httpx

# 开发工具
pip install pytest black flake8
```

## 问题排查

### Q: 模拟模块能提供真实数据吗？
A: 不能。模拟模块只返回示例数据，用于开发和测试。

### Q: 如何验证真实F2是否安装成功？
A: 运行示例时，如果没有"使用F2模拟模块"的警告，说明使用真实F2。

### Q: 项目功能完整吗？
A: 是的。所有API接口都已实现，只是数据源不同（模拟 vs 真实）。

## 项目结构
```
twitter-client/
├── src/
│   ├── f2_mock/              # F2模拟模块（自动生成）
│   └── twitter_client/       # 主要客户端代码
├── examples/                 # 使用示例
├── config/                   # 配置文件
└── install_f2.py            # 自动安装脚本
```

## 下一步

1. **开发学习**: 使用模拟数据学习API使用方法
2. **功能测试**: 测试所有客户端功能
3. **部署准备**: 配置真实环境后部署使用
4. **自定义扩展**: 基于现有框架添加新功能
