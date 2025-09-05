"""
Twitter客户端封装类
基于F2项目的TwitterHandler实现推文拉取功能
"""

import asyncio
import json
from typing import Dict, List, Optional, AsyncGenerator, Any
from datetime import datetime
import logging

# 设置日志
logger = logging.getLogger(__name__)

try:
    from f2.apps.twitter.handler import TwitterHandler
    logger.info("✅ 使用真实F2项目")
except ImportError:
    logger.error("❌ F2项目未正确安装")
    raise ImportError("请确保F2项目已正确安装: pip install -e /tmp/F2_correct")


class TwitterClient:
    """
    Twitter推文拉取客户端
    
    基于F2项目的TwitterHandler封装，提供简化的推文拉取接口
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化Twitter客户端
        
        Args:
            config: 配置字典，包含headers、proxies、cookie等信息
        """
        self.config = config
        self.handler = None
        self._init_handler()
    
    def _init_handler(self):
        """初始化TwitterHandler"""
        try:
            self.handler = TwitterHandler(self.config)
            logger.info("Twitter客户端初始化成功")
        except Exception as e:
            logger.error(f"Twitter客户端初始化失败: {e}")
            raise
    
    async def fetch_user_tweets(
        self,
        user_id: str,
        max_tweets: int = 20,
        page_size: int = 20,
        max_cursor: str = ""
    ) -> List[Dict[str, Any]]:
        """
        获取指定用户的推文
        
        Args:
            user_id: 用户ID
            max_tweets: 最大获取推文数量
            page_size: 每页获取的推文数量
            max_cursor: 分页游标
            
        Returns:
            推文列表
        """
        tweets = []
        
        try:
            async for tweet_list in self.handler.fetch_post_tweet(
                userId=user_id,
                page_counts=page_size,
                max_cursor=max_cursor,
                max_counts=max_tweets
            ):
                # 将推文数据转换为字典格式
                tweet_data = tweet_list._to_dict()
                tweets.extend(tweet_data)
                
                logger.info(f"获取到 {len(tweet_data)} 条推文")
                
        except Exception as e:
            logger.error(f"获取推文失败: {e}")
            raise
        
        return tweets[:max_tweets]  # 确保不超过指定数量
    
    async def fetch_user_tweets_stream(
        self,
        user_id: str,
        max_tweets: int = 100,
        page_size: int = 20,
        max_cursor: str = ""
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式获取用户推文
        
        Args:
            user_id: 用户ID
            max_tweets: 最大获取推文数量
            page_size: 每页获取的推文数量
            max_cursor: 分页游标
            
        Yields:
            单条推文数据
        """
        tweet_count = 0
        
        try:
            async for tweet_list in self.handler.fetch_post_tweet(
                userId=user_id,
                page_counts=page_size,
                max_cursor=max_cursor,
                max_counts=max_tweets
            ):
                tweet_data = tweet_list._to_list()
                
                for tweet in tweet_data:
                    if tweet_count >= max_tweets:
                        return
                    
                    yield tweet
                    tweet_count += 1
                    
        except Exception as e:
            logger.error(f"流式获取推文失败: {e}")
            raise
    
    async def get_tweet_details(self, tweet_id: str) -> Dict[str, Any]:
        """
        获取单条推文详情
        
        Args:
            tweet_id: 推文ID
            
        Returns:
            推文详情
        """
        # 注意：这个方法需要根据F2项目的实际API进行调整
        try:
            # 这里需要根据F2项目的具体实现来调用相应方法
            # 目前先返回一个占位符实现
            logger.warning("get_tweet_details方法需要根据F2项目的实际API实现")
            return {"tweet_id": tweet_id, "status": "not_implemented"}
        except Exception as e:
            logger.error(f"获取推文详情失败: {e}")
            raise
    
    def format_tweet(self, tweet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化推文数据
        
        Args:
            tweet_data: 原始推文数据
            
        Returns:
            格式化后的推文数据
        """
        try:
            # 提取关键信息
            formatted_tweet = {
                "id": tweet_data.get("id", ""),
                "text": tweet_data.get("text", ""),
                "author": tweet_data.get("author", {}).get("username", ""),
                "created_at": tweet_data.get("created_at", ""),
                "public_metrics": tweet_data.get("public_metrics", {}),
                "urls": [],
                "media": []
            }
            
            # 提取URL和媒体信息
            entities = tweet_data.get("entities", {})
            if "urls" in entities:
                formatted_tweet["urls"] = entities["urls"]
            
            attachments = tweet_data.get("attachments", {})
            if "media_keys" in attachments:
                formatted_tweet["media"] = attachments["media_keys"]
            
            return formatted_tweet
            
        except Exception as e:
            logger.error(f"格式化推文数据失败: {e}")
            return tweet_data
    
    async def search_tweets(
        self,
        query: str,
        max_tweets: int = 20,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """
        搜索推文（占位符方法）
        
        Args:
            query: 搜索关键词
            max_tweets: 最大获取推文数量
            page_size: 每页获取的推文数量
            
        Returns:
            搜索结果推文列表
        """
        # 注意：这个方法需要根据F2项目的实际API进行调整
        logger.warning("search_tweets方法需要根据F2项目的实际API实现")
        return []
    
    async def close(self):
        """关闭客户端连接"""
        if self.handler:
            # 如果F2的handler有关闭方法，在这里调用
            logger.info("Twitter客户端连接已关闭")


class TwitterClientError(Exception):
    """Twitter客户端异常"""
    pass
