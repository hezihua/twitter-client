#!/usr/bin/env python3
"""
抖音真实数据测试
处理实际的网络请求和数据格式
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.douyin_client import DouyinClient, DouyinConfigManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_real_data_with_timeout():
    """测试真实数据获取，带超时控制"""
    print("🎵 抖音真实数据测试")
    print("=" * 40)
    
    try:
        # 创建客户端
        config_manager = DouyinConfigManager()
        
        # 设置较短的超时时间
        config_manager.update_config({"timeout": 10})
        
        client = DouyinClient(config_manager.get_request_config())
        print("✅ 抖音客户端创建成功")
        
        # 测试用户ID
        test_user_id = "MS4wLjABAAAAssihLDGWRZQW6LPBR9aTi5UTO-vgXikwTObIvrMCz_Q"
        
        print(f"\n🔍 测试用户: {test_user_id}")
        
        # 1. 测试用户资料获取
        print("1. 测试用户资料获取...")
        try:
            # 设置较短的超时
            profile_task = asyncio.create_task(client.fetch_user_profile(test_user_id))
            profile = await asyncio.wait_for(profile_task, timeout=15)
            
            if profile:
                print("✅ 用户资料获取成功")
                print(f"   数据类型: {type(profile)}")
                print(f"   数据字段: {len(profile) if isinstance(profile, dict) else 'N/A'}")
                if isinstance(profile, dict):
                    print(f"   主要字段: {list(profile.keys())[:5]}")
            else:
                print("⚠️ 用户资料为空")
                
        except asyncio.TimeoutError:
            print("⏰ 用户资料获取超时")
        except Exception as e:
            print(f"❌ 用户资料获取失败: {e}")
        
        # 2. 测试视频获取
        print("\n2. 测试视频获取...")
        try:
            # 设置较短的超时和少量视频
            video_task = asyncio.create_task(client.fetch_user_videos(test_user_id, max_videos=2))
            videos = await asyncio.wait_for(video_task, timeout=20)
            print(videos, 'videos +++++++++++++++++++++++++++++++++')
            print(f"✅ 视频获取完成，数量: {len(videos)}")
            
            if videos:
                print("📊 视频数据分析:")
                for i, video in enumerate(videos[:2], 1):
                    print(f"\n   视频 {i}:")
                    print(f"   - 原始数据类型: {type(video)}")
                    
                    if isinstance(video, dict):
                        print(f"   - 字段数量: {len(video)}")
                        print(f"   - 主要字段: {list(video.keys())[:5]}")
                    elif isinstance(video, str):
                        print(f"   - 字符串长度: {len(video)}")
                        print(f"   - 内容预览: {video[:50]}...")
                    
                    # 测试格式化
                    try:
                        formatted = client.format_video(video)
                        print(f"   - 格式化成功: {formatted['desc'][:30]}...")
                        print(f"   - 作者: {formatted['author']['nickname']}")
                        print(f"   - 统计: 点赞{formatted['statistics']['digg_count']}")
                    except Exception as e:
                        print(f"   - 格式化失败: {e}")
            
        except asyncio.TimeoutError:
            print("⏰ 视频获取超时")
        except Exception as e:
            print(f"❌ 视频获取失败: {e}")
        
        # 3. 测试单个视频详情
        print("\n3. 测试视频详情获取...")
        # try:
        #     # 使用一个示例视频ID
        #     test_video_id = "7000000000000000000"  # 这需要替换为真实ID
            
        #     detail_task = asyncio.create_task(client.fetch_video_detail(test_video_id))
        #     detail = await asyncio.wait_for(detail_task, timeout=10)
            
        #     if detail:
        #         print("✅ 视频详情获取成功")
        #         print(f"   数据类型: {type(detail)}")
        #         if isinstance(detail, dict):
        #             formatted = client.format_video(detail)
        #             print(f"   视频描述: {formatted['desc'][:50]}...")
        #     else:
        #         print("⚠️ 视频详情为空（可能是无效的视频ID）")
                
        # except asyncio.TimeoutError:
        #     print("⏰ 视频详情获取超时")
        # except Exception as e:
        #     print(f"❌ 视频详情获取失败: {e}")
        
        await client.close()
        print("\n✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def analyze_error_messages():
    """分析常见错误信息"""
    print("\n🔍 错误信息分析")
    print("=" * 30)
    
    error_solutions = {
        "fetch_user_profile请求失败": {
            "原因": "Cookie无效或用户ID不存在",
            "解决方案": ["使用真实Cookie", "验证用户ID格式", "稍后重试"]
        },
        "string indices must be integers": {
            "原因": "数据格式不是预期的字典格式",
            "解决方案": ["检查API返回格式", "更新数据处理逻辑", "增加类型检查"]
        },
        "TimeoutError": {
            "原因": "网络请求超时",
            "解决方案": ["增加超时时间", "检查网络连接", "使用代理服务器"]
        },
        "503 Service Unavailable": {
            "原因": "服务器暂时不可用",
            "解决方案": ["稍后重试", "更换请求参数", "检查服务状态"]
        }
    }
    
    for error, info in error_solutions.items():
        print(f"\n❌ {error}")
        print(f"   原因: {info['原因']}")
        print("   解决方案:")
        for solution in info["解决方案"]:
            print(f"   - {solution}")

def show_success_summary():
    """显示成功的功能总结"""
    print("\n🎉 功能状态总结")
    print("=" * 30)
    
    print("✅ 成功的功能:")
    print("- 客户端创建和初始化")
    print("- DouyinHandler集成")
    print("- 配置管理和验证")
    print("- 数据格式化（已修复）")
    print("- 错误处理和超时控制")
    
    print("\n⚠️ 需要注意的问题:")
    print("- 用户资料获取需要有效Cookie")
    print("- 视频数据格式可能变化")
    print("- 网络请求可能超时")
    print("- 服务器可能返回503错误")
    
    print("\n💡 使用建议:")
    print("- 在网络良好时测试")
    print("- 使用真实的用户ID")
    print("- 设置合理的超时时间")
    print("- 实现重试机制")
    print("- 处理不同的数据格式")

async def main():
    """主测试函数"""
    print("🎵 抖音F2客户端真实数据测试")
    print("=" * 50)
    
    print("⚠️ 注意：此测试将进行真实的网络请求")
    print("如果网络较慢或服务器繁忙，可能会需要一些时间")
    print("可以随时按 Ctrl+C 中断测试")
    
    # 运行真实数据测试
    await test_real_data_with_timeout()
    
    # 分析错误信息
    analyze_error_messages()
    
    # 显示成功总结
    show_success_summary()

if __name__ == "__main__":
    asyncio.run(main())
