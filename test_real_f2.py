#!/usr/bin/env python3
"""
快速测试真实F2项目
"""

import asyncio
import os

def test_f2_import():
    """测试F2导入"""
    print("🔍 测试F2项目导入...")
    try:
        from f2.apps.twitter.handler import TwitterHandler
        print("✅ F2项目导入成功！")
        return True
    except ImportError as e:
        print(f"❌ F2项目导入失败: {e}")
        return False

async def test_with_cookie():
    """使用Cookie测试"""
    print("\n🍪 测试Cookie配置...")
    
    # 检查环境变量
    cookie = os.getenv("TWITTER_COOKIE")
    if not cookie:
        print("⚠️  未设置TWITTER_COOKIE环境变量")
        print("\n📝 设置方法:")
        print("export TWITTER_COOKIE='你的Twitter Cookie'")
        print("\n🍪 如何获取Cookie:")
        print("1. 打开浏览器，访问 https://x.com")
        print("2. 登录你的Twitter账号") 
        print("3. 按F12打开开发者工具")
        print("4. 刷新页面，在Network标签找任意请求")
        print("5. 复制Request Headers中的Cookie值")
        return False
    
    print(f"✅ Cookie已设置 (长度: {len(cookie)})")
    
    # 测试F2配置
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        # 简单配置
        config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cookie": cookie,
                "Referer": "https://x.com/"
            },
            "cookie": cookie,
            "proxies": {"http://": None, "https://": None}
        }
        
        print("⚙️ 创建TwitterHandler...")
        handler = TwitterHandler(config)
        print("✅ TwitterHandler创建成功")
        
        # 测试获取推文
        print("\n🔍 测试获取推文...")
        user_id = "elonmusk"  # 使用知名用户测试
        
        try:
            async for tweet_list in handler.fetch_post_tweet(
                userId=user_id,
                page_counts=1,
                max_counts=1
            ):
                tweets = tweet_list._to_dict()
                if tweets:
                    print(f"🎉 成功获取 {len(tweets)} 条真实推文!")
                    tweet = tweets[0]
                    print(f"📝 推文内容: {tweet.get('text', 'N/A')[:100]}...")
                    print(f"👤 作者: {tweet.get('author', {}).get('username', 'N/A')}")
                    return True
                else:
                    print("⚠️ 未获取到推文数据")
                    return False
        except Exception as e:
            print(f"❌ 获取推文失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            return False
            
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        return False

async def main():
    """主函数"""
    print("🐦 快速测试真实F2项目")
    print("=" * 40)
    
    # 1. 测试导入
    if not test_f2_import():
        print("\n❌ 请先安装F2项目:")
        print("cd /tmp/F2_correct && pip install -e .")
        return
    
    # 2. 测试Cookie
    success = await test_with_cookie()
    
    if success:
        print("\n🎉 恭喜！真实F2项目配置成功！")
        print("现在可以获取真实Twitter数据了")
    else:
        print("\n⚠️  配置未完成，但F2项目已正确安装")
        print("设置正确的Cookie后即可获取真实数据")

if __name__ == "__main__":
    asyncio.run(main())
