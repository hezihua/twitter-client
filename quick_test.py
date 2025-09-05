#!/usr/bin/env python3
"""
快速测试脚本 - 输入Cookie即可测试
"""

import asyncio
import sys
import os

async def quick_test():
    """快速测试"""
    print("🚀 Twitter真实数据快速测试")
    print("=" * 40)
    
    # 交互式输入Cookie（如果环境变量没有）
    cookie = os.getenv("TWITTER_COOKIE")
    if not cookie:
        print("请粘贴您的Twitter Cookie:")
        print("(从浏览器开发者工具中复制的完整Cookie字符串)")
        print("-" * 40)
        cookie = input().strip()
        
        if not cookie:
            print("❌ Cookie不能为空")
            return
        
        # 临时设置环境变量
        os.environ["TWITTER_COOKIE"] = cookie
    
    print("✅ Cookie已设置")
    
    # 测试获取推文
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cookie": cookie,
                "Referer": "https://x.com/"
            },
            "cookie": cookie,
            "proxies": {"http://": None, "https://": None}
        }
        
        handler = TwitterHandler(config)
        print("⚙️ 正在测试获取推文...")
        
        # 测试用户
        test_users = ["elonmusk", "twitter", "openai"]
        
        for user_id in test_users:
            try:
                print(f"\n🔍 测试用户: @{user_id}")
                
                async for tweet_list in handler.fetch_post_tweet(
                    userId=user_id,
                    page_counts=1,
                    max_counts=2
                ):
                    tweets = tweet_list._to_dict()
                    if tweets:
                        print(f"🎉 成功！获取到 {len(tweets)} 条推文")
                        for i, tweet in enumerate(tweets, 1):
                            text = tweet.get('text', 'N/A')
                            author = tweet.get('author', {}).get('username', 'N/A')
                            print(f"   推文{i}: @{author}: {text[:60]}...")
                        return True
                    break
            except Exception as e:
                print(f"   ❌ @{user_id} 失败: {str(e)[:50]}...")
                continue
        
        print("❌ 所有测试用户都失败了")
        print("可能原因：")
        print("- Cookie已过期")
        print("- 网络连接问题") 
        print("- Cookie格式不正确")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(quick_test())
