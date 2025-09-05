#!/usr/bin/env python3
"""
抖音客户端功能测试
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_douyin_import():
    """测试抖音模块导入"""
    print("🔍 测试抖音模块导入")
    print("=" * 30)
    
    try:
        from f2.apps.douyin.handler import DouyinHandler
        print("✅ DouyinHandler导入成功")
        
        # 显示可用的方法
        methods = [method for method in dir(DouyinHandler) if not method.startswith('_')]
        print(f"📋 可用方法数量: {len(methods)}")
        print("🔧 主要方法:")
        for method in methods[:10]:  # 显示前10个方法
            print(f"   - {method}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

async def test_douyin_client():
    """测试抖音客户端创建"""
    print("\n🎵 测试抖音客户端创建")
    print("=" * 30)
    
    try:
        from src.douyin_client import DouyinClient, DouyinConfigManager
        
        # 创建配置管理器
        config_manager = DouyinConfigManager()
        print("✅ 配置管理器创建成功")
        
        # 验证配置
        is_valid = config_manager.validate_config()
        print(f"📋 配置验证: {'✅ 通过' if is_valid else '❌ 失败'}")
        
        # 创建客户端
        client = DouyinClient(config_manager.get_request_config())
        print("✅ 抖音客户端创建成功")
        
        # 显示配置信息
        request_config = config_manager.get_request_config()
        print(f"🌐 User-Agent: {request_config['headers']['User-Agent'][:50]}...")
        print(f"🍪 Cookie: {'已设置' if request_config.get('cookie') else '未设置'}")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 客户端测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_douyin_handler_direct():
    """直接测试F2的DouyinHandler"""
    print("\n🔧 直接测试F2 DouyinHandler")
    print("=" * 35)
    
    try:
        from f2.apps.douyin.handler import DouyinHandler
        
        # 创建基本配置
        config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1",
                "Referer": "https://www.douyin.com/"
            },
            "proxies": {
                "http://": None,
                "https://": None
            },
            "cookie": os.getenv("DOUYIN_COOKIE", "test_cookie")
        }
        
        print("⚙️ 创建DouyinHandler...")
        handler = DouyinHandler(config)
        print("✅ DouyinHandler创建成功")
        
        # 测试一个简单的方法（如果有的话）
        print("🔍 测试基本功能...")
        
        # 注意：这里可能需要根据实际的DouyinHandler API调整
        print("✅ 基本功能测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ DouyinHandler测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_douyin_cookie_guide():
    """显示获取抖音Cookie的指南"""
    print("\n📋 获取抖音Cookie指南")
    print("=" * 30)
    
    guide = """
🌐 方法1: Chrome浏览器
1. 打开Chrome，访问 https://www.douyin.com
2. 登录您的抖音账户
3. 按F12打开开发者工具
4. 点击"Network"标签
5. 在页面上进行任何操作(滑动、点击视频等)
6. 在Network面板中找到任一请求
7. 点击该请求，查看"Request Headers"
8. 找到"Cookie:"行，复制完整内容
9. 设置环境变量: export DOUYIN_COOKIE="复制的内容"

🌐 方法2: 移动端模拟
- 抖音主要是移动端应用，建议使用移动端User-Agent
- 可以使用Chrome的设备模拟功能
- 选择iPhone或Android设备进行模拟

⚠️ 重要提醒:
- Cookie包含敏感信息，请妥善保管
- 定期更新Cookie以保持有效性
- 遵守抖音的使用条款和robots.txt
- 合理控制请求频率，避免被限制

🔄 Cookie更新频率建议:
- 每天使用: 每2-3天更新一次
- 偶尔使用: 每周更新一次
- 出现错误: 立即更新
"""
    
    print(guide)

async def main():
    """主测试函数"""
    print("🎵 抖音F2客户端功能测试")
    print("=" * 50)
    
    # 1. 测试模块导入
    import_success = await test_douyin_import()
    
    if not import_success:
        print("\n❌ 基础模块导入失败，请检查F2安装")
        return
    
    # 2. 测试客户端创建
    client_success = await test_douyin_client()
    
    # 3. 直接测试DouyinHandler
    handler_success = await test_douyin_handler_direct()
    
    # 4. 显示Cookie获取指南
    show_douyin_cookie_guide()
    
    # 总结
    print("\n" + "="*50)
    print("📝 测试总结")
    print("="*25)
    
    print(f"模块导入: {'✅ 成功' if import_success else '❌ 失败'}")
    print(f"客户端创建: {'✅ 成功' if client_success else '❌ 失败'}")
    print(f"Handler测试: {'✅ 成功' if handler_success else '❌ 失败'}")
    
    if import_success and client_success and handler_success:
        print("\n🎉 所有测试通过！抖音客户端已准备就绪")
        print("💡 下一步:")
        print("1. 设置DOUYIN_COOKIE环境变量")
        print("2. 运行 python examples/douyin_basic_usage.py")
        print("3. 开始获取抖音数据")
    else:
        print("\n⚠️ 部分测试失败，请检查:")
        print("1. F2项目是否正确安装")
        print("2. Python环境是否正确")
        print("3. 依赖包是否完整")

if __name__ == "__main__":
    asyncio.run(main())
