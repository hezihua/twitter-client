# 抖音视频拉取客户端

基于F2项目的抖音API封装，提供简单易用的抖音视频拉取接口。

## ✨ 特性

- 🚀 异步视频拉取，支持批量和流式获取
- 🔧 灵活的配置管理，支持环境变量和配置文件
- 📊 内置数据分析和格式化功能  
- 🛡️ 完善的错误处理和日志记录
- 🎯 简洁的API设计，易于集成
- 📦 基于成熟的F2项目，稳定可靠
- 🎵 支持用户视频、视频详情、用户资料等功能

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保F2项目已安装
pip install python-dotenv

# 项目已包含F2项目，可直接使用
```

### 2. 环境配置

创建 `.env` 文件：

```bash
# 复制示例配置
cp douyin_env.example .env

# 编辑配置文件
nano .env
```

在 `.env` 文件中设置：

```bash
# 抖音Cookie (必需)
DOUYIN_COOKIE=你的抖音Cookie字符串

# 下载路径 (可选)
DOUYIN_DOWNLOAD_PATH=./downloads/douyin/

# 代理设置 (可选)
# HTTP_PROXY=http://proxy:8080
# HTTPS_PROXY=http://proxy:8080
```

### 3. 获取抖音Cookie

1. 打开浏览器，访问 `https://www.douyin.com`
2. 登录你的抖音账户
3. 按 `F12` 打开开发者工具
4. 点击 `Network` 标签，刷新页面
5. 找到任一请求，复制 `Cookie` 请求头
6. 将Cookie设置到 `.env` 文件中

### 4. 基本使用

```python
import asyncio
from src.douyin_client import DouyinClient, DouyinConfigManager

async def main():
    # 创建配置管理器
    config_manager = DouyinConfigManager()
    
    # 创建抖音客户端
    client = DouyinClient(config_manager.get_request_config())
    
    # 获取用户视频 (需要替换为真实的用户ID)
    user_id = "MS4wLjABAAAANwkJuWIRFOzg5uCpGgC5Ac2h_bgVVFlo9wUL2vhTW8E"
    videos = await client.fetch_user_videos(user_id, max_videos=10)
    
    # 显示视频信息
    for video in videos:
        formatted = client.format_video(video)
        print(f"标题: {formatted['desc']}")
        print(f"点赞: {formatted['statistics']['digg_count']}")
        print(f"链接: {formatted['url']}")
        print("-" * 50)
    
    # 关闭客户端
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 📋 API 文档

### DouyinClient 类

#### 初始化
```python
client = DouyinClient(config)
```

#### 主要方法

##### 获取用户视频
```python
videos = await client.fetch_user_videos(
    user_id="用户ID",
    max_videos=20,
    page_size=20,
    max_cursor=""
)
```

##### 获取视频详情
```python
video_detail = await client.fetch_video_detail(aweme_id="视频ID")
```

##### 获取用户资料
```python
user_profile = await client.fetch_user_profile(user_id="用户ID")
```

##### 格式化视频数据
```python
formatted_video = client.format_video(raw_video_data)
```

### 配置管理

#### DouyinConfigManager 类

```python
from src.douyin_client import DouyinConfigManager

# 创建配置管理器
config_manager = DouyinConfigManager()

# 验证配置
is_valid = config_manager.validate_config()

# 获取请求配置
request_config = config_manager.get_request_config()

# 获取下载配置
download_config = config_manager.get_download_config()

# 更新配置
config_manager.update_config({
    "timeout": 60,
    "max_retries": 5
})

# 保存配置
config_manager.save_config()
```

## 🎬 使用示例

### 示例1：获取用户视频列表

```python
import asyncio
from src.douyin_client import DouyinClient, DouyinConfigManager

