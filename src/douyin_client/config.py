"""
抖音客户端配置管理
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# 设置日志
logger = logging.getLogger(__name__)


class DouyinConfigManager:
    """抖音配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认使用项目根目录下的config/douyin_config.json
        """
        if config_path is None:
            self.config_path = Path(__file__).parent.parent.parent / "config" / "douyin_config.json"
        else:
            self.config_path = Path(config_path)
        
        self.config = self._load_config()
        self._load_env_variables()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"配置文件加载成功: {self.config_path}")
                return config
            except Exception as e:
                logger.error(f"配置文件加载失败: {e}")
                return self._get_default_config()
        else:
            logger.info("配置文件不存在，使用默认配置")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            默认配置字典
        """
        return {
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1",
                "Referer": "https://www.douyin.com/",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            },
            "proxies": {
                "http://": None,
                "https://": None
            },
            "cookie": "",
            "timeout": 30,
            "max_retries": 3,
            "retry_delay": 1.0,
            "download": {
                "path": "./downloads/douyin/",
                "naming": "aweme_id",  # 文件命名方式：aweme_id 或 desc
                "max_concurrent": 3,
                "chunk_size": 1024 * 1024,  # 1MB
            },
            "filter": {
                "min_duration": 0,  # 最小视频时长（秒）
                "max_duration": 0,  # 最大视频时长（秒），0表示不限制
                "min_digg_count": 0,  # 最小点赞数
                "keywords": [],  # 关键词过滤
                "exclude_keywords": [],  # 排除关键词
            }
        }
    
    def _load_env_variables(self):
        """从环境变量加载配置"""
        # 加载Cookie
        douyin_cookie = os.getenv("DOUYIN_COOKIE")
        if douyin_cookie:
            self.config["cookie"] = douyin_cookie
            logger.info("从环境变量加载抖音Cookie")
        
        # 加载代理设置
        http_proxy = os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("HTTPS_PROXY")
        if http_proxy:
            self.config["proxies"]["http://"] = http_proxy
        if https_proxy:
            self.config["proxies"]["https://"] = https_proxy
        
        # 加载下载路径
        download_path = os.getenv("DOUYIN_DOWNLOAD_PATH")
        if download_path:
            self.config["download"]["path"] = download_path
    
    def save_config(self):
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"配置已保存到: {self.config_path}")
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            raise
    
    def update_config(self, updates: Dict[str, Any]):
        """
        更新配置
        
        Args:
            updates: 要更新的配置项
        """
        def update_nested_dict(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = update_nested_dict(d.get(k, {}), v)
                else:
                    d[k] = v
            return d
        
        update_nested_dict(self.config, updates)
        logger.info("配置已更新")
    
    def validate_config(self) -> bool:
        """
        验证配置是否有效
        
        Returns:
            配置是否有效
        """
        required_fields = ["headers"]
        
        for field in required_fields:
            if field not in self.config:
                logger.error(f"缺少必要配置项: {field}")
                return False
        
        # 验证User-Agent是否存在
        if not self.config["headers"].get("User-Agent"):
            logger.error("缺少User-Agent配置")
            return False
        
        # 抖音Cookie可以为空，F2会处理公开内容
        if not self.config.get("cookie"):
            logger.info("Cookie为空，将访问公开内容")
            self.config["cookie"] = ""  # 确保cookie字段存在
        
        logger.info("配置验证通过")
        return True
    
    def get_request_config(self) -> Dict[str, Any]:
        """
        获取请求相关的配置
        
        Returns:
            请求配置字典
        """
        return {
            "headers": self.config["headers"],
            "proxies": self.config["proxies"],
            "cookie": self.config["cookie"],
            "timeout": self.config.get("timeout", 30)
        }
    
    def get_download_config(self) -> Dict[str, Any]:
        """
        获取下载相关的配置
        
        Returns:
            下载配置字典
        """
        return self.config.get("download", {})
    
    def get_filter_config(self) -> Dict[str, Any]:
        """
        获取过滤相关的配置
        
        Returns:
            过滤配置字典
        """
        return self.config.get("filter", {})


def create_default_douyin_config_file(config_path: str = None):
    """
    创建默认的抖音配置文件
    
    Args:
        config_path: 配置文件路径
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "douyin_config.json"
    else:
        config_path = Path(config_path)
    
    # 创建配置管理器并保存默认配置
    config_manager = DouyinConfigManager()
    config_manager.config_path = config_path
    config_manager.save_config()
    
    print(f"默认抖音配置文件已创建: {config_path}")
    print("请根据需要修改配置文件中的设置")


if __name__ == "__main__":
    # 创建默认配置文件
    create_default_douyin_config_file()
