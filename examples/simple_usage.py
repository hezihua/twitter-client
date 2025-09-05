#!/usr/bin/env python3
"""
Twitter客户端简单使用示例
快速上手指南
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from twitter_client import TwitterClient, ConfigManager

async def main():
    """简单使用示例"""
    print("🐦 Twitter客户端简单使用示例")
    print()
    
    # 1. 创建客户端
    print("1️⃣ 创建客户端...")
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    print("✅ 客户端创建成功")
    
    # 2. 获取推文
    print("\n2️⃣ 获取推文...")
    user_id = "cellinlab"  # 可以替换为任意用户ID
    tweets = await client.fetch_user_tweets(user_id=user_id, max_tweets=10)
    print(tweets)
    print(f"✅ 获取到 {len(tweets)} 条推文")
    
    # 3. 显示推文
    print("\n3️⃣ 推文内容:")
    for i, tweet in enumerate(tweets, 1):
        formatted = client.format_tweet(tweet)
        print(f"   🐦 推文{i}: {formatted['text'][:60]}...")
        print(f"      ❤️ {formatted['public_metrics']['like_count']} 点赞")
    
    # 4. 关闭客户端
    await client.close()
    print("\n✅ 完成！")

if __name__ == "__main__":
    asyncio.run(main())
