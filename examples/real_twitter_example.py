#!/usr/bin/env python3
"""
真实Twitter数据获取示例
使用真实F2项目获取Twitter推文
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from twitter_client import TwitterClient, ConfigManager

async def test_real_twitter():
    """测试真实Twitter数据获取"""
    print("🐦 真实Twitter数据获取测试")
    print("=" * 50)
    
    # 检查环境变量
    cookie = os.getenv("TWITTER_COOKIE")
    if not cookie:
        print("❌ 未设置TWITTER_COOKIE环境变量")
        print("请先设置: export TWITTER_COOKIE='你的Cookie'")
        return
    
    print("✅ 检测到Twitter Cookie")
    print(f"Cookie长度: {len(cookie)} 字符")
    
    try:
        # 创建配置
        config_manager = ConfigManager()
        
        # 更新配置以使用真实Cookie
        config_manager.update_config({
            "cookie": cookie,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://x.com/",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "en",
                "x-twitter-active-user": "yes",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }
        })
        
        print("⚙️ 配置已更新，使用真实Cookie")
        
        # 创建客户端
        client = TwitterClient(config_manager.get_request_config())
        print("✅ Twitter客户端创建成功")
        
        # 测试获取推文
        user_id = "elonmusk"  # 使用一个知名用户进行测试
        print(f"\n🔍 正在获取 @{user_id} 的推文...")
        
        try:
            tweets = await client.fetch_user_tweets(
                user_id=user_id,
                max_tweets=3  # 先获取少量推文测试
            )
            
            if tweets:
                print(f"🎉 成功获取 {len(tweets)} 条真实推文!")
                
                for i, tweet in enumerate(tweets, 1):
                    formatted = client.format_tweet(tweet)
                    print(f"\n📝 推文 {i}:")
                    print(f"   内容: {formatted.get('text', 'N/A')[:100]}...")
                    print(f"   作者: {formatted.get('author', 'N/A')}")
                    print(f"   时间: {formatted.get('created_at', 'N/A')}")
                    
                    metrics = formatted.get('public_metrics', {})
                    if metrics:
                        print(f"   互动: ❤️{metrics.get('like_count', 0)} "
                              f"🔄{metrics.get('retweet_count', 0)} "
                              f"💬{metrics.get('reply_count', 0)}")
            else:
                print("⚠️ 未获取到推文数据")
                print("可能的原因:")
                print("- Cookie已过期")
                print("- 用户不存在或账号受保护")
                print("- 网络连接问题")
        
        except Exception as e:
            print(f"❌ 获取推文失败: {e}")
            print("\n🔧 调试信息:")
            print(f"错误类型: {type(e).__name__}")
            print("\n可能的解决方案:")
            print("1. 检查Cookie是否有效")
            print("2. 尝试刷新Cookie")
            print("3. 检查网络连接")
            print("4. 尝试其他用户ID")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_real_twitter())
