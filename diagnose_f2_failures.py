#!/usr/bin/env python3
"""
F2爬虫失败诊断工具
系统性分析和解决F2爬虫问题
"""

import asyncio
import os
import sys
import json
import time
import socket
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

async def test_network_connectivity():
    """测试网络连接"""
    print("🌐 网络连接测试")
    print("=" * 30)
    
    # 测试基本网络连接
    test_hosts = [
        ("www.douyin.com", 80),
        ("www.douyin.com", 443),
        ("8.8.8.8", 53),  # Google DNS
    ]
    
    for host, port in test_hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ {host}:{port} - 连接成功")
            else:
                print(f"❌ {host}:{port} - 连接失败")
        except Exception as e:
            print(f"❌ {host}:{port} - 异常: {e}")
    
    # 测试DNS解析
    try:
        import socket
        ip = socket.gethostbyname("www.douyin.com")
        print(f"✅ DNS解析: www.douyin.com -> {ip}")
    except Exception as e:
        print(f"❌ DNS解析失败: {e}")

def analyze_cookie_quality():
    """分析Cookie质量"""
    print("\n🍪 Cookie质量分析")
    print("=" * 30)
    
    cookie = os.getenv("DOUYIN_COOKIE", "")
    
    if not cookie:
        print("❌ 未设置DOUYIN_COOKIE环境变量")
        return False
    
    print(f"📏 Cookie长度: {len(cookie)} 字符")
    
    # 分析Cookie组件
    if ';' in cookie:
        parts = [p.strip() for p in cookie.split(';') if p.strip()]
        print(f"🔧 Cookie组件数: {len(parts)}")
        
        # 检查关键字段
        key_fields = ['sessionid', 'sid_guard', 'uid_tt', 'sid_tt', 'ssid_ucp_v1']
        found_fields = []
        
        for part in parts:
            if '=' in part:
                key = part.split('=')[0].strip()
                if key in key_fields:
                    found_fields.append(key)
        
        print(f"🔑 关键字段: {found_fields}")
        
        if len(found_fields) >= 2:
            print("✅ Cookie质量: 良好")
            return True
        else:
            print("⚠️ Cookie质量: 可能不足")
            return False
    else:
        print("⚠️ Cookie格式异常")
        return False

async def test_f2_basic_functionality():
    """测试F2基本功能"""
    print("\n🕷️ F2基本功能测试")
    print("=" * 30)
    
    try:
        from f2.apps.douyin.handler import DouyinHandler
        print("✅ DouyinHandler导入成功")
        
        # 测试Handler创建
        config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15"
            },
            "cookie": os.getenv("DOUYIN_COOKIE", ""),
            "proxies": {"http://": None, "https://": None}
        }
        
        handler = DouyinHandler(config)
        print("✅ DouyinHandler创建成功")
        
        # 测试网络请求（短超时）
        print("🔍 测试网络请求能力...")
        
        test_user = "MS4wLjABAAAAssihLDGWRZQW6LPBR9aTi5UTO-vgXikwTObIvrMCz_Q"
        
        try:
            # 设置短超时测试
            start_time = time.time()
            
            async def test_request():
                async for data in handler.fetch_user_post_videos(
                    sec_user_id=test_user,
                    max_counts=1,
                    page_counts=1
                ):
                    return data
            
            result = await asyncio.wait_for(test_request(), timeout=10)
            elapsed = time.time() - start_time
            
            print(f"✅ 网络请求成功 (耗时: {elapsed:.1f}秒)")
            
            # 分析返回数据
            try:
                data = result._to_dict()
                print(f"📊 数据类型: {type(data)}")
                print(f"📊 数据长度: {len(data) if hasattr(data, '__len__') else 'N/A'}")
                
                if isinstance(data, list) and data and isinstance(data[0], str):
                    print("⚠️ 返回字段名列表 - 可能是空响应")
                    return False
                else:
                    print("✅ 数据格式正常")
                    return True
                    
            except Exception as e:
                print(f"❌ 数据解析失败: {e}")
                return False
                
        except asyncio.TimeoutError:
            print("⏰ 网络请求超时")
            return False
        except Exception as e:
            print(f"❌ 网络请求失败: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ F2导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ F2测试失败: {e}")
        return False

def analyze_common_errors():
    """分析常见错误模式"""
    print("\n🔍 常见错误模式分析")
    print("=" * 30)
    
    error_patterns = {
        "403 Forbidden": {
            "可能原因": ["Cookie无效", "请求频率过高", "IP被限制", "User-Agent被识别"],
            "解决方案": ["更新Cookie", "降低请求频率", "使用代理", "更换User-Agent"]
        },
        "响应内容为空": {
            "可能原因": ["用户不存在", "内容被限制", "网络问题", "服务器问题"],
            "解决方案": ["验证用户ID", "检查网络连接", "稍后重试", "使用不同用户测试"]
        },
        "字段名列表": {
            "可能原因": ["API返回空数据", "解析逻辑问题", "Cookie权限不足"],
            "解决方案": ["使用有效Cookie", "检查用户权限", "实现数据验证"]
        },
        "超时错误": {
            "可能原因": ["网络延迟", "服务器响应慢", "请求参数问题"],
            "解决方案": ["增加超时时间", "优化网络环境", "检查请求参数"]
        }
    }
    
    for error, info in error_patterns.items():
        print(f"\n❌ {error}")
        print(f"   可能原因: {', '.join(info['可能原因'])}")
        print(f"   解决方案: {', '.join(info['解决方案'])}")

def provide_optimization_suggestions():
    """提供优化建议"""
    print("\n💡 优化建议")
    print("=" * 20)
    
    suggestions = [
        "🍪 定期更新Cookie（建议每2-3天）",
        "⏱️ 合理设置请求间隔（建议2-5秒）",
        "🔄 实现智能重试机制",
        "📱 使用移动端User-Agent",
        "🌐 考虑使用代理服务器",
        "📊 实现数据验证和后备方案",
        "🔍 监控请求成功率",
        "⚙️ 根据网络环境调整配置"
    ]
    
    for suggestion in suggestions:
        print(f"  {suggestion}")

async def comprehensive_diagnosis():
    """综合诊断"""
    print("🔧 F2爬虫失败综合诊断")
    print("=" * 50)
    
    # 1. 网络连接测试
    await test_network_connectivity()
    
    # 2. Cookie质量分析
    cookie_ok = analyze_cookie_quality()
    
    # 3. F2功能测试
    f2_ok = await test_f2_basic_functionality()
    
    # 4. 错误分析
    analyze_common_errors()
    
    # 5. 优化建议
    provide_optimization_suggestions()
    
    # 6. 总结
    print("\n" + "="*50)
    print("📊 诊断结果总结")
    print("="*25)
    
    print(f"Cookie状态: {'✅ 正常' if cookie_ok else '❌ 异常'}")
    print(f"F2功能状态: {'✅ 正常' if f2_ok else '❌ 异常'}")
    
    if cookie_ok and f2_ok:
        print("\n🎉 基础功能正常！")
        print("如果仍然遇到问题，可能是:")
        print("- 目标用户的内容受限")
        print("- 临时的网络或服务器问题")
        print("- 需要进一步的配置优化")
    else:
        print("\n⚠️ 发现问题，建议:")
        if not cookie_ok:
            print("1. 🍪 重新获取有效的Cookie")
        if not f2_ok:
            print("2. 🔧 检查F2配置和网络环境")
        print("3. 📖 参考故障排除指南")

if __name__ == "__main__":
    asyncio.run(comprehensive_diagnosis())
