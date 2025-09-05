"""
抖音客户端封装类
基于F2项目的DouyinHandler实现抖音视频拉取功能
"""

import asyncio
import json
from typing import Dict, List, Optional, AsyncGenerator, Any
from datetime import datetime
import logging

# 设置日志
logger = logging.getLogger(__name__)

try:
    from f2.apps.douyin.handler import DouyinHandler
    logger.info("✅ 使用真实F2项目抖音模块")
except ImportError:
    logger.error("❌ F2项目抖音模块未正确安装")
    raise ImportError("请确保F2项目已正确安装: pip install -e /tmp/F2_correct")


class DouyinClient:
    """
    抖音视频拉取客户端
    
    基于F2项目的DouyinHandler封装，提供简化的抖音视频拉取接口
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化抖音客户端
        
        Args:
            config: 配置字典，包含headers、proxies、cookie等信息
        """
        self.config = config
        self.handler = None
        self._init_handler()
    
    def _init_handler(self):
        """初始化DouyinHandler"""
        try:
            self.handler = DouyinHandler(self.config)
            logger.info("抖音客户端初始化成功")
        except Exception as e:
            logger.error(f"抖音客户端初始化失败: {e}")
            raise
    
    async def fetch_user_videos(
        self,
        user_id: str,
        max_videos: int = 20,
        page_size: int = 20,
        max_cursor: str = ""
    ) -> List[Dict[str, Any]]:
        """
        获取用户发布的视频
        
        Args:
            user_id: 用户ID或抖音号
            max_videos: 最大获取视频数量
            page_size: 每页视频数量
            max_cursor: 分页游标
            
        Returns:
            视频信息列表
        """
        if not self.handler:
            raise RuntimeError("客户端未初始化")
        
        videos = []
        current_cursor = max_cursor
        
        try:
            # 使用DouyinHandler的用户视频获取功能
            async for video_data in self.handler.fetch_user_post_videos(
                sec_user_id=user_id,
                max_counts=max_videos,
                page_counts=max_videos // page_size + 1,
                max_cursor=int(current_cursor) if current_cursor else 0
            ):
                # 转换为字典格式
                try:
                    video_list = video_data._to_dict()
                    
                    # 调试：打印数据类型和内容
                    logger.info(f"video_data类型: {type(video_data)}")
                    logger.info(f"_to_dict()结果类型: {type(video_list)}")
                    logger.info(f"_to_dict()结果长度: {len(video_list) if hasattr(video_list, '__len__') else 'N/A'}")
                    
                    # 如果返回的是字符串列表（字段名），尝试获取原始数据
                    if isinstance(video_list, list) and video_list and isinstance(video_list[0], str):
                        logger.warning("获取到的是字段名列表，尝试获取原始数据")
                        try:
                            # 尝试使用_to_raw()获取原始数据
                            raw_data = video_data._to_raw()
                            logger.info(f"原始数据类型: {type(raw_data)}")
                            
                            if isinstance(raw_data, dict):
                                # 如果原始数据是字典，直接使用
                                videos.append(raw_data)
                            elif isinstance(raw_data, str):
                                # 如果是JSON字符串，尝试解析
                                import json
                                try:
                                    parsed_data = json.loads(raw_data)
                                    if isinstance(parsed_data, dict) and 'aweme_list' in parsed_data:
                                        videos.extend(parsed_data['aweme_list'])
                                    else:
                                        videos.append(parsed_data)
                                except json.JSONDecodeError:
                                    logger.error("无法解析JSON数据")
                                    videos.append({"raw_data": raw_data, "type": "raw_string"})
                            else:
                                videos.append({"raw_data": raw_data, "type": "unknown"})
                        except Exception as e:
                            logger.error(f"获取原始数据失败: {e}")
                            # 创建一个基本的数据结构
                            videos.append({
                                "aweme_id": "unknown",
                                "desc": f"数据解析失败: {e}",
                                "fields": video_list,
                                "type": "field_list"
                            })
                    else:
                        # 正常情况，直接扩展列表
                        videos.extend(video_list)
                        
                except Exception as e:
                    logger.error(f"数据转换失败: {e}")
                    # 尝试直接使用video_data对象
                    videos.append({
                        "error": str(e),
                        "raw_object": str(video_data),
                        "type": "conversion_error"
                    })
                
                if len(videos) >= max_videos:
                    break
                    
        except Exception as e:
            logger.error(f"获取用户视频失败: {e}")
            # 返回空列表而不是抛出异常，便于演示
            return []
        
        return videos[:max_videos]
    
    async def fetch_video_detail(self, aweme_id: str) -> Dict[str, Any]:
        """
        获取单个视频详情
        
        Args:
            aweme_id: 视频ID
            
        Returns:
            视频详细信息
        """
        if not self.handler:
            raise RuntimeError("客户端未初始化")
        
        try:
            video_detail = await self.handler.fetch_one_video(aweme_id=aweme_id)
            result = video_detail._to_dict()
            return result[0] if result else {}
        except Exception as e:
            logger.error(f"获取视频详情失败: {e}")
            return {}
    
    async def fetch_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户资料信息
        
        Args:
            user_id: 用户ID或抖音号
            
        Returns:
            用户资料信息
        """
        if not self.handler:
            raise RuntimeError("客户端未初始化")
        
        try:
            # 使用正确的DouyinHandler API调用方式
            user_profile = await self.handler.fetch_user_profile(sec_user_id=user_id)
            result = user_profile._to_dict()
            return result[0] if result else {}
        except Exception as e:
            logger.error(f"获取用户资料失败: {e}")
            # 返回空字典而不是抛出异常，便于演示
            return {}
    
    async def search_videos(self, keyword: str, max_videos: int = 20) -> List[Dict[str, Any]]:
        """
        搜索视频
        
        Args:
            keyword: 搜索关键词
            max_videos: 最大获取视频数量
            
        Returns:
            搜索结果视频列表
        """
        if not self.handler:
            raise RuntimeError("客户端未初始化")
        
        videos = []
        
        try:
            # 注意：搜索功能需要根据F2项目的具体实现调整
            # 这里提供基本框架，具体实现可能需要调整
            logger.warning("搜索功能需要根据F2项目具体实现调整")
            
        except Exception as e:
            logger.error(f"搜索视频失败: {e}")
            raise
        
        return videos
    
    def format_video(self, video_data: Any) -> Dict[str, Any]:
        """
        格式化视频数据
        
        Args:
            video_data: 原始视频数据（可能是字典、字符串或其他格式）
            
        Returns:
            格式化后的视频数据
        """
        try:
            # 如果是字符串，直接返回基本格式
            if isinstance(video_data, str):
                return {
                    "aweme_id": "unknown",
                    "desc": video_data[:100] if len(video_data) > 100 else video_data,
                    "author": {"nickname": "Unknown", "unique_id": "unknown"},
                    "statistics": {"digg_count": 0, "comment_count": 0, "share_count": 0, "play_count": 0},
                    "video": {"duration": 0, "width": 0, "height": 0},
                    "url": "https://www.douyin.com/video/unknown",
                    "raw_data": video_data  # 保留原始数据
                }
            
            # 如果不是字典，尝试转换
            if not isinstance(video_data, dict):
                return {
                    "aweme_id": "unknown",
                    "desc": str(video_data)[:100],
                    "author": {"nickname": "Unknown", "unique_id": "unknown"},
                    "statistics": {"digg_count": 0, "comment_count": 0, "share_count": 0, "play_count": 0},
                    "video": {"duration": 0, "width": 0, "height": 0},
                    "url": "https://www.douyin.com/video/unknown",
                    "raw_data": video_data
                }
            
            # 安全地获取字典数据
            def safe_get(data, *keys):
                """安全地获取嵌套字典的值"""
                for key in keys:
                    if isinstance(data, dict) and key in data:
                        data = data[key]
                    else:
                        return None
                return data
            
            return {
                "aweme_id": video_data.get("aweme_id", "unknown"),
                "desc": video_data.get("desc", ""),
                "author": {
                    "unique_id": safe_get(video_data, "author", "unique_id") or "unknown",
                    "nickname": safe_get(video_data, "author", "nickname") or "Unknown",
                    "avatar_url": safe_get(video_data, "author", "avatar_larger", "url_list", 0) or "",
                    "follower_count": safe_get(video_data, "author", "follower_count") or 0,
                    "following_count": safe_get(video_data, "author", "following_count") or 0,
                },
                "create_time": video_data.get("create_time", 0),
                "statistics": {
                    "digg_count": safe_get(video_data, "statistics", "digg_count") or 0,
                    "comment_count": safe_get(video_data, "statistics", "comment_count") or 0,
                    "share_count": safe_get(video_data, "statistics", "share_count") or 0,
                    "play_count": safe_get(video_data, "statistics", "play_count") or 0,
                },
                "video": {
                    "play_url": safe_get(video_data, "video", "play_addr", "url_list", 0) or "",
                    "cover_url": safe_get(video_data, "video", "cover", "url_list", 0) or "",
                    "duration": safe_get(video_data, "video", "duration") or 0,
                    "width": safe_get(video_data, "video", "width") or 0,
                    "height": safe_get(video_data, "video", "height") or 0,
                },
                "music": {
                    "title": safe_get(video_data, "music", "title") or "",
                    "author": safe_get(video_data, "music", "author") or "",
                    "play_url": safe_get(video_data, "music", "play_url", "url_list", 0) or "",
                },
                "hashtags": [
                    tag.get("hashtag_name", "") 
                    for tag in video_data.get("text_extra", []) 
                    if isinstance(tag, dict) and tag.get("type") == 1
                ],
                "url": f"https://www.douyin.com/video/{video_data.get('aweme_id', 'unknown')}",
            }
        except Exception as e:
            logger.error(f"格式化视频数据失败: {e}")
            # 返回安全的默认格式
            return {
                "aweme_id": "error",
                "desc": f"数据格式化错误: {str(e)[:50]}",
                "author": {"nickname": "Error", "unique_id": "error"},
                "statistics": {"digg_count": 0, "comment_count": 0, "share_count": 0, "play_count": 0},
                "video": {"duration": 0, "width": 0, "height": 0},
                "url": "https://www.douyin.com/video/error",
                "raw_data": video_data,
                "error": str(e)
            }
    
    async def close(self):
        """关闭客户端连接"""
        if self.handler:
            # 如果handler有close方法，调用它
            if hasattr(self.handler, 'close'):
                await self.handler.close()
        logger.info("抖音客户端已关闭")
