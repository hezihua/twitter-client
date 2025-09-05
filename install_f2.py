#!/usr/bin/env python3
"""
F2项目安装脚本
自动从GitHub克隆F2项目并安装，或创建模拟模块
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {cmd}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return None

def install_f2_from_github():
    """尝试从GitHub安装F2项目"""
    print("=== 尝试从GitHub安装F2项目 ===")
    
    # 可能的GitHub仓库地址
    repo_urls = [
        "https://github.com/JohnstonLiu/F2.git",
        "https://github.com/johnliu-tw/F2.git", 
        "https://github.com/F2-dev/F2.git"
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for repo_url in repo_urls:
            print(f"\n尝试从 {repo_url} 克隆...")
            
            # 尝试克隆仓库
            clone_result = run_command(f"git clone --depth=1 {repo_url}", cwd=temp_dir)
            if clone_result is not None:
                print(f"✅ 成功克隆仓库")
                
                # 查找克隆的目录
                repo_name = repo_url.split('/')[-1].replace('.git', '')
                repo_path = Path(temp_dir) / repo_name
                
                if repo_path.exists():
                    print(f"安装F2项目: {repo_path}")
                    
                    # 尝试安装
                    install_result = run_command("pip install -e .", cwd=repo_path)
                    if install_result is not None:
                        print("✅ F2项目安装成功!")
                        return True
                    else:
                        # 尝试标准安装
                        install_result = run_command("pip install .", cwd=repo_path)
                        if install_result is not None:
                            print("✅ F2项目安装成功!")
                            return True
            
            print(f"❌ 从 {repo_url} 安装失败")
    
    return False

def create_mock_f2():
    """创建F2的模拟模块"""
    print("\n=== 创建F2模拟模块 ===")
    
    mock_f2_dir = Path("src/f2_mock")
    mock_f2_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建__init__.py
    (mock_f2_dir / "__init__.py").write_text('"""F2模拟模块"""\n')
    
    # 创建apps模块结构
    apps_dir = mock_f2_dir / "apps"
    apps_dir.mkdir(exist_ok=True)
    (apps_dir / "__init__.py").write_text("")
    
    twitter_dir = apps_dir / "twitter"
    twitter_dir.mkdir(exist_ok=True)
    (twitter_dir / "__init__.py").write_text("")
    
    # 创建模拟的TwitterHandler
    handler_content = '''"""
Twitter处理器模拟模块
"""

import asyncio
import json
import logging
from typing import Dict, Any, AsyncGenerator

logger = logging.getLogger(__name__)

class TwitterHandler:
    """Twitter处理器模拟类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        print("⚠️  使用F2模拟模块 - 返回示例数据")
    
    async def fetch_post_tweet(
        self, 
        userId: str, 
        page_counts: int = 20, 
        max_cursor: str = "", 
        max_counts: int = 20
    ) -> AsyncGenerator:
        """模拟获取推文"""
        mock_tweets = MockTweetList([
            {
                "id": f"mock_{userId}_{i}",
                "text": f"这是用户{userId}的第{i}条模拟推文 #示例 #测试",
                "author": {"username": f"user_{userId}"},
                "created_at": f"2024-01-{i:02d}T12:00:00Z",
                "public_metrics": {
                    "like_count": i * 10,
                    "retweet_count": i * 5,
                    "reply_count": i * 2
                },
                "entities": {"urls": []},
                "attachments": {}
            }
            for i in range(1, min(max_counts, 10) + 1)
        ])
        
        await asyncio.sleep(0.1)
        yield mock_tweets

class MockTweetList:
    """模拟推文列表类"""
    
    def __init__(self, tweets):
        self.tweets = tweets
    
    def _to_dict(self):
        return self.tweets
    
    def _to_list(self):
        return self.tweets
    
    def _to_raw(self):
        return json.dumps(self.tweets, indent=2, ensure_ascii=False)
'''
    
    (twitter_dir / "handler.py").write_text(handler_content, encoding='utf-8')
    
    print(f"✅ F2模拟模块已创建")
    return True

def update_client_imports():
    """更新客户端代码"""
    client_file = Path("src/twitter_client/client.py")
    if not client_file.exists():
        return False
    
    content = client_file.read_text(encoding='utf-8')
    
    old_import = '''try:
    from f2.apps.twitter.handler import TwitterHandler
except ImportError:
    raise ImportError("请先安装f2包：pip install f2")'''
    
    new_import = '''try:
    from f2.apps.twitter.handler import TwitterHandler
except ImportError:
    try:
        import sys
        from pathlib import Path
        mock_path = Path(__file__).parent.parent / "f2_mock"
        if mock_path.exists():
            sys.path.insert(0, str(mock_path.parent))
            from f2_mock.apps.twitter.handler import TwitterHandler
        else:
            raise ImportError("F2项目和模拟模块都未找到")
    except ImportError:
        raise ImportError("请运行 python install_f2.py 安装F2或创建模拟模块")'''
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        client_file.write_text(content, encoding='utf-8')
        print("✅ 客户端导入已更新")
    
    return True

def main():
    """主函数"""
    print("=== F2项目安装工具 ===")
    
    # 检查git
    if run_command("git --version"):
        print("✅ Git已安装")
        if install_f2_from_github():
            print("\n🎉 F2项目安装成功！")
            return
    
    # 创建模拟模块
    if create_mock_f2():
        update_client_imports()
        print("\n🎭 已创建F2模拟模块")
        print("✅ 现在可以运行示例代码了（使用模拟数据）")
        print("\n要获取真实数据，请手动安装F2项目")

if __name__ == "__main__":
    main()
