"""
命令行接口模块
提供twitter-client命令行工具
"""

import argparse
import asyncio
import json
import sys
import os
import logging
from typing import Optional

from .client import TwitterClient
from .config import ConfigManager, create_default_config_file

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def fetch_tweets_command(args):
    """获取推文命令"""
    try:
        # 创建配置管理器
        config_manager = ConfigManager(args.config)
        
        if not config_manager.validate_config():
            print("❌ 配置验证失败，请检查配置文件或环境变量TWITTER_COOKIE")
            return 1
        
        # 创建客户端
        client = TwitterClient(config_manager.get_request_config())
        
        print(f"正在获取用户 {args.user_id} 的推文...")
        
        # 获取推文
        if args.stream:
            # 流式获取
            count = 0
            async for tweet in client.fetch_user_tweets_stream(
                user_id=args.user_id,
                max_tweets=args.count,
                page_size=args.page_size
            ):
                count += 1
                formatted = client.format_tweet(tweet)
                
                if args.output:
                    # 保存到文件
                    with open(args.output, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(formatted, ensure_ascii=False) + '\n')
                else:
                    # 输出到控制台
                    print(f"推文 {count}:")
                    print(f"  内容: {formatted.get('text', '')[:100]}...")
                    print(f"  点赞: {formatted.get('public_metrics', {}).get('like_count', 0)}")
                    print("-" * 50)
        else:
            # 批量获取
            tweets = await client.fetch_user_tweets(
                user_id=args.user_id,
                max_tweets=args.count,
                page_size=args.page_size
            )
            
            if args.output:
                # 保存到文件
                output_data = {
                    "user_id": args.user_id,
                    "tweet_count": len(tweets),
                    "tweets": [client.format_tweet(tweet) for tweet in tweets]
                }
                
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ 成功获取 {len(tweets)} 条推文，已保存到 {args.output}")
            else:
                # 输出到控制台
                print(f"✅ 成功获取 {len(tweets)} 条推文:")
                print("-" * 50)
                
                for i, tweet in enumerate(tweets, 1):
                    formatted = client.format_tweet(tweet)
                    print(f"推文 {i}:")
                    print(f"  ID: {formatted.get('id', 'N/A')}")
                    print(f"  作者: {formatted.get('author', 'N/A')}")
                    print(f"  内容: {formatted.get('text', '')[:100]}...")
                    
                    metrics = formatted.get('public_metrics', {})
                    if metrics:
                        print(f"  互动: 👍{metrics.get('like_count', 0)} "
                              f"🔄{metrics.get('retweet_count', 0)} "
                              f"💬{metrics.get('reply_count', 0)}")
                    print("-" * 50)
        
        await client.close()
        return 0
        
    except Exception as e:
        logger.error(f"获取推文失败: {e}")
        print(f"❌ 错误: {e}")
        return 1


def config_command(args):
    """配置命令"""
    try:
        if args.init:
            # 创建默认配置文件
            create_default_config_file(args.config)
            return 0
        
        elif args.show:
            # 显示当前配置
            config_manager = ConfigManager(args.config)
            config = config_manager.get_config()
            
            # 隐藏敏感信息
            config_copy = config.copy()
            if config_copy.get('cookie'):
                config_copy['cookie'] = '[已设置]'
            
            print("当前配置:")
            print(json.dumps(config_copy, indent=2, ensure_ascii=False))
            return 0
        
        elif args.validate:
            # 验证配置
            config_manager = ConfigManager(args.config)
            if config_manager.validate_config():
                print("✅ 配置验证通过")
                return 0
            else:
                print("❌ 配置验证失败")
                return 1
    
    except Exception as e:
        logger.error(f"配置操作失败: {e}")
        print(f"❌ 错误: {e}")
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Twitter推文拉取客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取用户推文
  twitter-client fetch 25073877 --count 10
  
  # 流式获取并保存到文件
  twitter-client fetch 25073877 --stream --output tweets.json
  
  # 初始化配置文件
  twitter-client config --init
  
  # 验证配置
  twitter-client config --validate
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # fetch子命令
    fetch_parser = subparsers.add_parser("fetch", help="获取推文")
    fetch_parser.add_argument("user_id", help="用户ID")
    fetch_parser.add_argument(
        "--count", "-n",
        type=int,
        default=20,
        help="获取推文数量 (默认: 20)"
    )
    fetch_parser.add_argument(
        "--page-size",
        type=int,
        default=20,
        help="每页大小 (默认: 20)"
    )
    fetch_parser.add_argument(
        "--stream",
        action="store_true",
        help="流式获取"
    )
    fetch_parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    
    # config子命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_group = config_parser.add_mutually_exclusive_group()
    config_group.add_argument(
        "--init",
        action="store_true",
        help="创建默认配置文件"
    )
    config_group.add_argument(
        "--show",
        action="store_true",
        help="显示当前配置"
    )
    config_group.add_argument(
        "--validate",
        action="store_true",
        help="验证配置"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 执行命令
    if args.command == "fetch":
        return asyncio.run(fetch_tweets_command(args))
    elif args.command == "config":
        return config_command(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
