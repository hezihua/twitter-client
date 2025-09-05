#!/usr/bin/env python3
"""
Twitter 403错误诊断和解决方案
"""

import asyncio
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

def analyze_cookie_structure():
    """分析Cookie结构和有效性"""
    print("🔍 Cookie结构分析")
    print("=" * 30)
    
    cookie = os.getenv("TWITTER_COOKIE")
    if not cookie:
        print("❌ 未找到Cookie，请设置TWITTER_COOKIE环境变量")
        return False
    
    # 分析Cookie结构
    parts = [p.strip() for p in cookie.split(';') if p.strip()]
    print(f"📊 Cookie组件总数: {len(parts)}")
    print(f"📏 Cookie总长度: {len(cookie)} 字符")
    
    # 检查关键组件
    key_parts = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            key_parts[key.strip()] = value.strip()
    
    # Twitter关键认证字段
    critical_fields = {
        'auth_token': '用户认证令牌',
        'ct0': 'CSRF令牌', 
        'guest_id': '访客ID',
        'twid': '用户ID'
    }
    
    important_fields = {
        'personalization_id': '个性化ID',
        'guest_id_marketing': '营销访客ID',
        'guest_id_ads': '广告访客ID'
    }
    
    print("\n🔑 关键认证字段:")
    missing_critical = []
    for field, desc in critical_fields.items():
        if field in key_parts:
            value_len = len(key_parts[field])
            print(f"  ✅ {field} ({desc}): {value_len} 字符")
            
            # 检查字段格式
            if field == 'auth_token' and value_len != 40:
                print(f"    ⚠️ auth_token长度异常 (应为40字符)")
            elif field == 'ct0' and value_len < 100:
                print(f"    ⚠️ ct0长度可能异常 (通常>100字符)")
        else:
            print(f"  ❌ {field} ({desc}): 缺失")
            missing_critical.append(field)
    
    print("\n📋 其他重要字段:")
    for field, desc in important_fields.items():
        if field in key_parts:
            print(f"  ✅ {field} ({desc}): {len(key_parts[field])} 字符")
        else:
            print(f"  ⚠️ {field} ({desc}): 缺失")
    
    # 检查Cookie新鲜度
    print("\n⏰ Cookie时效性检查:")
    if 'auth_token' in key_parts:
        # 检查auth_token是否为空或默认值
        auth_token = key_parts['auth_token']
        if not auth_token or auth_token == '""' or len(auth_token) < 20:
            print("  ❌ auth_token无效或为空")
        else:
            print("  ✅ auth_token格式正常")
    
    return len(missing_critical) == 0

def get_403_solutions():
    """获取403错误的解决方案"""
    print("\n🔧 403错误解决方案")
    print("=" * 30)
    
    solutions = [
        {
            "title": "1. 更新Cookie (最重要)",
            "steps": [
                "打开浏览器，访问 https://x.com",
                "确保已登录Twitter账户",
                "按F12打开开发者工具",
                "转到Network标签页",
                "刷新页面或点击任意推文",
                "找到任一请求，复制Cookie请求头",
                "更新.env文件中的TWITTER_COOKIE"
            ]
        },
        {
            "title": "2. 检查账户状态",
            "steps": [
                "确保Twitter账户未被限制或封禁",
                "检查是否需要完成额外验证",
                "尝试在浏览器中正常浏览Twitter",
                "如果浏览器也无法访问，说明账户有问题"
            ]
        },
        {
            "title": "3. 更新请求头",
            "steps": [
                "使用最新的User-Agent",
                "确保Referer设置正确",
                "添加必要的安全头部",
                "检查Accept和Content-Type设置"
            ]
        },
        {
            "title": "4. 网络环境检查",
            "steps": [
                "检查是否被IP限制",
                "尝试使用代理服务器",
                "检查防火墙设置",
                "确认DNS解析正常"
            ]
        },
        {
            "title": "5. API限制应对",
            "steps": [
                "降低请求频率",
                "增加请求间隔",
                "使用不同的用户ID测试",
                "避免频繁的大量请求"
            ]
        }
    ]
    
    for solution in solutions:
        print(f"\n🎯 {solution['title']}")
        for i, step in enumerate(solution['steps'], 1):
            print(f"   {i}. {step}")
    
    return solutions

