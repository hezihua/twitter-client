#!/usr/bin/env python3
"""
抖音高级功能演示
包含用户分析、热门视频筛选、数据导出等功能
"""

import asyncio
import json
import csv
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.douyin_client import DouyinClient, DouyinConfigManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DouyinAnalyzer:
    """抖音数据分析器"""
    
    def __init__(self, client: DouyinClient):
        self.client = client
        self.videos_data = []
        self.users_data = []
    
    async def analyze_user(self, user_id: str, max_videos: int = 50) -> Dict[str, Any]:
        """
        分析单个用户的数据
        
        Args:
            user_id: 用户ID
            max_videos: 最大分析视频数
            
        Returns:
            用户分析结果
        """
        print(f"🔍 分析用户: {user_id}")
        
        try:
            # 获取用户资料
            profile = await self.client.fetch_user_profile(user_id)
            if not profile:
                return {"error": "无法获取用户资料"}
            
            # 获取用户视频
            videos = await self.client.fetch_user_videos(user_id, max_videos=max_videos)
            
            if not videos:
                return {"error": "无法获取用户视频"}
            
            # 分析视频数据
            analysis = self._analyze_videos(videos)
            analysis.update({
                "user_profile": {
                    "nickname": profile.get('nickname', 'N/A'),
                    "unique_id": profile.get('unique_id', 'N/A'),
                    "follower_count": profile.get('follower_count', 0),
                    "following_count": profile.get('following_count', 0),
                    "total_favorited": profile.get('total_favorited', 0),
                    "aweme_count": profile.get('aweme_count', 0),
                },
                "videos_analyzed": len(videos),
                "user_id": user_id
            })
            
            # 保存数据
            self.users_data.append(analysis)
            self.videos_data.extend(videos)
            
            return analysis
            
        except Exception as e:
            print(f"❌ 分析用户失败: {e}")
            return {"error": str(e)}
    
    def _analyze_videos(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析视频数据"""
        if not videos:
            return {}
        
        # 基础统计
        total_likes = sum(v.get('statistics', {}).get('digg_count', 0) for v in videos)
        total_comments = sum(v.get('statistics', {}).get('comment_count', 0) for v in videos)
        total_shares = sum(v.get('statistics', {}).get('share_count', 0) for v in videos)
        total_plays = sum(v.get('statistics', {}).get('play_count', 0) for v in videos)
        
        durations = [v.get('video', {}).get('duration', 0) for v in videos if v.get('video', {}).get('duration', 0) > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # 互动率计算
        engagement_rates = []
        for video in videos:
            stats = video.get('statistics', {})
            plays = stats.get('play_count', 0)
            if plays > 0:
                engagement = (stats.get('digg_count', 0) + stats.get('comment_count', 0) + stats.get('share_count', 0)) / plays
                engagement_rates.append(engagement)
        
        avg_engagement_rate = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        
        # 热门视频（点赞数前10%）
        sorted_videos = sorted(videos, key=lambda x: x.get('statistics', {}).get('digg_count', 0), reverse=True)
        top_10_percent = max(1, len(sorted_videos) // 10)
        hot_videos = sorted_videos[:top_10_percent]
        
        # 话题标签分析
        hashtags = []
        for video in videos:
            text_extra = video.get('text_extra', [])
            for tag in text_extra:
                if tag.get('type') == 1:  # 话题标签
                    hashtags.append(tag.get('hashtag_name', ''))
        
        hashtag_counts = {}
        for tag in hashtags:
            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_videos": len(videos),
            "statistics": {
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_shares": total_shares,
                "total_plays": total_plays,
                "avg_likes": total_likes / len(videos),
                "avg_comments": total_comments / len(videos),
                "avg_shares": total_shares / len(videos),
                "avg_plays": total_plays / len(videos),
                "avg_duration": avg_duration,
                "avg_engagement_rate": avg_engagement_rate,
            },
            "hot_videos": [
                {
                    "aweme_id": v.get('aweme_id'),
                    "desc": v.get('desc', '')[:100],
                    "digg_count": v.get('statistics', {}).get('digg_count', 0),
                    "comment_count": v.get('statistics', {}).get('comment_count', 0),
                    "play_count": v.get('statistics', {}).get('play_count', 0),
                }
                for v in hot_videos[:5]  # 前5个热门视频
            ],
            "top_hashtags": top_hashtags,
            "content_analysis": {
                "short_videos": len([v for v in videos if v.get('video', {}).get('duration', 0) < 30]),
                "medium_videos": len([v for v in videos if 30 <= v.get('video', {}).get('duration', 0) < 60]),
                "long_videos": len([v for v in videos if v.get('video', {}).get('duration', 0) >= 60]),
            }
        }
    
    def export_to_json(self, filename: str = None):
        """导出数据到JSON文件"""
        if filename is None:
            filename = f"douyin_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "export_time": datetime.now().isoformat(),
            "summary": {
                "users_analyzed": len(self.users_data),
                "total_videos": len(self.videos_data),
            },
            "users_analysis": self.users_data,
            "raw_videos": self.videos_data[:100]  # 只保存前100个视频的原始数据
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 数据已导出到: {filename}")
        return filename
    
    def export_to_csv(self, filename: str = None):
        """导出视频数据到CSV文件"""
        if filename is None:
            filename = f"douyin_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not self.videos_data:
            print("❌ 没有视频数据可导出")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入表头
            headers = [
                '视频ID', '标题', '作者', '点赞数', '评论数', '分享数', '播放数',
                '视频时长', '创建时间', '链接'
            ]
            writer.writerow(headers)
            
            # 写入数据
            for video in self.videos_data:
                formatted = self.client.format_video(video)
                row = [
                    formatted.get('aweme_id', ''),
                    formatted.get('desc', ''),
                    formatted.get('author', {}).get('nickname', ''),
                    formatted.get('statistics', {}).get('digg_count', 0),
                    formatted.get('statistics', {}).get('comment_count', 0),
                    formatted.get('statistics', {}).get('share_count', 0),
                    formatted.get('statistics', {}).get('play_count', 0),
                    formatted.get('video', {}).get('duration', 0),
                    formatted.get('create_time', 0),
                    formatted.get('url', ''),
                ]
                writer.writerow(row)
        
        print(f"📊 CSV数据已导出到: {filename}")
        return filename

async def demo_user_analysis():
    """演示用户分析功能"""
    print("🎵 抖音用户分析演示")
    print("=" * 50)
    
    # 检查Cookie
    douyin_cookie = os.getenv("DOUYIN_COOKIE")
    if not douyin_cookie:
        print("⚠️ 未设置DOUYIN_COOKIE环境变量")
        print("这将使用模拟数据进行演示")
        # 这里可以设置一个测试Cookie或使用模拟数据
    
    try:
        # 创建客户端
        config_manager = DouyinConfigManager()
        client = DouyinClient(config_manager.get_request_config())
        
        # 创建分析器
        analyzer = DouyinAnalyzer(client)
        
        # 示例用户ID列表（需要替换为真实的用户ID）
        test_users = [
            "MS4wLjABAAAANwkJuWIRFOzg5uCpGgC5Ac2h_bgVVFlo9wUL2vhTW8E",  # 示例1
            "MS4wLjABAAAAv7iSuuXDdUDdaJrFQx-QYPOsGrFSKi1gNdZhqaQkPDA",  # 示例2
        ]
        
        print("📊 开始分析用户数据...")
        
        for user_id in test_users[:1]:  # 只分析第一个用户作为演示
            analysis = await analyzer.analyze_user(user_id, max_videos=20)
            
            if "error" in analysis:
                print(f"❌ 分析失败: {analysis['error']}")
                continue
            
            # 显示分析结果
            profile = analysis.get('user_profile', {})
            stats = analysis.get('statistics', {})
            
            print(f"\n👤 用户: {profile.get('nickname', 'N/A')}")
            print(f"🆔 抖音号: {profile.get('unique_id', 'N/A')}")
            print(f"👥 粉丝数: {profile.get('follower_count', 0):,}")
            print(f"❤️ 获赞总数: {profile.get('total_favorited', 0):,}")
            print(f"🎬 作品数: {profile.get('aweme_count', 0)}")
            
            print(f"\n📈 视频分析 (基于 {analysis.get('videos_analyzed', 0)} 个视频):")
            print(f"平均点赞数: {stats.get('avg_likes', 0):.0f}")
            print(f"平均评论数: {stats.get('avg_comments', 0):.0f}")
            print(f"平均播放数: {stats.get('avg_plays', 0):.0f}")
            print(f"平均时长: {stats.get('avg_duration', 0):.1f}秒")
            print(f"平均互动率: {stats.get('avg_engagement_rate', 0):.2%}")
            
            # 显示热门视频
            hot_videos = analysis.get('hot_videos', [])
            if hot_videos:
                print(f"\n🔥 热门视频 (前5个):")
                for i, video in enumerate(hot_videos, 1):
                    print(f"{i}. {video['desc'][:50]}...")
                    print(f"   点赞: {video['digg_count']:,} | 评论: {video['comment_count']:,}")
            
            # 显示热门话题
            top_hashtags = analysis.get('top_hashtags', [])
            if top_hashtags:
                print(f"\n#️⃣ 热门话题:")
                for tag, count in top_hashtags[:5]:
                    print(f"   #{tag}: {count}次")
        
        # 导出数据
        print(f"\n💾 导出分析数据...")
        json_file = analyzer.export_to_json()
        csv_file = analyzer.export_to_csv()
        
        print(f"✅ 分析完成！")
        print(f"📄 JSON报告: {json_file}")
        print(f"📊 CSV数据: {csv_file}")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()

async def demo_video_filtering():
    """演示视频过滤功能"""
    print("\n🎯 视频过滤演示")
    print("=" * 30)
    
    # 这里可以添加视频过滤的演示代码
    print("💡 过滤功能演示:")
    print("- 按点赞数过滤")
    print("- 按时长过滤") 
    print("- 按关键词过滤")
    print("- 按发布时间过滤")

def show_usage_tips():
    """显示使用技巧"""
    print("\n💡 使用技巧")
    print("=" * 20)
    
    tips = [
        "🔑 获取用户ID: 从用户主页的网络请求中查找sec_user_id",
        "⏱️ 控制频率: 在请求间添加延迟，避免被限制",
        "📱 移动端UA: 使用移动端User-Agent获得更好的兼容性",
        "🍪 Cookie管理: 定期更新Cookie以保持有效性",
        "💾 数据备份: 及时导出重要数据",
        "🔍 批量分析: 可以分析多个用户进行对比",
        "📊 数据可视化: 结合图表工具进行数据可视化",
        "🚫 遵守规则: 遵守平台使用条款和法律法规"
    ]
    
    for tip in tips:
        print(f"  {tip}")

async def main():
    """主演示函数"""
    print("🎵 抖音F2客户端高级功能演示")
    print("=" * 60)
    
    # 运行用户分析演示
    await demo_user_analysis()
    
    # 运行视频过滤演示
    await demo_video_filtering()
    
    # 显示使用技巧
    show_usage_tips()
    
    print(f"\n🎉 演示完成！")
    print("💡 接下来你可以:")
    print("1. 设置真实的DOUYIN_COOKIE")
    print("2. 替换示例中的用户ID为真实ID")
    print("3. 根据需要调整分析参数")
    print("4. 开发更多自定义功能")

if __name__ == "__main__":
    asyncio.run(main())