async def get_user_videos():
    config_manager = DouyinConfigManager()
    client = DouyinClient(config_manager.get_request_config())
    
    # 用户ID (需要从抖音获取真实的sec_user_id)
    user_id = "MS4wLjABAAAA..."
    
    try:
        # 获取用户资料
        profile = await client.fetch_user_profile(user_id)
        print(f"用户: {profile.get('nickname', 'N/A')}")
        print(f"粉丝: {profile.get('follower_count', 0)}")
        
        # 获取视频列表
        videos = await client.fetch_user_videos(user_id, max_videos=10)
        
        for i, video in enumerate(videos, 1):
            formatted = client.format_video(video)
            print(f"\n视频 {i}:")
            print(f"  标题: {formatted['desc'][:50]}...")
            print(f"  点赞: {formatted['statistics']['digg_count']}")
            print(f"  评论: {formatted['statistics']['comment_count']}")
            print(f"  时长: {formatted['video']['duration']}秒")
            
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await client.close()

asyncio.run(get_user_videos())
```

### 示例2：视频数据分析

```python
import asyncio
from src.douyin_client import DouyinClient, DouyinConfigManager

async def analyze_videos():
    config_manager = DouyinConfigManager()
    client = DouyinClient(config_manager.get_request_config())
    
    user_id = "MS4wLjABAAAA..."
    videos = await client.fetch_user_videos(user_id, max_videos=50)
    
    # 数据分析
    total_likes = sum(v.get('statistics', {}).get('digg_count', 0) for v in videos)
    total_comments = sum(v.get('statistics', {}).get('comment_count', 0) for v in videos)
    avg_duration = sum(v.get('video', {}).get('duration', 0) for v in videos) / len(videos)
    
    print(f"视频总数: {len(videos)}")
    print(f"总点赞数: {total_likes}")
    print(f"总评论数: {total_comments}")
    print(f"平均时长: {avg_duration:.1f}秒")
    print(f"平均点赞数: {total_likes/len(videos):.1f}")
    
    # 找出最受欢迎的视频
    most_liked = max(videos, key=lambda x: x.get('statistics', {}).get('digg_count', 0))
    formatted = client.format_video(most_liked)
    print(f"\n最受欢迎视频:")
    print(f"  标题: {formatted['desc']}")
    print(f"  点赞: {formatted['statistics']['digg_count']}")
    
    await client.close()

asyncio.run(analyze_videos())
```

## 🧪 测试

运行测试脚本：

```bash
# 测试基本功能
python test_douyin.py

# 运行示例
python examples/douyin_basic_usage.py
```

## ⚠️ 注意事项

1. **Cookie 管理**
   - Cookie 需要定期更新
   - 建议使用移动端 User-Agent
   - 保护好你的 Cookie 信息

2. **请求频率**
   - 合理控制请求频率，避免被限制
   - 建议在请求间添加延迟
   - 遵守抖音的 robots.txt 和使用条款

3. **用户ID获取**
   - 用户ID是 `sec_user_id` 格式
   - 可以从用户主页的网络请求中获取
   - 格式类似：`MS4wLjABAAAA...`

4. **数据使用**
   - 仅用于学习和研究目的
   - 不要用于商业用途
   - 尊重用户隐私和版权

## 🔧 配置选项

### 请求配置
```json
{
  "headers": {
    "User-Agent": "移动端浏览器标识",
    "Referer": "https://www.douyin.com/",
    "Accept": "application/json, text/plain, */*"
  },
  "proxies": {
    "http://": null,
    "https://": null
  },
  "cookie": "你的Cookie",
  "timeout": 30,
  "max_retries": 3
}
```

### 下载配置
```json
{
  "path": "./downloads/douyin/",
  "naming": "aweme_id",
  "max_concurrent": 3,
  "chunk_size": 1048576
}
```

### 过滤配置
```json
{
  "min_duration": 0,
  "max_duration": 0,
  "min_digg_count": 0,
  "keywords": [],
  "exclude_keywords": []
}
```

## 📚 更多资源

- [F2项目文档](https://github.com/JohnstonLiu/F2)
- [抖音开发者文档](https://developer.open-douyin.com/)
- [项目问题反馈](https://github.com/your-repo/issues)

## 📄 许可证

本项目基于 MIT 许可证开源。使用时请遵守相关法律法规和平台使用条款。
