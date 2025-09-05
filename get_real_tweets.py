#!/usr/bin/env python3
"""
获取真实Twitter推文的解决方案
"""

import os
import sys
import subprocess

def check_current_status():
    """检查当前使用的是模拟还是真实F2"""
    print("🔍 检查当前状态...")
    
    # 检查是否有模拟模块
    if os.path.exists("src/f2_mock"):
        print("⚠️  当前使用模拟模块 - 返回示例数据")
        print("   位置: src/f2_mock/")
        return "mock"
    
    # 检查是否安装了真实F2
    try:
        import f2
        print("✅ 真实F2项目已安装")
        return "real"
    except ImportError:
        print("❌ 真实F2项目未安装")
        return "none"

def install_real_f2():
    """尝试安装真实的F2项目"""
    print("\n🚀 尝试安装真实F2项目...")
    
    # 可能的GitHub仓库地址
    repos = [
        "https://github.com/JohnstonLiu/F2.git",
        "https://gitee.com/johnsonliu/F2.git",  # 国内镜像
        "https://github.com/F2-dev/F2.git"
    ]
    
    for repo in repos:
        print(f"\n📥 尝试从 {repo} 安装...")
        try:
            # 克隆仓库
            result = subprocess.run([
                "git", "clone", "--depth=1", repo, "/tmp/F2_install"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ 仓库克隆成功")
                
                # 安装
                install_result = subprocess.run([
                    "pip", "install", "-e", "/tmp/F2_install"
                ], capture_output=True, text=True, timeout=60)
                
                if install_result.returncode == 0:
                    print("🎉 F2项目安装成功！")
                    return True
                else:
                    print(f"❌ 安装失败: {install_result.stderr}")
            else:
                print(f"❌ 克隆失败: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ 超时，尝试下一个仓库...")
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    return False

def setup_real_twitter_config():
    """配置真实Twitter访问"""
    print("\n⚙️ 配置真实Twitter访问...")
    print("""
要获取真实Twitter推文，您需要：

1️⃣ 获取Twitter Cookie:
   - 登录 https://x.com (Twitter)
   - 打开浏览器开发者工具 (F12)
   - 找到 Network 标签
   - 刷新页面，查找任意请求
   - 复制 Request Headers 中的 Cookie 值

2️⃣ 设置环境变量:
   export TWITTER_COOKIE="你的Cookie值"

3️⃣ 或者编辑配置文件:
   编辑 config/config.json，设置 cookie 字段

📝 Cookie 格式示例:
   auth_token=xxxxx; ct0=xxxxx; _ga=xxxxx; ...

⚠️  注意事项:
   - Cookie会过期，需要定期更新
   - 请遵守Twitter服务条款
   - 不要分享您的Cookie给他人
    """)

def remove_mock_module():
    """移除模拟模块，强制使用真实F2"""
    print("\n🗑️ 移除模拟模块...")
    
    mock_path = "src/f2_mock"
    if os.path.exists(mock_path):
        import shutil
        shutil.rmtree(mock_path)
        print("✅ 模拟模块已移除")
        return True
    else:
        print("ℹ️  模拟模块不存在")
        return False

def test_real_f2():
    """测试真实F2是否正常工作"""
    print("\n🧪 测试真实F2...")
    
    try:
        from f2.apps.twitter.handler import TwitterHandler
        print("✅ 真实F2导入成功")
        
        # 简单测试
        test_config = {
            "headers": {"User-Agent": "Test"},
            "cookie": os.getenv("TWITTER_COOKIE", "test_cookie")
        }
        
        handler = TwitterHandler(test_config)
        print("✅ TwitterHandler创建成功")
        return True
        
    except ImportError:
        print("❌ F2导入失败，可能未正确安装")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🐦 获取真实Twitter推文解决方案")
    print("="*50)
    
    # 1. 检查当前状态
    status = check_current_status()
    
    if status == "real":
        print("\n🎉 您已经在使用真实F2项目！")
        setup_real_twitter_config()
        return
    
    # 2. 提供解决方案选择
    print("\n🔧 解决方案:")
    print("1️⃣ 尝试自动安装真实F2项目")
    print("2️⃣ 查看手动安装指南")
    print("3️⃣ 继续使用模拟数据进行开发")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        print("\n📦 开始自动安装...")
        if install_real_f2():
            remove_mock_module()
            if test_real_f2():
                print("\n🎉 真实F2安装成功！")
                setup_real_twitter_config()
            else:
                print("\n⚠️  F2安装成功但测试失败，请检查配置")
        else:
            print("\n❌ 自动安装失败，请尝试手动安装")
    
    elif choice == "2":
        print("""
📖 手动安装F2项目指南:

1. 准备环境:
   sudo apt update
   sudo apt install git python3-pip

2. 克隆F2项目:
   git clone https://github.com/JohnstonLiu/F2.git
   cd F2

3. 安装F2:
   pip install -e .

4. 返回twitter-client项目:
   cd ../twitter-client

5. 移除模拟模块:
   rm -rf src/f2_mock

6. 测试:
   python examples/simple_usage.py

💡 如果GitHub访问有问题，尝试:
   - 使用国内镜像: https://gitee.com/johnsonliu/F2.git
   - 配置代理: git config --global http.proxy http://proxy:port
   - 下载zip包: wget https://github.com/JohnstonLiu/F2/archive/main.zip
        """)
    
    elif choice == "3":
        print("""
🎭 继续使用模拟数据:

模拟数据的优势:
✅ 无需网络配置
✅ 数据结构完整
✅ 适合开发和测试
✅ 功能完全可用

模拟数据的限制:
❌ 非真实Twitter内容
❌ 固定的用户和推文
❌ 无法获取最新数据

💡 您可以:
1. 使用模拟数据学习API
2. 开发和测试功能
3. 稍后安装真实F2获取真实数据
        """)
    
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 操作被取消")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        import traceback
        traceback.print_exc()