async def test_alternative_config():
    """测试替代配置"""
    print("\n🧪 测试替代配置")
    print("=" * 30)
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        
        cookie = os.getenv("TWITTER_COOKIE")
        if not cookie:
            print("❌ 未找到Cookie")
            return False
        
        # 尝试更保守的配置
        conservative_config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Cache-Control": "max-age=0",
            },
            "proxies": {
                "http://": None,
                "https://": None
            },
            "cookie": cookie
        }
        
        print("⚙️ 尝试保守配置...")
        handler = TwitterHandler(conservative_config)
        
        # 尝试访问Twitter官方账号（通常限制较少）
        test_users = ["Twitter", "support", "TwitterDev"]
        
        for user in test_users:
            print(f"\n🔍 测试用户: {user}")
            try:
                async for tweet_list in handler.fetch_post_tweet(
                    userId=user,
                    page_counts=1,
                    max_counts=1
                ):
                    print(f"✅ {user} - 请求成功!")
                    
                    try:
                        tweets = tweet_list._to_dict()
                        if tweets:
                            print(f"🎉 获取到 {len(tweets)} 条推文")
                            return True
                    except:
                        pass
                    
                    return True  # 至少请求成功了
                    
            except Exception as e:
                print(f"❌ {user} - 失败: {str(e)[:100]}")
                continue
        
        return False
        
    except ImportError:
        print("❌ F2模块导入失败")
        return False
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def create_fresh_cookie_guide():
    """创建获取新Cookie的详细指南"""
    print("\n📋 获取新Cookie详细指南")
    print("=" * 40)
    
    guide = """
🌐 方法1: Chrome浏览器
1. 打开Chrome，访问 https://x.com
2. 登录您的Twitter账户
3. 按F12打开开发者工具
4. 点击"Network"标签
5. 在页面上进行任何操作(点击推文、刷新等)
6. 在Network面板中找到任一请求
7. 点击该请求，查看"Request Headers"
8. 找到"Cookie:"行，复制完整内容
9. 更新.env文件

🌐 方法2: 使用扩展插件
1. 安装Cookie导出插件(如Cookie-Editor)
2. 访问 https://x.com 并登录
3. 使用插件导出Cookie
4. 复制Cookie字符串到.env文件

⚠️ 重要提醒:
- Cookie包含敏感信息，请妥善保管
- 定期更新Cookie以保持有效性
- 不要在公共场所或不安全的网络下操作
- 如果账户被限制，需要先解除限制

🔄 Cookie更新频率建议:
- 每天使用: 每2-3天更新一次
- 偶尔使用: 每周更新一次
- 出现403错误: 立即更新
"""
    
    print(guide)

async def main():
    """主诊断流程"""
    print("🩺 Twitter 403错误综合诊断")
    print("=" * 50)
    
    # 1. Cookie结构分析
    cookie_valid = analyze_cookie_structure()
    
    # 2. 获取解决方案
    get_403_solutions()
    
    # 3. 测试替代配置
    if cookie_valid:
        print("\n" + "="*50)
        alt_success = await test_alternative_config()
        if alt_success:
            print("\n🎉 替代配置测试成功!")
        else:
            print("\n💡 替代配置也失败，建议更新Cookie")
    
    # 4. 提供详细指南
    create_fresh_cookie_guide()
    
    # 5. 总结建议
    print("\n" + "="*50)
    print("📝 诊断总结与建议")
    print("="*25)
    
    if not cookie_valid:
        print("🔴 Cookie结构不完整，强烈建议重新获取Cookie")
    else:
        print("🟡 Cookie结构正常，但可能已过期或被限制")
    
    print("\n💡 推荐解决步骤:")
    print("1. 🔄 重新获取最新Cookie (最重要)")
    print("2. 🌐 确认网络环境正常")
    print("3. 👤 检查Twitter账户状态")
    print("4. ⏱️ 降低请求频率")
    print("5. 🔧 如仍失败，考虑使用模拟数据进行开发")

if __name__ == "__main__":
    asyncio.run(main())
