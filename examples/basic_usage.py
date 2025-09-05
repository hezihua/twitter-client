"""
基本使用示例
展示如何使用TwitterClient拉取推文
"""

import asyncio
import json
import logging
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from twitter_client import TwitterClient, ConfigManager

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def basic_example():
    """基本使用示例"""
    print("=== Twitter推文拉取客户端基本使用示例 ===")
    
    try:
        # 1. 创建配置管理器
        config_manager = ConfigManager()
        
        # 2. 验证配置
        if not config_manager.validate_config():
            print("配置验证失败，请检查配置文件或环境变量")
            print("提示：请设置环境变量 TWITTER_COOKIE 或在配置文件中设置cookie")
            return
        
        # 3. 创建Twitter客户端
        client = TwitterClient(config_manager.get_request_config())
        
        # 4. 获取用户推文（示例：使用一个公开的用户ID）
        user_id = "25073877"  # 示例用户ID，您可以替换为其他用户ID
        print(f"\n正在获取用户 {user_id} 的推文...")
        
        tweets = await client.fetch_user_tweets(
            user_id=user_id,
            max_tweets=5,  # 获取5条推文
            page_size=5
        )
        
        print(f"\n成功获取 {len(tweets)} 条推文:")
        print("-" * 50)
        
        for i, tweet in enumerate(tweets, 1):
            # 格式化推文
            formatted_tweet = client.format_tweet(tweet)
            
            print(f"\n推文 {i}:")
            print(f"ID: {formatted_tweet.get('id', 'N/A')}")
            print(f"作者: {formatted_tweet.get('author', 'N/A')}")
            print(f"内容: {formatted_tweet.get('text', 'N/A')[:100]}...")
            print(f"创建时间: {formatted_tweet.get('created_at', 'N/A')}")
            
            # 显示互动数据
            metrics = formatted_tweet.get('public_metrics', {})
            if metrics:
                print(f"点赞: {metrics.get('like_count', 0)}, "
                      f"转发: {metrics.get('retweet_count', 0)}, "
                      f"回复: {metrics.get('reply_count', 0)}")
        
        # 5. 关闭客户端
        await client.close()
        
    except Exception as e:
        logger.error(f"获取推文时出错: {e}")
        print(f"\n错误: {e}")
        print("\n请检查以下项目:")
        print("1. 网络连接是否正常")
        print("2. Cookie是否有效")
        print("3. 用户ID是否正确")


async def stream_example():
    """流式获取示例"""
    print("\n=== 流式获取推文示例 ===")
    
    try:
        config_manager = ConfigManager()
        
        if not config_manager.validate_config():
            print("配置验证失败")
            return
        
        client = TwitterClient(config_manager.get_request_config())
        
        user_id = "25073877"
        print(f"\n流式获取用户 {user_id} 的推文...")
        
        tweet_count = 0
        async for tweet in client.fetch_user_tweets_stream(
            user_id=user_id,
            max_tweets=3,
            page_size=10
        ):
            tweet_count += 1
            formatted_tweet = client.format_tweet(tweet)
            
            print(f"\n流式推文 {tweet_count}:")
            print(f"内容: {formatted_tweet.get('text', 'N/A')[:80]}...")
            
            if tweet_count >= 3:  # 限制输出数量
                break
        
        await client.close()
        
    except Exception as e:
        logger.error(f"流式获取推文时出错: {e}")
        print(f"\n流式获取错误: {e}")


def main():
    """主函数"""
    print("Twitter推文拉取客户端示例")
    print("基于F2项目的Twitter API封装")
    print()
    
    # 检查环境
    if not os.getenv("TWITTER_COOKIE"):
        print("⚠️  警告: 未检测到环境变量 TWITTER_COOKIE")
        print("   请设置Twitter登录后的Cookie:")
        print("   export TWITTER_COOKIE='your_cookie_here'")
        print()
    
    try:
        # 运行基本示例
        asyncio.run(basic_example())
        
        # 运行流式示例
        asyncio.run(stream_example())
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行错误: {e}")
        print(f"\n程序错误: {e}")


if __name__ == "__main__":
    main()
