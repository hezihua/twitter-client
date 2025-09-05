#!/usr/bin/env python3
"""
Twitter API 故障排除工具
"""

import asyncio
import os
import time
from dotenv import load_dotenv

load_dotenv()

async def test_different_approaches():
    """测试不同的方法"""
    print("🔧 Twitter API 故障排除")
    print("=" * 40)
    
    cookie = os.getenv("TWITTER_COOKIE")
    if not cookie:
        print("❌ Cookie未设置")
        return
    
    print("📋 诊断信息:")
    print(f"   Cookie长度: {len(cookie)}")
    print(f"   包含guest_id: {'guest_id=' in cookie}")
    print(f"   包含auth_token: {'auth_token=' in cookie}")
    print(f"   包含ct0: {'ct0=' in cookie}")
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        # 方法1：尝试更简单的配置
        print("\n🔍 方法1: 简化配置测试")
        simple_config = {
            "cookie": cookie,
            "headers": {"User-Agent": "Mozilla/5.0"},
            "proxies": {"http://": None, "https://": None}
        }
        
        handler = TwitterHandler(simple_config)
        
        # 测试知名用户（更可能有数据）
        test_users = ["X", "elonmusk", "OpenAI"]
        
        for user in test_users:
            print(f"\n   测试 @{user} (10秒超时)...")
            try:
                start_time = time.time()
                async def quick_test():
                    async for tweet_list in handler.fetch_post_tweet(
                        userId=user,
                        page_counts=1,
                        max_counts=1
                    ):
                        return tweet_list._to_dict()
                    return []
                
                # 短超时测试
                tweets = await asyncio.wait_for(quick_test(), timeout=10.0)
                
                if tweets:
                    elapsed = time.time() - start_time
                    print(f"   ✅ 成功! ({elapsed:.1f}秒)")
                    tweet = tweets[0]
                    print(f"   📝 {tweet.get('text', '')[:80]}...")
                    return True
                else:
                    print(f"   ⚠️ 无数据")
                    
            except asyncio.TimeoutError:
                print(f"   ⏰ 超时")
            except Exception as e:
                print(f"   ❌ 错误: {str(e)[:50]}...")
        
        print("\n🔧 可能的原因:")
        print("1. Cookie已过期 (最常见)")
        print("2. Twitter API限制")
        print("3. 网络连接问题")
        print("4. 用户账号受保护")
        
        print("\n💡 解决建议:")
        print("1. 重新获取最新Cookie:")
        print("   - 清除浏览器缓存")
        print("   - 重新登录 x.com")
        print("   - 获取新的Cookie")
        print("2. 尝试不同的网络环境")
        print("3. 检查用户是否公开")
        
    except Exception as e:
        print(f"❌ 初始化错误: {e}")

def show_cookie_refresh_guide():
    """显示Cookie刷新指南"""
    print("\n🔄 Cookie刷新指南:")
    print("=" * 30)
    print("1. 打开浏览器无痕模式")
    print("2. 访问 https://x.com")
    print("3. 重新登录您的账号")
    print("4. 按F12 -> Network标签")
    print("5. 刷新页面")
    print("6. 复制新的Cookie")
    print("7. 更新.env文件")

async def main():
    """主函数"""
    await test_different_approaches()
    show_cookie_refresh_guide()
    
    print("\n🎯 下一步:")
    print("如果问题依然存在，最可能是Cookie过期")
    print("请按照上述指南刷新Cookie")

if __name__ == "__main__":
    asyncio.run(main())
