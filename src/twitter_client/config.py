"""
配置管理模块
用于管理Twitter客户端的配置信息
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# 支持.env文件
try:
    from dotenv import load_dotenv
    # 查找并加载.env文件
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ .env文件已加载: {env_path}")
except ImportError:
    pass  # 如果没安装python-dotenv，跳过

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "Referer": "https://www.x.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
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
        "retry_count": 3,
        "retry_delay": 1
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认为项目根目录的config.json
        """
        if config_path is None:
            # 查找项目根目录
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            config_path = project_root / "config" / "config.json"
        
        self.config_path = Path(config_path)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        从文件加载配置
        
        Returns:
            配置字典
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                
                # 合并配置，文件配置覆盖默认配置
                self._merge_config(self.config, file_config)
                logger.info(f"配置文件已加载: {self.config_path}")
            else:
                logger.info(f"配置文件不存在，使用默认配置: {self.config_path}")
                
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            logger.info("使用默认配置")
        
        # 从环境变量加载敏感配置
        self._load_from_env()
        
        return self.config
    
    def _merge_config(self, base_config: Dict[str, Any], new_config: Dict[str, Any]):
        """
        递归合并配置字典
        
        Args:
            base_config: 基础配置
            new_config: 新配置
        """
        for key, value in new_config.items():
            if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
                self._merge_config(base_config[key], value)
            else:
                base_config[key] = value
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        # 加载Cookie
        env_cookie = os.getenv("TWITTER_COOKIE")
        if env_cookie:
            self.config["cookie"] = env_cookie
            logger.info("从环境变量加载Cookie配置")
        
        # 加载代理配置
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        
        if http_proxy or https_proxy:
            self.config["proxies"] = {
                "http://": http_proxy,
                "https://": https_proxy
            }
            logger.info("从环境变量加载代理配置")
        
        # 加载User-Agent
        env_user_agent = os.getenv("TWITTER_USER_AGENT")
        if env_user_agent:
            self.config["headers"]["User-Agent"] = env_user_agent
            logger.info("从环境变量加载User-Agent配置")
    
    def save_config(self, config: Dict[str, Any] = None):
        """
        保存配置到文件
        
        Args:
            config: 要保存的配置，如果为None则保存当前配置
        """
        try:
            if config:
                self.config = config
            
            # 确保配置目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建一个副本用于保存，移除敏感信息
            save_config = self.config.copy()
            if save_config.get("cookie"):
                save_config["cookie"] = "[从环境变量TWITTER_COOKIE加载]"
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(save_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"配置已保存到: {self.config_path}")
            
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置
        
        Returns:
            配置字典
        """
        return self.config.copy()
    
    def update_config(self, updates: Dict[str, Any]):
        """
        更新配置
        
        Args:
            updates: 要更新的配置项
        """
        self._merge_config(self.config, updates)
        logger.info("配置已更新")
    
    def validate_config(self) -> bool:
        """
        验证配置是否有效
        
        Returns:
            配置是否有效
        """
        required_fields = ["headers", "cookie"]
        
        for field in required_fields:
            if field not in self.config:
                logger.error(f"缺少必要配置项: {field}")
                return False
        
        # 验证Cookie是否存在
        if not self.config["cookie"]:
            logger.warning("Cookie为空，可能无法正常访问Twitter API")
            return False
        
        # 验证User-Agent是否存在
        if not self.config["headers"].get("User-Agent"):
            logger.error("缺少User-Agent配置")
            return False
        
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


def create_default_config_file(config_path: str = None):
    """
    创建默认配置文件
    
    Args:
        config_path: 配置文件路径
    """
    if config_path is None:
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        config_path = project_root / "config" / "config.json"
    else:
        config_path = Path(config_path)
    
    # 确保目录存在
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 创建示例配置
    example_config = ConfigManager.DEFAULT_CONFIG.copy()
    example_config["cookie"] = "[请设置您的Twitter Cookie或使用环境变量TWITTER_COOKIE]"
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(example_config, f, indent=2, ensure_ascii=False)
    
    print(f"默认配置文件已创建: {config_path}")
    print("请编辑配置文件或设置环境变量TWITTER_COOKIE")


if __name__ == "__main__":
    # 创建默认配置文件
    create_default_config_file()
