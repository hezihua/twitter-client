#!/usr/bin/env python3
"""
最小化Twitter测试 - 尝试获取任何响应
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def minimal_twitter_test():
    """最简单的Twitter测试"""
    print("🔬 最小化Twitter测试")
    print("=" * 30)
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        cookie = os.getenv("TWITTER_COOKIE")
        if not cookie:
            print("❌ Cookie未设置")
            return False
        
        print(f"✅ Cookie: {len(cookie)} 字符")
        
        # 最简配置
        config = {
            "cookie": cookie,
            "headers": {
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*"
            },
            "proxies": None
        }
        
        handler = TwitterHandler(config)
        print("✅ Handler创建")
        
        # 尝试最简单的请求
        print("\n🔍 尝试极简请求...")
        
        try:
            # 手动设置更短的超时
            import time
            start = time.time()
            
            async for tweet_list in handler.fetch_post_tweet(
                userId="Twitter",  # 官方账号
                page_counts=1,
                max_counts=1
            ):
                elapsed = time.time() - start
                print(f"⚡ 响应时间: {elapsed:.1f}秒")
                
                # 检查响应类型
                print(f"📦 响应类型: {type(tweet_list)}")
                
                # 尝试获取数据
                try:
                    raw_data = tweet_list._to_raw()
                    print(f"📊 原始数据长度: {len(raw_data)}")
                    
                    dict_data = tweet_list._to_dict()
                    print(f"📋 字典数据: {len(dict_data)} 项")
                    
                    if dict_data:
                        print("🎉 成功获取数据!")
                        return True
                    else:
                        print("⚠️ 数据为空")
                        
                except Exception as e:
                    print(f"❌ 数据处理错误: {e}")
                
                return False
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            print(f"异常类型: {type(e).__name__}")
            
            # 检查是否是网络问题
            if "timeout" in str(e).lower():
                print("🌐 这是网络超时问题")
            elif "unauthorized" in str(e).lower():
                print("🔐 这是认证问题 - Cookie可能过期")
            elif "rate limit" in str(e).lower():
                print("⏱️ 这是频率限制问题")
            
            return False
            
    except ImportError:
        print("❌ F2导入失败")
        return False
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False

async def test_f2_versions():
    """测试F2版本信息"""
    print("\n🔍 F2项目信息:")
    print("=" * 25)
    
    try:
        import f2
        if hasattr(f2, '__version__'):
            print(f"版本: {f2.__version__}")
        
        from f2.apps.twitter import handler
        print(f"模块路径: {handler.__file__}")
        
        # 检查TwitterHandler的方法
        from f2.apps.twitter.handler import TwitterHandler
        methods = [m for m in dir(TwitterHandler) if not m.startswith('_')]
        print(f"可用方法: {methods[:5]}...")
        
    except Exception as e:
        print(f"版本检查失败: {e}")

async def main():
    """主函数"""
    # 测试F2信息
    await test_f2_versions()
    
    # 运行最小测试
    success = await minimal_twitter_test()
    
    if success:
        print("\n🎉 最小测试成功!")
        print("现在可以运行完整测试")
    else:
        print("\n🔧 建议检查:")
        print("1. Cookie是否最新")
        print("2. 网络连接")
        print("3. Twitter服务状态")
        
        # 提供Cookie检查工具
        print("\n💡 快速Cookie检查:")
        cookie = os.getenv("TWITTER_COOKIE")
        if cookie:
            parts = cookie.split(';')
            print(f"   Cookie段数: {len(parts)}")
            
            required = ['auth_token', 'ct0', 'guest_id']
            for req in required:
                has_it = any(req in part for part in parts)
                print(f"   {req}: {'✅' if has_it else '❌'}")

if __name__ == "__main__":
    asyncio.run(main())
