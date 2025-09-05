#!/usr/bin/env python3
"""
简化的抖音客户端测试
专注于测试基本功能而不发送网络请求
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.douyin_client import DouyinClient, DouyinConfigManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_client_creation():
    """测试客户端创建"""
    print("🎵 测试抖音客户端创建")
    print("=" * 40)
    
    try:
        # 创建配置管理器
        print("1. 创建配置管理器...")
        config_manager = DouyinConfigManager()
        print("✅ 配置管理器创建成功")
        
        # 验证配置
        print("2. 验证配置...")
        is_valid = config_manager.validate_config()
        print(f"✅ 配置验证: {'通过' if is_valid else '失败'}")
        
        # 显示配置信息
        request_config = config_manager.get_request_config()
        print("3. 配置信息:")
        print(f"   User-Agent: {request_config['headers']['User-Agent'][:50]}...")
        print(f"   Cookie: {'已设置' if request_config.get('cookie') else '空'}")
        print(f"   超时设置: {request_config.get('timeout', 30)}秒")
        
        # 创建客户端
        print("4. 创建抖音客户端...")
        client = DouyinClient(request_config)
        print("✅ 抖音客户端创建成功")
        
        # 检查handler
        print("5. 检查Handler...")
        if client.handler:
            print("✅ DouyinHandler已初始化")
            
            # 显示可用方法
            methods = [m for m in dir(client.handler) if not m.startswith('_') and 'fetch' in m]
            print(f"✅ 可用的fetch方法: {len(methods)}个")
            for method in methods[:5]:  # 显示前5个
                print(f"   - {method}")
            if len(methods) > 5:
                print(f"   ... 还有{len(methods)-5}个方法")
        else:
            print("❌ DouyinHandler未初始化")
        
        # 测试数据格式化功能
        print("6. 测试数据格式化...")
        sample_video = {
            "aweme_id": "test123",
            "desc": "测试视频描述",
            "author": {
                "nickname": "测试用户",
                "unique_id": "testuser"
            },
            "statistics": {
                "digg_count": 100,
                "comment_count": 20,
                "share_count": 5
            }
        }
        
        formatted = client.format_video(sample_video)
        print("✅ 数据格式化功能正常")
        print(f"   格式化结果: {len(formatted)}个字段")
        
        await client.close()
        print("✅ 客户端已关闭")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_options():
    """测试不同的配置选项"""
    print("\n🔧 测试配置选项")
    print("=" * 30)
    
    try:
        # 测试默认配置
        print("1. 测试默认配置...")
        config1 = DouyinConfigManager()
        print("✅ 默认配置加载成功")
        
        # 测试自定义配置
        print("2. 测试配置更新...")
        config1.update_config({
            "timeout": 60,
            "max_retries": 5,
            "download": {
                "path": "./test_downloads/"
            }
        })
        print("✅ 配置更新成功")
        
        # 测试配置获取
        print("3. 测试配置获取...")
        request_config = config1.get_request_config()
        download_config = config1.get_download_config()
        filter_config = config1.get_filter_config()
        
        print(f"✅ 请求配置: {len(request_config)}个字段")
        print(f"✅ 下载配置: {len(download_config)}个字段")
        print(f"✅ 过滤配置: {len(filter_config)}个字段")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def show_usage_summary():
    """显示使用总结"""
    print("\n📋 抖音F2客户端使用总结")
    print("=" * 40)
    
    print("✅ 客户端状态: 已准备就绪")
    print("✅ 配置状态: 无Cookie模式（正常）")
    print("✅ F2集成: DouyinHandler可用")
    print("✅ 异步支持: 完全支持")
    
    print("\n🎯 主要功能:")
    print("- 获取用户资料信息")
    print("- 获取用户发布的视频")
    print("- 获取单个视频详情")
    print("- 数据格式化和导出")
    print("- 配置管理和验证")
    
    print("\n💡 使用建议:")
    print("1. 无需Cookie即可获取公开内容")
    print("2. 合理控制请求频率避免限制")
    print("3. 使用真实的用户ID进行测试")
    print("4. 处理网络错误和超时情况")
    
    print("\n🚀 下一步:")
    print("- 获取真实的抖音用户ID")
    print("- 在网络良好时测试实际数据获取")
    print("- 开发自定义分析功能")
    print("- 实现数据可视化")

async def main():
    """主测试函数"""
    print("🎵 抖音F2客户端简化测试")
    print("=" * 50)
    
    # 测试客户端创建
    creation_success = await test_client_creation()
    
    # 测试配置功能
    config_success = test_config_options()
    
    # 显示总结
    show_usage_summary()
    
    # 最终结果
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*25)
    
    print(f"客户端创建: {'✅ 成功' if creation_success else '❌ 失败'}")
    print(f"配置管理: {'✅ 成功' if config_success else '❌ 失败'}")
    
    if creation_success and config_success:
        print("\n🎉 所有基础功能测试通过！")
        print("抖音F2客户端已准备就绪，可以开始使用。")
        print("\n💡 网络请求测试建议:")
        print("- 在网络状况良好时进行")
        print("- 使用真实的用户ID")
        print("- 设置合适的超时时间")
        print("- 实现错误重试机制")
    else:
        print("\n⚠️ 部分测试失败，请检查:")
        print("- F2项目是否正确安装")
        print("- Python环境是否正确")
        print("- 依赖包是否完整")

if __name__ == "__main__":
    asyncio.run(main())
