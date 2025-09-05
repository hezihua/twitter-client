#!/usr/bin/env python3
"""
清晰显示推文内容的示例
"""

import asyncio
import sys
import os
import json

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from twitter_client import TwitterClient, ConfigManager

def display_tweet_content(tweets):
    """清晰地显示推文内容"""
    print(f"\n📋 推文内容详情 (共{len(tweets)}条):")
    print("=" * 80)
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n🐦 推文 {i}:")
        print(f"   📝 内容: {tweet['text']}")
        print(f"   🆔 ID: {tweet['id']}")
        print(f"   👤 作者: {tweet['author']['username']}")
        print(f"   📅 时间: {tweet['created_at']}")
        
        metrics = tweet['public_metrics']
        print(f"   📊 互动数据:")
        print(f"      ❤️  点赞: {metrics['like_count']}")
        print(f"      🔄 转发: {metrics['retweet_count']}")
        print(f"      💬 回复: {metrics['reply_count']}")
        
        # 提取话题标签
        hashtags = [word for word in tweet['text'].split() if word.startswith('#')]
        if hashtags:
            print(f"   🏷️  话题: {', '.join(hashtags)}")
        
        print("-" * 60)

def display_formatted_content(client, tweets):
    """使用客户端格式化功能显示"""
    print(f"\n🎨 格式化显示 (使用客户端格式化功能):")
    print("=" * 80)
    
    for i, tweet in enumerate(tweets, 1):
        formatted = client.format_tweet(tweet)
        print(f"\n🐦 推文 {i}:")
        print(f"   📝 {formatted['text']}")
        print(f"   👤 @{formatted['author']}")
        print(f"   📅 {formatted['created_at']}")
        
        metrics = formatted.get('public_metrics', {})
        print(f"   📊 {metrics.get('like_count', 0)}❤️  "
              f"{metrics.get('retweet_count', 0)}🔄  "
              f"{metrics.get('reply_count', 0)}💬")

def analyze_content(tweets):
    """分析推文内容"""
    print(f"\n📊 内容分析:")
    print("=" * 80)
    
    total_chars = 0
    total_likes = 0
    hashtags = {}
    
    for tweet in tweets:
        content = tweet['text']
        total_chars += len(content)
        total_likes += tweet['public_metrics']['like_count']
        
        # 统计话题标签
        words = content.split()
        for word in words:
            if word.startswith('#'):
                hashtags[word] = hashtags.get(word, 0) + 1
    
    print(f"📝 总字符数: {total_chars}")
    print(f"📏 平均长度: {total_chars / len(tweets):.1f} 字符/推文")
    print(f"❤️  总点赞数: {total_likes}")
    print(f"📈 平均点赞: {total_likes / len(tweets):.1f} 点赞/推文")
    
    if hashtags:
        print(f"🏷️  话题标签统计:")
        for tag, count in sorted(hashtags.items(), key=lambda x: x[1], reverse=True):
            print(f"   {tag}: {count}次")

async def main():
    """主函数"""
    print("🐦 推文内容显示示例")
    print("展示如何清晰地查看和分析推文内容")
    
    # 创建客户端
    config_manager = ConfigManager()
    client = TwitterClient(config_manager.get_request_config())
    
    # 获取推文
    user_id = "cellinlab"  # 使用您设置的用户ID
    print(f"\n🔍 获取用户 @{user_id} 的推文...")
    tweets = await client.fetch_user_tweets(user_id=user_id, max_tweets=10)
    
    print(f"✅ 成功获取 {len(tweets)} 条推文")
    
    # 1. 显示原始推文内容
    display_tweet_content(tweets)
    
    # 2. 使用格式化显示
    display_formatted_content(client, tweets)
    
    # 3. 分析推文内容
    analyze_content(tweets)
    
    # 4. 显示JSON格式（部分）
    print(f"\n🔧 JSON格式示例 (第1条推文):")
    print("=" * 80)
    first_tweet = tweets[0] if tweets else {}
    print(json.dumps(first_tweet, indent=2, ensure_ascii=False))
    
    await client.close()
    print(f"\n✅ 演示完成！")

if __name__ == "__main__":
    asyncio.run(main())
