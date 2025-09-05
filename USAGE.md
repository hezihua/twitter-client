# 使用指南

本指南将详细介绍如何使用Twitter推文拉取客户端。

## 1. 环境准备

### 安装依赖

```bash
cd twitter-client
pip install -r requirements.txt
```

### 获取Twitter Cookie

1. 使用浏览器登录 [Twitter/X](https://x.com)
2. 按 F12 打开开发者工具
3. 切换到 "Application" 或 "存储" 标签
4. 在左侧找到 "Cookies" -> "https://x.com"
5. 复制所有Cookie值，格式如下：
   ```
   auth_token=xxxxx; ct0=xxxxx; _ga=xxxxx; ...
   ```

### 设置环境变量

```bash
# Linux/Mac
export TWITTER_COOKIE="你的Cookie内容"

# Windows
set TWITTER_COOKIE=你的Cookie内容
```

## 2. 基本使用

### 方式1：使用配置文件

```bash
# 创建默认配置文件
python -c "from src.twitter_client.config import create_default_config_file; create_default_config_file()"

# 编辑 config/config.json 文件，设置cookie
```

### 方式2：使用环境变量（推荐）

```bash
export TWITTER_COOKIE="你的Cookie"
```

### 运行基本示例

```bash
cd examples
python basic_usage.py
```

## 3. API使用方法

### 同步方式获取推文

```python
import asyncio
from twitter_client import TwitterClient, ConfigManager

async def get_tweets():
    # 初始化
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    # 获取推文
    tweets = await client.fetch_user_tweets(
        user_id="25073877",  # 用户ID
        max_tweets=20        # 最大数量
    )
    
    # 处理数据
    for tweet in tweets:
        formatted = client.format_tweet(tweet)
        print(formatted['text'])
    
    await client.close()

# 运行
asyncio.run(get_tweets())
```

### 流式获取推文

```python
async def stream_tweets():
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    # 流式获取
    async for tweet in client.fetch_user_tweets_stream(
        user_id="25073877",
        max_tweets=100
    ):
        formatted = client.format_tweet(tweet)
        print(f"实时推文: {formatted['text'][:50]}...")
    
    await client.close()

asyncio.run(stream_tweets())
```

## 4. 命令行使用

### 安装为命令行工具

```bash
pip install -e .
```

### 基本命令

```bash
# 获取推文
twitter-client fetch 25073877 --count 10

# 流式获取
twitter-client fetch 25073877 --stream --count 50

# 保存到文件
twitter-client fetch 25073877 --output tweets.json

# 初始化配置
twitter-client config --init

# 验证配置
twitter-client config --validate

# 显示配置
twitter-client config --show
```

## 5. 高级功能

### 批量用户分析

```python
from twitter_client import TwitterClient, ConfigManager

async def analyze_multiple_users():
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    user_ids = ["25073877", "44196397"]  # 多个用户
    
    for user_id in user_ids:
        tweets = await client.fetch_user_tweets(user_id, max_tweets=50)
        
        # 统计分析
        total_likes = sum(
            client.format_tweet(t)['public_metrics']['like_count'] 
            for t in tweets
        )
        
        print(f"用户 {user_id} 总点赞数: {total_likes}")
    
    await client.close()
```

### 数据导出

```python
import json
from datetime import datetime

async def export_tweets():
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    tweets = await client.fetch_user_tweets("25073877", max_tweets=100)
    
    # 格式化数据
    formatted_data = {
        "export_time": datetime.now().isoformat(),
        "user_id": "25073877",
        "tweet_count": len(tweets),
        "tweets": [client.format_tweet(t) for t in tweets]
    }
    
    # 保存到JSON文件
    with open("tweets_export.json", "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
    
    await client.close()
```

### 自定义配置

```python
# 自定义请求配置
custom_config = {
    "headers": {
        "User-Agent": "自定义UserAgent",
        "Referer": "https://x.com/"
    },
    "proxies": {
        "http://": "http://proxy:8080",
        "https://": "http://proxy:8080"
    },
    "cookie": "你的Cookie",
    "timeout": 60
}

client = TwitterClient(custom_config)
```

## 6. 错误处理

### 常见错误及解决方法

#### 1. Cookie错误
```
错误: 配置验证失败
```
**解决方法:**
- 检查Cookie是否正确设置
- 重新获取最新的Cookie
- 确保Cookie格式正确

#### 2. 网络连接错误
```
错误: 获取推文失败
```
**解决方法:**
- 检查网络连接
- 设置代理配置
- 增加超时时间

#### 3. 用户ID错误
```
错误: 未获取到推文数据
```
**解决方法:**
- 检查用户ID是否正确
- 确保用户账号存在且公开
- 尝试其他用户ID

### 错误处理示例

```python
async def safe_fetch_tweets():
    try:
        config_manager = ConfigManager()
        
        # 验证配置
        if not config_manager.validate_config():
            print("配置无效，请检查Cookie设置")
            return
        
        client = TwitterClient(config_manager.get_request_config())
        
        tweets = await client.fetch_user_tweets(
            user_id="25073877",
            max_tweets=20
        )
        
        if not tweets:
            print("未获取到推文，请检查用户ID")
            return
        
        print(f"成功获取 {len(tweets)} 条推文")
        
    except Exception as e:
        print(f"发生错误: {e}")
        # 记录详细错误信息
        import traceback
        traceback.print_exc()
    
    finally:
        if 'client' in locals():
            await client.close()
```

## 7. 性能优化

### 批量处理优化

```python
async def optimized_batch_fetch():
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    # 使用适当的页面大小
    tweets = await client.fetch_user_tweets(
        user_id="25073877",
        max_tweets=200,
        page_size=50  # 调整页面大小以优化性能
    )
    
    await client.close()
```

### 内存优化（流式处理）

```python
async def memory_efficient_processing():
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    # 流式处理，避免内存占用过高
    processed_count = 0
    
    async for tweet in client.fetch_user_tweets_stream(
        user_id="25073877",
        max_tweets=1000,
        page_size=20
    ):
        # 立即处理每条推文
        formatted = client.format_tweet(tweet)
        
        # 执行你的处理逻辑
        # process_tweet(formatted)
        
        processed_count += 1
        if processed_count % 100 == 0:
            print(f"已处理 {processed_count} 条推文")
    
    await client.close()
```

## 8. 注意事项

1. **遵守使用条款**: 请遵守Twitter的服务条款和API使用政策
2. **请求频率控制**: 避免过于频繁的请求，防止被限制访问
3. **Cookie安全**: 妥善保管Cookie信息，不要泄露给他人
4. **数据使用**: 获取的数据仅供个人学习和研究使用
5. **错误处理**: 在生产环境中加入完善的错误处理机制

## 9. 疑难解答

### Q: 为什么获取不到推文？
A: 检查以下项目：
- Cookie是否有效
- 网络连接是否正常
- 用户ID是否正确
- 用户账号是否为公开账号

### Q: 如何获取用户ID？
A: 用户ID可以通过以下方式获取：
- 使用第三方工具查询
- 查看用户主页的URL
- 使用Twitter API搜索功能

### Q: 支持哪些数据格式？
A: 目前支持：
- JSON格式导出
- Python字典格式
- 自定义格式化输出

### Q: 如何处理大量数据？
A: 建议：
- 使用流式处理避免内存溢出
- 分批次处理大量用户
- 合理设置页面大小和请求间隔
