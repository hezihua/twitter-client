#!/usr/bin/env python3
"""
抖音客户端基本使用示例
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.douyin_client import DouyinClient, DouyinConfigManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def basic_douyin_example():
    """基本的抖音视频获取示例"""
    print("🎵 抖音客户端基本使用示例")
    print("=" * 50)
    
    try:
        # 创建配置管理器
        config_manager = DouyinConfigManager()
        
        # 验证配置
        if not config_manager.validate_config():
            print("❌ 配置验证失败")
            return
        
        # 创建抖音客户端
        client = DouyinClient(config_manager.get_request_config())
        print("✅ 抖音客户端创建成功")
        
        # 测试用户（这里使用一些知名的抖音账号ID作为示例）
        test_users = [
            "MS4wLjABAAAANwkJuWIRFOzg5uCpGgC5Ac2h_bgVVFlo9wUL2vhTW8E",  # 示例用户ID
            "MS4wLjABAAAAv7iSuuXDdUDdaJrFQx-QYPOsGrFSKi1gNdZhqaQkPDA"   # 示例用户ID
        ]
        
        for user_id in test_users[:1]:  # 只测试第一个用户
            print(f"\n🔍 获取用户视频: {user_id}")
            
            try:
                # 获取用户资料
                print("📋 获取用户资料...")
                user_profile = await client.fetch_user_profile(user_id)
                
                if user_profile:
                    print(f"👤 用户名: {user_profile.get('nickname', 'N/A')}")
                    print(f"🆔 抖音号: {user_profile.get('unique_id', 'N/A')}")
                    print(f"👥 粉丝数: {user_profile.get('follower_count', 0)}")
                    print(f"❤️ 获赞数: {user_profile.get('total_favorited', 0)}")
                    print(f"🎬 作品数: {user_profile.get('aweme_count', 0)}")
                
                # 获取用户视频
                print("\n🎬 获取用户视频...")
                videos = await client.fetch_user_videos(user_id, max_videos=5)
                
                print(f"📊 获取到 {len(videos)} 个视频")
                
                # 显示视频信息
                for i, video in enumerate(videos, 1):
                    formatted_video = client.format_video(video)
                    print(f"\n🎥 视频 {i}:")
                    print(f"   标题: {formatted_video['desc'][:50]}...")
                    print(f"   作者: {formatted_video['author']['nickname']}")
                    print(f"   点赞: {formatted_video['statistics']['digg_count']}")
                    print(f"   评论: {formatted_video['statistics']['comment_count']}")
                    print(f"   分享: {formatted_video['statistics']['share_count']}")
                    print(f"   时长: {formatted_video['video']['duration']}秒")
                    print(f"   链接: {formatted_video['url']}")
                
            except Exception as e:
                print(f"❌ 获取用户 {user_id} 的数据失败: {e}")
                continue
        
        # 关闭客户端
        await client.close()
        print("\n✅ 示例执行完成")
        
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        import traceback
        traceback.print_exc()

async def video_detail_example():
    """获取单个视频详情示例"""
    print("\n🎬 单个视频详情获取示例")
    print("=" * 40)
    
    try:
        config_manager = DouyinConfigManager()
        client = DouyinClient(config_manager.get_request_config())
        
        # 示例视频ID（需要替换为真实的视频ID）
        test_aweme_id = "7000000000000000000"
        
        print(f"🔍 获取视频详情: {test_aweme_id}")
        
        video_detail = await client.fetch_video_detail(test_aweme_id)
        
        if video_detail:
            formatted_video = client.format_video(video_detail)
            print("✅ 视频详情获取成功:")
            print(f"   标题: {formatted_video['desc']}")
            print(f"   作者: {formatted_video['author']['nickname']}")
            print(f"   播放: {formatted_video['statistics']['play_count']}")
            print(f"   点赞: {formatted_video['statistics']['digg_count']}")
            print(f"   视频尺寸: {formatted_video['video']['width']}x{formatted_video['video']['height']}")
            print(f"   音乐: {formatted_video['music']['title']}")
        else:
            print("❌ 未获取到视频详情")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 视频详情获取失败: {e}")

def show_config_guide():
    """显示配置指南"""
    print("\n📋 抖音配置指南")
    print("=" * 30)
    
    print("1. 环境变量配置 (.env文件):")
    print("   DOUYIN_COOKIE=你的抖音Cookie")
    print("   DOUYIN_DOWNLOAD_PATH=./downloads/douyin/")
    print("   HTTP_PROXY=http://proxy:8080  # 可选")
    print("   HTTPS_PROXY=http://proxy:8080  # 可选")
    
    print("\n2. 获取抖音Cookie:")
    print("   - 打开浏览器，访问 https://www.douyin.com")
    print("   - 登录你的抖音账户")
    print("   - 按F12打开开发者工具")
    print("   - 点击Network标签，刷新页面")
    print("   - 找到任一请求，复制Cookie请求头")
    
    print("\n3. 获取用户ID:")
    print("   - 访问用户主页")
    print("   - 查看页面源代码或网络请求")
    print("   - 找到sec_user_id参数")
    
    print("\n4. 注意事项:")
    print("   - Cookie需要定期更新")
    print("   - 请遵守抖音的使用条款")
    print("   - 合理控制请求频率")

async def main():
    """主函数"""
    print("🎵 抖音F2客户端演示")
    print("=" * 60)
    
    # 显示配置指南
    show_config_guide()
    
    # 检查Cookie配置（可以为空）
    douyin_cookie = os.getenv("DOUYIN_COOKIE", "")
    if not douyin_cookie:
        print("\n✅ 检测到无Cookie模式")
        print("将使用公开API访问抖音内容")
        print("这是完全正常的配置，无需Cookie即可获取公开数据")
    else:
        print(f"\n✅ 检测到Cookie配置 (长度: {len(douyin_cookie)} 字符)")
    
    print(f"\n✅ 检测到Cookie配置 (长度: {len(douyin_cookie)} 字符)")
    
    # 运行基本示例
    await basic_douyin_example()
    
    # 可选：运行视频详情示例
    # await video_detail_example()

if __name__ == "__main__":
    asyncio.run(main())
