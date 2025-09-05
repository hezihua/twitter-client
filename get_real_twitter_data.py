#!/usr/bin/env python3
"""
获取真实Twitter数据的完整配置指南
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def show_cookie_guide():
    """显示获取Twitter Cookie的详细指南"""
    print("🍪 如何获取Twitter Cookie:")
    print("=" * 60)
    print()
    print("1️⃣ 登录Twitter:")
    print("   打开浏览器，访问 https://x.com (Twitter)")
    print("   使用您的账号登录")
    print()
    print("2️⃣ 打开开发者工具:")
    print("   按 F12 键打开开发者工具")
    print("   或右键点击页面 -> 检查")
    print()
    print("3️⃣ 获取Cookie:")
    print("   方法A - 从Application标签获取:")
    print("   - 点击 Application (应用) 标签")
    print("   - 左侧展开 Cookies -> https://x.com")
    print("   - 复制所有cookie值")
    print()
    print("   方法B - 从Network标签获取:")
    print("   - 点击 Network (网络) 标签")
    print("   - 刷新页面 (F5)")
    print("   - 点击任意请求")
    print("   - 在Request Headers中找到Cookie字段")
    print("   - 复制完整的Cookie值")
    print()
    print("4️⃣ Cookie格式示例:")
    print("   auth_token=xxx; ct0=xxx; _ga=xxx; _gid=xxx; ...")
    print()
    print("5️⃣ 设置环境变量:")
    print("   export TWITTER_COOKIE='你的Cookie值'")
    print()

def create_real_twitter_example():
    """创建真实Twitter数据获取示例"""
    content = '''#!/usr/bin/env python3
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
        print(f"\\n🔍 正在获取 @{user_id} 的推文...")
        
        try:
            tweets = await client.fetch_user_tweets(
                user_id=user_id,
                max_tweets=3  # 先获取少量推文测试
            )
            
            if tweets:
                print(f"🎉 成功获取 {len(tweets)} 条真实推文!")
                
                for i, tweet in enumerate(tweets, 1):
                    formatted = client.format_tweet(tweet)
                    print(f"\\n📝 推文 {i}:")
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
            print("\\n🔧 调试信息:")
            print(f"错误类型: {type(e).__name__}")
            print("\\n可能的解决方案:")
            print("1. 检查Cookie是否有效")
            print("2. 尝试刷新Cookie")
            print("3. 检查网络连接")
            print("4. 尝试其他用户ID")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_real_twitter())
'''
    
    example_path = Path(__file__).parent / "examples" / "real_twitter_example.py"
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 真实Twitter示例已创建: {example_path}")

def check_f2_installation():
    """检查F2项目安装状态"""
    print("🔍 检查F2项目安装状态:")
    print("=" * 40)
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        print("✅ 真实F2项目已安装")
        
        # 检查F2版本
        import f2
        if hasattr(f2, '__version__'):
            print(f"📦 F2版本: {f2.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ F2项目导入失败: {e}")
        return False

def update_client_for_real_f2():
    """更新客户端以使用真实F2"""
    print("🔧 更新客户端配置以使用真实F2...")
    
    client_file = Path(__file__).parent / "src" / "twitter_client" / "client.py"
    
    if client_file.exists():
        content = client_file.read_text(encoding='utf-8')
        
        # 检查是否仍在使用模拟模块
        if "f2_mock" in content:
            # 更新导入语句
            new_import = '''try:
    from f2.apps.twitter.handler import TwitterHandler
    logger.info("✅ 使用真实F2项目")
except ImportError:
    logger.error("❌ F2项目未正确安装")
    raise ImportError("请确保F2项目已正确安装: pip install -e /tmp/F2_correct")'''
            
            # 替换导入部分
            lines = content.split('\n')
            in_import_block = False
            new_lines = []
            
            for line in lines:
                if line.strip().startswith('try:') and 'f2.apps.twitter.handler' in content[content.find(line):content.find(line)+200]:
                    in_import_block = True
                    new_lines.extend(new_import.split('\n'))
                elif in_import_block and line.strip().startswith('raise ImportError'):
                    in_import_block = False
                    continue
                elif not in_import_block:
                    new_lines.append(line)
            
            # 写回文件
            client_file.write_text('\n'.join(new_lines), encoding='utf-8')
            print("✅ 客户端已更新为使用真实F2")
        else:
            print("ℹ️ 客户端已经配置为使用真实F2")
    else:
        print("❌ 客户端文件不存在")

def main():
    """主函数"""
    print("🐦 真实Twitter数据获取配置工具")
    print("=" * 60)
    
    # 1. 检查F2安装
    if not check_f2_installation():
        print("\n❌ F2项目未正确安装，请先运行:")
        print("cd /tmp/F2_correct && pip install -e .")
        return
    
    print()
    
    # 2. 更新客户端
    update_client_for_real_f2()
    print()
    
    # 3. 创建真实示例
    create_real_twitter_example()
    print()
    
    # 4. 显示Cookie获取指南
    show_cookie_guide()
    
    print("📝 下一步操作:")
    print("=" * 30)
    print("1. 按照上述指南获取Twitter Cookie")
    print("2. 设置环境变量:")
    print("   export TWITTER_COOKIE='你的Cookie'")
    print("3. 运行真实Twitter示例:")
    print("   python examples/real_twitter_example.py")
    print("4. 或直接运行简单示例:")
    print("   python examples/simple_usage.py")

if __name__ == "__main__":
    main()
