#!/usr/bin/env python3
"""
抖音客户端演示 - 包含模拟数据
当真实API返回空数据时，使用模拟数据进行演示
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.douyin_client import DouyinClient, DouyinConfigManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_mock_video_data():
    """创建模拟的抖音视频数据"""
    return [
        {
            "aweme_id": "7300000000000000001",
            "desc": "这是一个模拟的抖音视频，展示了美食制作过程 #美食 #烹饪 #生活",
            "author": {
                "unique_id": "foodlover123",
                "nickname": "美食达人小王",
                "avatar_larger": {
                    "url_list": ["https://example.com/avatar1.jpg"]
                },
                "follower_count": 150000,
                "following_count": 500,
                "total_favorited": 2500000
            },
            "create_time": 1701234567,
            "statistics": {
                "digg_count": 12500,
                "comment_count": 350,
                "share_count": 280,
                "play_count": 85000
            },
            "video": {
                "play_addr": {"url_list": ["https://example.com/video1.mp4"]},
                "cover": {"url_list": ["https://example.com/cover1.jpg"]},
                "duration": 45,
                "width": 720,
                "height": 1280
            },
            "music": {
                "title": "轻快的背景音乐",
                "author": "音乐制作人",
                "play_url": {"url_list": ["https://example.com/music1.mp3"]}
            },
            "text_extra": [
                {"hashtag_name": "美食", "type": 1},
                {"hashtag_name": "烹饪", "type": 1},
                {"hashtag_name": "生活", "type": 1}
            ]
        },
        {
            "aweme_id": "7300000000000000002", 
            "desc": "旅行vlog：探索神秘的古镇，发现隐藏的美景 #旅行 #vlog #古镇",
            "author": {
                "unique_id": "traveler_mike",
                "nickname": "旅行者Mike",
                "avatar_larger": {
                    "url_list": ["https://example.com/avatar2.jpg"]
                },
                "follower_count": 89000,
                "following_count": 200,
                "total_favorited": 1200000
            },
            "create_time": 1701220000,
            "statistics": {
                "digg_count": 8900,
                "comment_count": 245,
                "share_count": 156,
                "play_count": 42000
            },
            "video": {
                "play_addr": {"url_list": ["https://example.com/video2.mp4"]},
                "cover": {"url_list": ["https://example.com/cover2.jpg"]},
                "duration": 120,
                "width": 720,
                "height": 1280
            },
            "music": {
                "title": "民谣风格音乐",
                "author": "独立音乐人",
                "play_url": {"url_list": ["https://example.com/music2.mp3"]}
            },
            "text_extra": [
                {"hashtag_name": "旅行", "type": 1},
                {"hashtag_name": "vlog", "type": 1},
                {"hashtag_name": "古镇", "type": 1}
            ]
        },
        {
            "aweme_id": "7300000000000000003",
            "desc": "科技分享：最新AI工具使用心得，效率提升100% #科技 #AI #效率",
            "author": {
                "unique_id": "tech_guru",
                "nickname": "科技极客",
                "avatar_larger": {
                    "url_list": ["https://example.com/avatar3.jpg"]
                },
                "follower_count": 320000,
                "following_count": 1200,
                "total_favorited": 5800000
            },
            "create_time": 1701200000,
            "statistics": {
                "digg_count": 25600,
                "comment_count": 890,
                "share_count": 1200,
                "play_count": 156000
            },
            "video": {
                "play_addr": {"url_list": ["https://example.com/video3.mp4"]},
                "cover": {"url_list": ["https://example.com/cover3.jpg"]},
                "duration": 180,
                "width": 720,
                "height": 1280
            },
            "music": {
                "title": "电子音乐",
                "author": "电音制作人",
                "play_url": {"url_list": ["https://example.com/music3.mp3"]}
            },
            "text_extra": [
                {"hashtag_name": "科技", "type": 1},
                {"hashtag_name": "AI", "type": 1},
                {"hashtag_name": "效率", "type": 1}
            ]
        }
    ]

def create_mock_user_profile():
    """创建模拟的用户资料"""
    return {
        "unique_id": "demo_user_2024",
        "nickname": "抖音演示用户",
        "avatar_larger": {
            "url_list": ["https://example.com/demo_avatar.jpg"]
        },
        "follower_count": 125000,
        "following_count": 800,
        "total_favorited": 3200000,
        "aweme_count": 156,
        "signature": "分享生活中的美好瞬间 ✨",
        "verify_info": "认证用户",
        "region": "中国",
        "city": "北京"
    }

async def demo_with_fallback():
    """带有后备方案的抖音客户端演示"""
    print("🎵 抖音F2客户端完整演示")
    print("=" * 50)
    
    try:
        # 创建客户端
        config_manager = DouyinConfigManager()
        client = DouyinClient(config_manager.get_request_config())
        print("✅ 抖音客户端创建成功")
        
        test_user_id = "MS4wLjABAAAAssihLDGWRZQW6LPBR9aTi5UTO-vgXikwTObIvrMCz_Q"
        
        print(f"\n🔍 尝试获取真实数据...")
        
        # 尝试获取真实数据
        try:
            videos_task = asyncio.create_task(client.fetch_user_videos(test_user_id, max_videos=3))
            real_videos = await asyncio.wait_for(videos_task, timeout=15)
            
            # 检查是否获取到有效数据
            valid_videos = []
            for video in real_videos:
                if isinstance(video, dict) and video.get("aweme_id") != "unknown":
                    valid_videos.append(video)
            
            if valid_videos:
                print(f"✅ 获取到 {len(valid_videos)} 个真实视频")
                videos_to_use = valid_videos
                data_source = "真实API"
            else:
                print("⚠️ 真实API返回空数据，使用模拟数据演示")
                videos_to_use = create_mock_video_data()
                data_source = "模拟数据"
                
        except asyncio.TimeoutError:
            print("⏰ 真实API请求超时，使用模拟数据演示")
            videos_to_use = create_mock_video_data()
            data_source = "模拟数据"
        except Exception as e:
            print(f"❌ 真实API请求失败: {e}")
            print("使用模拟数据进行演示")
            videos_to_use = create_mock_video_data()
            data_source = "模拟数据"
        
        # 获取用户资料（尝试真实数据，失败则使用模拟）
        try:
            profile_task = asyncio.create_task(client.fetch_user_profile(test_user_id))
            profile = await asyncio.wait_for(profile_task, timeout=10)
            
            if not profile or not profile.get("nickname"):
                profile = create_mock_user_profile()
                profile_source = "模拟数据"
            else:
                profile_source = "真实API"
        except:
            profile = create_mock_user_profile()
            profile_source = "模拟数据"
        
        # 展示结果
        print(f"\n👤 用户资料 ({profile_source}):")
        print(f"   昵称: {profile.get('nickname', 'N/A')}")
        print(f"   抖音号: {profile.get('unique_id', 'N/A')}")
        print(f"   粉丝数: {profile.get('follower_count', 0):,}")
        print(f"   获赞数: {profile.get('total_favorited', 0):,}")
        print(f"   作品数: {profile.get('aweme_count', 0)}")
        
        print(f"\n🎬 视频列表 ({data_source}):")
        print("=" * 40)
        
        total_likes = 0
        total_comments = 0
        total_shares = 0
        
        for i, video in enumerate(videos_to_use, 1):
            formatted = client.format_video(video)
            
            print(f"\n📹 视频 {i}:")
            print(f"   标题: {formatted['desc'][:60]}...")
            print(f"   作者: {formatted['author']['nickname']}")
            print(f"   时长: {formatted['video']['duration']}秒")
            print(f"   点赞: {formatted['statistics']['digg_count']:,}")
            print(f"   评论: {formatted['statistics']['comment_count']:,}")
            print(f"   分享: {formatted['statistics']['share_count']:,}")
            print(f"   播放: {formatted['statistics']['play_count']:,}")
            
            if formatted['hashtags']:
                hashtags_str = " ".join([f"#{tag}" for tag in formatted['hashtags']])
                print(f"   标签: {hashtags_str}")
            
            print(f"   链接: {formatted['url']}")
            
            total_likes += formatted['statistics']['digg_count']
            total_comments += formatted['statistics']['comment_count']
            total_shares += formatted['statistics']['share_count']
        
        # 数据分析
        print(f"\n📊 数据分析:")
        print("=" * 20)
        print(f"总视频数: {len(videos_to_use)}")
        print(f"总点赞数: {total_likes:,}")
        print(f"总评论数: {total_comments:,}")
        print(f"总分享数: {total_shares:,}")
        print(f"平均点赞数: {total_likes // len(videos_to_use):,}")
        print(f"平均互动率: {((total_likes + total_comments + total_shares) / len(videos_to_use)):,.0f}")
        
        # 导出数据演示
        export_data = {
            "export_time": datetime.now().isoformat(),
            "data_source": data_source,
            "profile_source": profile_source,
            "user_profile": profile,
            "videos": [client.format_video(v) for v in videos_to_use],
            "statistics": {
                "total_videos": len(videos_to_use),
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_shares": total_shares
            }
        }
        
        export_file = "douyin_demo_export.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 演示数据已导出到: {export_file}")
        print(f"📄 文件大小: {Path(export_file).stat().st_size} 字节")
        
        await client.close()
        
        print(f"\n🎉 演示完成！")
        print(f"数据来源: {data_source}")
        print(f"用户资料来源: {profile_source}")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()

def show_usage_summary():
    """显示使用总结"""
    print(f"\n💡 使用总结")
    print("=" * 20)
    
    print("✅ 已验证功能:")
    print("- 客户端创建和配置")
    print("- 数据格式化和处理")
    print("- 错误处理和超时控制")
    print("- 模拟数据后备方案")
    print("- JSON数据导出")
    
    print("\n⚠️ 当前限制:")
    print("- 真实API可能返回空数据（需要有效Cookie）")
    print("- 网络请求可能超时")
    print("- 部分用户可能无法访问")
    
    print("\n🚀 改进建议:")
    print("- 获取真实的抖音Cookie")
    print("- 使用有效的用户ID进行测试")
    print("- 实现更智能的重试机制")
    print("- 添加更多的数据分析功能")

async def main():
    """主函数"""
    await demo_with_fallback()
    show_usage_summary()

if __name__ == "__main__":
    asyncio.run(main())
