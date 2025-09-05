"""
高级使用示例
展示TwitterClient的高级功能
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime, timezone

# 添加项目路径到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from twitter_client import TwitterClient, ConfigManager

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TwitterAnalyzer:
    """Twitter数据分析器"""
    
    def __init__(self, client: TwitterClient):
        self.client = client
    
    def analyze_tweets(self, tweets):
        """分析推文数据"""
        if not tweets:
            return {"error": "没有推文数据"}
        
        analysis = {
            "total_tweets": len(tweets),
            "total_likes": 0,
            "total_retweets": 0,
            "total_replies": 0,
            "avg_text_length": 0,
            "most_liked_tweet": None,
            "most_retweeted_tweet": None,
            "hashtags": {},
            "urls": []
        }
        
        text_lengths = []
        max_likes = 0
        max_retweets = 0
        
        for tweet in tweets:
            formatted = self.client.format_tweet(tweet)
            
            # 统计互动数据
            metrics = formatted.get('public_metrics', {})
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            replies = metrics.get('reply_count', 0)
            
            analysis["total_likes"] += likes
            analysis["total_retweets"] += retweets
            analysis["total_replies"] += replies
            
            # 找出最热推文
            if likes > max_likes:
                max_likes = likes
                analysis["most_liked_tweet"] = {
                    "text": formatted.get('text', '')[:100] + "...",
                    "likes": likes
                }
            
            if retweets > max_retweets:
                max_retweets = retweets
                analysis["most_retweeted_tweet"] = {
                    "text": formatted.get('text', '')[:100] + "...",
                    "retweets": retweets
                }
            
            # 统计文本长度
            text = formatted.get('text', '')
            text_lengths.append(len(text))
            
            # 提取话题标签
            words = text.split()
            for word in words:
                if word.startswith('#'):
                    hashtag = word.lower()
                    analysis["hashtags"][hashtag] = analysis["hashtags"].get(hashtag, 0) + 1
            
            # 收集URLs
            urls = formatted.get('urls', [])
            analysis["urls"].extend(urls)
        
        # 计算平均文本长度
        if text_lengths:
            analysis["avg_text_length"] = sum(text_lengths) / len(text_lengths)
        
        return analysis


async def batch_user_analysis():
    """批量用户分析示例"""
    print("=== 批量用户分析示例 ===")
    
    try:
        config_manager = ConfigManager()
        
        if not config_manager.validate_config():
            print("配置验证失败")
            return
        
        client = TwitterClient(config_manager.get_request_config())
        analyzer = TwitterAnalyzer(client)
        
        # 多个用户ID列表
        user_ids = ["25073877"]  # 可以添加更多用户ID
        
        for user_id in user_ids:
            print(f"\n分析用户 {user_id}:")
            print("-" * 30)
            
            try:
                # 获取推文
                tweets = await client.fetch_user_tweets(
                    user_id=user_id,
                    max_tweets=10
                )
                
                if not tweets:
                    print("未获取到推文数据")
                    continue
                
                # 分析推文
                analysis = analyzer.analyze_tweets(tweets)
                
                # 输出分析结果
                print(f"总推文数: {analysis['total_tweets']}")
                print(f"总点赞数: {analysis['total_likes']}")
                print(f"总转发数: {analysis['total_retweets']}")
                print(f"总回复数: {analysis['total_replies']}")
                print(f"平均文本长度: {analysis['avg_text_length']:.1f}字符")
                
                if analysis['most_liked_tweet']:
                    print(f"最热推文(点赞): {analysis['most_liked_tweet']['likes']}赞")
                    print(f"  内容: {analysis['most_liked_tweet']['text']}")
                
                if analysis['hashtags']:
                    print(f"热门话题标签: {dict(list(analysis['hashtags'].items())[:3])}")
                
            except Exception as e:
                logger.error(f"分析用户 {user_id} 时出错: {e}")
                print(f"用户 {user_id} 分析失败: {e}")
        
        await client.close()
        
    except Exception as e:
        logger.error(f"批量分析出错: {e}")


async def data_export_example():
    """数据导出示例"""
    print("\n=== 数据导出示例 ===")
    
    try:
        config_manager = ConfigManager()
        
        if not config_manager.validate_config():
            print("配置验证失败")
            return
        
        client = TwitterClient(config_manager.get_request_config())
        
        user_id = "25073877"
        print(f"\n导出用户 {user_id} 的推文数据...")
        
        # 获取更多推文
        tweets = await client.fetch_user_tweets(
            user_id=user_id,
            max_tweets=20
        )
        
        if not tweets:
            print("未获取到推文数据")
            return
        
        # 格式化推文数据
        formatted_tweets = []
        for tweet in tweets:
            formatted = client.format_tweet(tweet)
            formatted_tweets.append({
                "id": formatted.get('id'),
                "text": formatted.get('text'),
                "author": formatted.get('author'),
                "created_at": formatted.get('created_at'),
                "metrics": formatted.get('public_metrics'),
                "export_time": datetime.now(timezone.utc).isoformat()
            })
        
        # 导出到JSON文件
        export_file = f"tweets_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_path = os.path.join(os.path.dirname(__file__), export_file)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump({
                "user_id": user_id,
                "export_time": datetime.now(timezone.utc).isoformat(),
                "tweet_count": len(formatted_tweets),
                "tweets": formatted_tweets
            }, f, indent=2, ensure_ascii=False)
        
        print(f"推文数据已导出到: {export_path}")
        print(f"导出了 {len(formatted_tweets)} 条推文")
        
        await client.close()
        
    except Exception as e:
        logger.error(f"数据导出出错: {e}")


async def custom_config_example():
    """自定义配置示例"""
    print("\n=== 自定义配置示例 ===")
    
    try:
        # 创建自定义配置
        custom_config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Referer": "https://x.com/",
                "Accept": "application/json",
            },
            "proxies": {
                "http://": None,
                "https://": None
            },
            "cookie": os.getenv("TWITTER_COOKIE", ""),
            "timeout": 60,  # 自定义超时时间
        }
        
        if not custom_config["cookie"]:
            print("需要设置环境变量 TWITTER_COOKIE")
            return
        
        # 使用自定义配置创建客户端
        client = TwitterClient(custom_config)
        
        user_id = "25073877"
        print(f"使用自定义配置获取用户 {user_id} 的推文...")
        
        tweets = await client.fetch_user_tweets(
            user_id=user_id,
            max_tweets=3
        )
        
        print(f"使用自定义配置成功获取 {len(tweets)} 条推文")
        
        await client.close()
        
    except Exception as e:
        logger.error(f"自定义配置示例出错: {e}")


def main():
    """主函数"""
    print("Twitter推文拉取客户端高级示例")
    print("基于F2项目的Twitter API封装")
    print()
    
    # 检查环境
    if not os.getenv("TWITTER_COOKIE"):
        print("⚠️  警告: 未检测到环境变量 TWITTER_COOKIE")
        print("   请设置Twitter登录后的Cookie")
        return
    
    try:
        # 运行高级示例
        print("1. 批量用户分析")
        asyncio.run(batch_user_analysis())
        
        print("\n2. 数据导出")
        asyncio.run(data_export_example())
        
        print("\n3. 自定义配置")
        asyncio.run(custom_config_example())
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行错误: {e}")
        print(f"\n程序错误: {e}")


if __name__ == "__main__":
    main()
