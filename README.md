# Twitter推文拉取客户端

基于F2项目的Twitter API封装，提供简单易用的推文拉取接口。

## 特性

- 🚀 异步推文拉取，支持批量和流式获取
- 🔧 灵活的配置管理，支持环境变量和配置文件
- 📊 内置数据分析和格式化功能  
- 🛡️ 完善的错误处理和日志记录
- 🎯 简洁的API设计，易于集成
- 📦 基于成熟的F2项目，稳定可靠

## 安装

### 快速安装（推荐）

```bash
git clone <repository-url>
cd twitter-client

# 运行安装脚本（会自动处理F2依赖问题）
python install_f2.py

# 安装其他依赖（可选，目前项目只使用Python内置模块）
# pip install -r requirements.txt
```

### 当前状态

🎭 **使用模拟模块**: 由于F2项目需要特定的网络环境，当前项目使用模拟模块运行，返回结构完整的示例数据。

✅ **功能完整**: 所有API接口都已实现，可用于开发、测试和学习。

🔧 **升级到真实数据**: 如需获取真实Twitter数据，请手动安装F2项目：
```bash
git clone https://github.com/JohnstonLiu/F2.git
cd F2 && pip install -e .
```

## 快速开始

### 1. 环境配置

首先设置Twitter Cookie环境变量：

```bash
export TWITTER_COOKIE="your_twitter_cookie_here"
```

或者创建配置文件 `config/config.json`：

```json
{
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.x.com/"
  },
  "proxies": {
    "http://": null,
    "https://": null
  },
  "cookie": "your_twitter_cookie_here",
  "timeout": 30
}
```

### 2. 基本使用

```python
import asyncio
from twitter_client import TwitterClient, ConfigManager

async def main():
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 创建客户端
    client = TwitterClient(config_manager.get_request_config())
    
    # 获取用户推文
    user_id = "25073877"  # 替换为目标用户ID
    tweets = await client.fetch_user_tweets(
        user_id=user_id,
        max_tweets=10
    )
    
    # 处理推文数据
    for tweet in tweets:
        formatted = client.format_tweet(tweet)
        print(f"推文内容: {formatted['text'][:100]}...")
        print(f"点赞数: {formatted.get('public_metrics', {}).get('like_count', 0)}")
        print("-" * 50)
    
    await client.close()

asyncio.run(main())
```

### 3. 流式获取

```python
import asyncio
from twitter_client import TwitterClient, ConfigManager

async def stream_example():
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    # 流式获取推文
    async for tweet in client.fetch_user_tweets_stream(
        user_id="25073877",
        max_tweets=50
    ):
        formatted = client.format_tweet(tweet)
        print(f"实时推文: {formatted['text'][:80]}...")
    
    await client.close()

asyncio.run(stream_example())
```

## API文档

### TwitterClient

主要的推文拉取客户端类。

#### 初始化

```python
client = TwitterClient(config: Dict[str, Any])
```

**参数:**
- `config`: 配置字典，包含headers、cookie、proxies等信息

#### 方法

##### `fetch_user_tweets(user_id, max_tweets=20, page_size=20, max_cursor="")`

获取指定用户的推文列表。

**参数:**
- `user_id` (str): 用户ID
- `max_tweets` (int): 最大获取推文数量
- `page_size` (int): 每页获取的推文数量
- `max_cursor` (str): 分页游标

**返回:** `List[Dict[str, Any]]` - 推文列表

##### `fetch_user_tweets_stream(user_id, max_tweets=100, page_size=20, max_cursor="")`

流式获取用户推文。

**参数:** 同上

**返回:** `AsyncGenerator[Dict[str, Any], None]` - 推文生成器

##### `format_tweet(tweet_data)`

格式化推文数据。

**参数:**
- `tweet_data` (Dict): 原始推文数据

**返回:** `Dict[str, Any]` - 格式化后的推文数据

### ConfigManager

配置管理器类。

#### 初始化

```python
config_manager = ConfigManager(config_path=None)
```

**参数:**
- `config_path` (str, optional): 配置文件路径

#### 方法

##### `get_request_config()`

获取请求相关的配置。

**返回:** `Dict[str, Any]` - 请求配置字典

##### `validate_config()`

验证配置是否有效。

**返回:** `bool` - 配置是否有效

## 示例

### 基本使用示例

运行基本使用示例：

```bash
cd examples
python basic_usage.py
```

### 高级功能示例

运行高级功能示例：

```bash
cd examples  
python advanced_usage.py
```

## 配置说明

### 环境变量

- `TWITTER_COOKIE`: Twitter登录后的Cookie（必需）
- `HTTP_PROXY`: HTTP代理地址（可选）
- `HTTPS_PROXY`: HTTPS代理地址（可选）
- `TWITTER_USER_AGENT`: 自定义User-Agent（可选）

### 配置文件

配置文件位置：`config/config.json`

```json
{
  "headers": {
    "User-Agent": "浏览器User-Agent",
    "Referer": "https://www.x.com/",
    "Accept": "application/json, text/plain, */*"
  },
  "proxies": {
    "http://": "代理地址或null",
    "https://": "代理地址或null"
  },
  "cookie": "Twitter Cookie",
  "timeout": 30,
  "retry_count": 3,
  "retry_delay": 1
}
```

## 注意事项

1. **Cookie获取**: 需要在浏览器中登录Twitter，然后从开发者工具中获取Cookie
2. **请求频率**: 请合理控制请求频率，避免被限制访问
3. **数据使用**: 请遵守Twitter的服务条款和数据使用政策
4. **错误处理**: 建议在生产环境中加入适当的错误处理和重试机制

## 开发

### 安装开发依赖

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

### 运行测试

```bash
pytest tests/
```

### 代码格式化

```bash
black src/ examples/
```

### 类型检查

```bash
mypy src/
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的推文拉取功能
- 配置管理和错误处理
- 示例代码和文档
