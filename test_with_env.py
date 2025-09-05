#!/usr/bin/env python3
"""
支持.env文件的Twitter测试脚本
"""

import asyncio
import os
import sys
from pathlib import Path

# 加载.env文件
try:
    from dotenv import load_dotenv
    # 查找.env文件
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ .env文件已加载")
    else:
        print("⚠️  .env文件不存在，使用系统环境变量")
        print("📝 创建.env文件:")
        print(f"   cp {Path(__file__).parent}/env.example {Path(__file__).parent}/.env")
        print("   然后编辑.env文件设置TWITTER_COOKIE")
except ImportError:
    print("⚠️  python-dotenv未安装，跳过.env文件加载")

async def test_with_env():
    """使用.env配置测试"""
    print("\n🐦 使用.env配置测试Twitter客户端")
    print("=" * 50)
    
    # 从环境变量读取配置
    cookie = os.getenv("TWITTER_COOKIE")
    user_agent = os.getenv("TWITTER_USER_AGENT", 
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")
    
    print(f"📋 配置信息:")
    print(f"   Cookie: {'✅ 已设置' if cookie else '❌ 未设置'}")
    print(f"   User-Agent: {user_agent[:50]}...")
    print(f"   日志级别: {log_level}")
    print(f"   HTTP代理: {http_proxy if http_proxy else '未设置'}")
    print(f"   HTTPS代理: {https_proxy if https_proxy else '未设置'}")
    
    if not cookie:
        print("\n❌ TWITTER_COOKIE未设置")
        print("请在.env文件中设置:")
        print("TWITTER_COOKIE=your_cookie_here")
        return False
    
    # 测试F2
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        # 构建代理配置
        proxies = {"http://": http_proxy, "https://": https_proxy}
        if not http_proxy and not https_proxy:
            proxies = {"http://": None, "https://": None}
        
        config = {
            "headers": {
                "User-Agent": user_agent,
                "Cookie": cookie,
                "Referer": "https://x.com/",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "en",
                "x-twitter-active-user": "yes",
            },
            "cookie": cookie,
            "proxies": proxies
        }
        
        print(f"\n⚙️ 创建TwitterHandler...")
        handler = TwitterHandler(config)
        print("✅ TwitterHandler创建成功")
        
        # 测试获取推文
        print(f"\n🔍 测试获取推文...")
        test_users = ["elonmusk", "openai", "twitter"]
        
        for user_id in test_users:
            try:
                print(f"   测试用户: @{user_id}")
                async for tweet_list in handler.fetch_post_tweet(
                    userId=user_id,
                    page_counts=1,
                    max_counts=1
                ):
                    tweets = tweet_list._to_dict()
                    if tweets and len(tweets) > 0:
                        tweet = tweets[0]
                        text = tweet.get('text', 'N/A')
                        author = tweet.get('author', {}).get('username', 'N/A')
                        
                        print(f"   🎉 成功！")
                        print(f"   📝 推文: {text[:80]}...")
                        print(f"   👤 作者: @{author}")
                        return True
                    break
            except Exception as e:
                print(f"   ❌ @{user_id} 失败: {str(e)[:50]}...")
                continue
        
        print("\n❌ 所有测试用户都失败了")
        print("请检查:")
        print("- Cookie是否有效")
        print("- 网络连接是否正常")
        return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def create_env_file():
    """交互式创建.env文件"""
    print("\n📝 创建.env文件")
    print("=" * 30)
    
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print(f"⚠️  .env文件已存在: {env_path}")
        choice = input("是否覆盖? (y/N): ").strip().lower()
        if choice != 'y':
            return
    
    print("请提供以下信息 (按Enter使用默认值):")
    
    # 获取Cookie
    cookie = input("Twitter Cookie (必需): ").strip()
    if not cookie:
        print("❌ Cookie是必需的")
        return
    
    # 其他可选配置
    user_agent = input("User-Agent (可选, 按Enter使用默认): ").strip()
    if not user_agent:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    http_proxy = input("HTTP代理 (可选): ").strip()
    https_proxy = input("HTTPS代理 (可选): ").strip()
    log_level = input("日志级别 [INFO]: ").strip() or "INFO"
    
    # 创建.env文件内容
    env_content = f"""# Twitter推文拉取客户端环境变量配置
# 自动生成于 {Path(__file__).name}

# Twitter Cookie (必需)
TWITTER_COOKIE={cookie}

# User-Agent
TWITTER_USER_AGENT={user_agent}

# 日志级别
LOG_LEVEL={log_level}
"""
    
    if http_proxy:
        env_content += f"\n# HTTP代理\nHTTP_PROXY={http_proxy}\n"
    if https_proxy:
        env_content += f"\n# HTTPS代理\nHTTPS_PROXY={https_proxy}\n"
    
    # 写入文件
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ .env文件已创建: {env_path}")
        return True
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False

async def main():
    """主函数"""
    print("🔧 .env配置的Twitter客户端测试")
    print("=" * 50)
    
    # 检查.env文件
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print("📁 .env文件不存在")
        choice = input("是否创建.env文件? (Y/n): ").strip().lower()
        if choice != 'n':
            if not create_env_file():
                return
            # 重新加载.env文件
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
                print("✅ 新创建的.env文件已加载")
            except ImportError:
                pass
    
    # 运行测试
    success = await test_with_env()
    
    if success:
        print("\n🎉 .env配置成功！")
        print("现在可以使用以下命令获取真实推文:")
        print("  python examples/simple_usage.py")
    else:
        print("\n⚠️  配置需要调整")
        print("请检查.env文件中的TWITTER_COOKIE设置")

if __name__ == "__main__":
    asyncio.run(main())
