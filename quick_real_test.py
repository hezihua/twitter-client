#!/usr/bin/env python3
"""
快速真实Twitter数据测试 - 带超时和进度显示
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# 加载.env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

async def test_real_twitter_with_timeout():
    """带超时的真实Twitter测试"""
    print("🚀 快速真实Twitter数据测试")
    print("=" * 40)
    
    cookie = os.getenv("TWITTER_COOKIE")
    if not cookie:
        print("❌ 未找到TWITTER_COOKIE")
        return False
    
    print(f"✅ Cookie已加载 (长度: {len(cookie)})")
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cookie": cookie,
                "Referer": "https://x.com/",
            },
            "cookie": cookie,
            "proxies": {"http://": None, "https://": None}
        }
        
        handler = TwitterHandler(config)
        print("✅ TwitterHandler创建成功")
        
        # 测试简单用户
        test_user = "twitter"  # 官方账号，应该有推文
        print(f"\n🔍 获取 @{test_user} 的推文 (30秒超时)...")
        
        try:
            # 设置超时
            timeout_seconds = 30
            start_time = time.time()
            
            async def get_tweets():
                async for tweet_list in handler.fetch_post_tweet(
                    userId=test_user,
                    page_counts=1,
                    max_counts=1
                ):
                    return tweet_list._to_dict()
                return []
            
            # 带进度的等待
            tweets_task = asyncio.create_task(get_tweets())
            
            while not tweets_task.done():
                elapsed = time.time() - start_time
                if elapsed > timeout_seconds:
                    tweets_task.cancel()
                    print(f"\n⏰ 超时 ({timeout_seconds}秒)")
                    break
                
                print(f"\r⏳ 请求中... {elapsed:.1f}s", end="", flush=True)
                await asyncio.sleep(0.5)
            
            if tweets_task.done() and not tweets_task.cancelled():
                tweets = await tweets_task
                if tweets and len(tweets) > 0:
                    print(f"\n🎉 成功获取 {len(tweets)} 条推文!")
                    
                    tweet = tweets[0]
                    print(f"📝 内容: {tweet.get('text', 'N/A')[:100]}...")
                    print(f"👤 作者: {tweet.get('author', {}).get('username', 'N/A')}")
                    
                    # 保存结果
                    result = {
                        "success": True,
                        "user": test_user,
                        "tweets_count": len(tweets),
                        "sample_tweet": tweet.get('text', '')[:200]
                    }
                    
                    with open("real_twitter_test_result.json", "w", encoding="utf-8") as f:
                        import json
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    
                    print("✅ 结果已保存到 real_twitter_test_result.json")
                    return True
                else:
                    print(f"\n⚠️ 未获取到推文数据")
            
        except asyncio.CancelledError:
            print("\n❌ 请求被取消")
        except Exception as e:
            print(f"\n❌ 获取推文失败: {e}")
            print(f"错误类型: {type(e).__name__}")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
    
    return False

def show_status():
    """显示当前状态"""
    print("📊 当前状态:")
    print("=" * 25)
    
    # 检查.env
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env文件存在")
    else:
        print("❌ .env文件不存在")
    
    # 检查Cookie
    cookie = os.getenv("TWITTER_COOKIE")
    if cookie:
        print(f"✅ Cookie已设置 (长度: {len(cookie)})")
        print(f"✅ 包含auth_token: {'auth_token=' in cookie}")
        print(f"✅ 包含ct0: {'ct0=' in cookie}")
    else:
        print("❌ Cookie未设置")
    
    # 检查F2
    try:
        from f2.apps.twitter.handler import TwitterHandler
        print("✅ F2项目可用")
    except ImportError:
        print("❌ F2项目不可用")

async def main():
    """主函数"""
    print("🐦 Twitter真实数据快速测试")
    print("带超时和进度显示")
    print()
    
    show_status()
    print()
    
    if await test_real_twitter_with_timeout():
        print("\n🎉 恭喜！真实Twitter数据获取成功！")
        print("📝 现在可以使用:")
        print("  python examples/simple_usage.py")
    else:
        print("\n🔧 故障排除建议:")
        print("1. 检查网络连接")
        print("2. 验证Cookie是否最新")
        print("3. 稍后重试")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
