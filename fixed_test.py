#!/usr/bin/env python3
"""
修复配置格式的Twitter测试
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_with_correct_config():
    """使用正确配置格式测试"""
    print("🔧 修复配置格式测试")
    print("=" * 30)
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        cookie = os.getenv("TWITTER_COOKIE")
        if not cookie:
            print("❌ Cookie未设置")
            return False
        
        print(f"✅ Cookie: {len(cookie)} 字符")
        
        # F2项目的标准配置格式
        config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://x.com/",
                "Origin": "https://x.com",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            },
            "proxies": {
                "http://": None,
                "https://": None
            },
            "cookie": cookie
        }
        
        print("⚙️ 尝试创建TwitterHandler...")
        try:
            handler = TwitterHandler(config)
            print("✅ TwitterHandler创建成功!")
            
            # 测试简单请求
            print("\n🔍 测试获取推文...")
            
            try:
                # 使用更直接的方法
                async for tweet_list in handler.fetch_post_tweet(
                    userId="elonmusk",  # 知名用户
                    page_counts=1,
                    max_counts=1
                ):
                    print("📦 收到响应!")
                    
                    # 检查响应
                    try:
                        tweets = tweet_list._to_dict()
                        print(f"📊 获取推文数: {len(tweets)}")
                        
                        if tweets and len(tweets) > 0:
                            tweet = tweets[0]
                            print("🎉 成功获取推文!")
                            print(f"📝 内容: {tweet.get('text', 'N/A')[:80]}...")
                            print(f"👤 作者: {tweet.get('author', {}).get('username', 'N/A')}")
                            return True
                        else:
                            print("⚠️ 推文列表为空")
                            return False
                            
                    except Exception as e:
                        print(f"❌ 数据解析错误: {e}")
                        # 尝试获取原始数据
                        try:
                            raw = tweet_list._to_raw()
                            print(f"📄 原始数据长度: {len(raw)}")
                            if "error" in raw.lower():
                                print("⚠️ API返回错误")
                            return False
                        except:
                            return False
                
                print("⚠️ 没有收到任何响应")
                return False
                
            except Exception as e:
                print(f"❌ 请求失败: {e}")
                print(f"错误类型: {type(e).__name__}")
                
                # 详细错误分析
                error_str = str(e).lower()
                if "unauthorized" in error_str:
                    print("🔐 认证失败 - Cookie无效或过期")
                elif "forbidden" in error_str:
                    print("🚫 访问被禁止 - 可能需要更新Cookie")
                elif "not found" in error_str:
                    print("🔍 用户不存在或受保护")
                elif "timeout" in error_str:
                    print("⏰ 网络超时")
                else:
                    print(f"❓ 未知错误: {e}")
                
                return False
                
        except Exception as e:
            print(f"❌ TwitterHandler创建失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            
            # 分析初始化错误
            if "nonetype" in str(e).lower():
                print("🔧 配置对象为空，检查配置格式")
            elif "attribute" in str(e).lower():
                print("🔧 配置缺少必要属性")
            
            return False
            
    except ImportError as e:
        print(f"❌ F2导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def show_debug_info():
    """显示调试信息"""
    print("\n🔍 调试信息:")
    print("=" * 20)
    
    cookie = os.getenv("TWITTER_COOKIE")
    if cookie:
        # 分析Cookie结构
        parts = [p.strip() for p in cookie.split(';') if p.strip()]
        print(f"Cookie组件数量: {len(parts)}")
        
        # 检查关键组件
        key_parts = {}
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                key_parts[key.strip()] = len(value)
        
        important = ['auth_token', 'ct0', 'guest_id', 'twid']
        for key in important:
            if key in key_parts:
                print(f"  ✅ {key}: {key_parts[key]} 字符")
            else:
                print(f"  ❌ {key}: 缺失")
    else:
        print("❌ 未找到Cookie")

async def main():
    """主函数"""
    print("🐦 修复配置的Twitter测试")
    print("="*40)
    
    show_debug_info()
    
    success = await test_with_correct_config()
    
    if success:
        print("\n🎉 测试成功！现在可以获取真实Twitter数据了!")
    else:
        print("\n💡 如果仍然失败，请尝试:")
        print("1. 重新获取最新Cookie (最重要)")
        print("2. 确保登录状态有效")
        print("3. 清除浏览器缓存后重新登录")

if __name__ == "__main__":
    asyncio.run(main())
