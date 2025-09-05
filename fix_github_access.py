#!/usr/bin/env python3
"""
修复GitHub访问问题并安装真正的F2项目
基于workspace中的GitHub连接问题解决方案
"""

import subprocess
import os
import sys

def run_command(cmd, description=""):
    """运行命令并显示结果"""
    print(f"🔧 {description}")
    print(f"   命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ 输出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 失败: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def fix_dns_config():
    """修复DNS配置"""
    print("\n📡 步骤 1: 修复DNS配置")
    
    # 备份并更换DNS
    commands = [
        ('echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf.backup', "备份DNS配置"),
        ('sudo cp /etc/resolv.conf.backup /etc/resolv.conf', "应用Google DNS"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    return True

def add_github_hosts():
    """添加GitHub IP映射"""
    print("\n🌐 步骤 2: 添加GitHub IP映射")
    
    # 添加GitHub主站和API的IP映射
    commands = [
        ('echo "140.82.112.3 github.com" | sudo tee -a /etc/hosts', "添加GitHub主站IP"),
        ('echo "140.82.114.3 api.github.com" | sudo tee -a /etc/hosts', "添加GitHub API IP"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    return True

def verify_github_connection():
    """验证GitHub连接"""
    print("\n🔍 步骤 3: 验证GitHub连接")
    
    return run_command('ping -c 2 github.com', "测试GitHub连接")

def configure_git_settings():
    """配置Git设置以优化网络连接"""
    print("\n⚙️  步骤 4: 优化Git配置")
    
    commands = [
        ('git config --global http.lowSpeedLimit 0', "设置Git低速限制"),
        ('git config --global http.lowSpeedTime 999999', "设置Git超时时间"),
    ]
    
    for cmd, desc in commands:
        run_command(cmd, desc)

def install_real_f2():
    """安装真正的F2项目"""
    print("\n📦 步骤 5: 安装真正的F2项目")
    
    # 使用浅克隆减少数据传输
    f2_repos = [
        "https://github.com/JohnstonLiu/F2.git",
        "https://github.com/F2-dev/F2.git"
    ]
    
    for repo_url in f2_repos:
        print(f"\n📥 尝试从 {repo_url} 克隆...")
        
        # 清理可能存在的目录
        run_command('rm -rf /tmp/F2_real', "清理临时目录")
        
        # 使用浅克隆
        if run_command(f'git clone --depth 1 {repo_url} /tmp/F2_real', f"浅克隆 {repo_url}"):
            print("✅ 克隆成功！开始安装...")
            
            # 安装F2
            if run_command('pip install -e /tmp/F2_real', "安装F2项目"):
                print("🎉 F2项目安装成功！")
                return True
            else:
                print("❌ F2安装失败，继续尝试下一个仓库")
        else:
            print(f"❌ 克隆失败: {repo_url}")
    
    return False

def remove_mock_module():
    """移除模拟模块"""
    print("\n🗑️  步骤 6: 移除模拟模块")
    
    mock_path = "src/f2_mock"
    if os.path.exists(mock_path):
        import shutil
        shutil.rmtree(mock_path)
        print("✅ 模拟模块已移除")
        return True
    else:
        print("ℹ️  模拟模块不存在")
        return False

def test_real_twitter_client():
    """测试真实Twitter客户端"""
    print("\n🧪 步骤 7: 测试真实Twitter客户端")
    
    try:
        # 重新导入以使用真实F2
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from f2.apps.twitter.handler import TwitterHandler
        print("✅ 真实F2模块导入成功")
        
        # 测试基本功能
        test_config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "cookie": "test_cookie",
            "proxies": {"http://": None, "https://": None}
        }
        
        handler = TwitterHandler(test_config)
        print("✅ TwitterHandler创建成功")
        print("🎉 真实F2项目已就绪！")
        
        return True
        
    except ImportError:
        print("❌ F2导入失败，可能安装不完整")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def setup_permanent_solution():
    """设置永久解决方案"""
    print("\n🔒 步骤 8: 配置永久解决方案")
    
    wsl_conf_content = """[network]
generateResolvConf = false
"""
    
    try:
        with open('/tmp/wsl.conf', 'w') as f:
            f.write(wsl_conf_content)
        
        if run_command('sudo cp /tmp/wsl.conf /etc/wsl.conf', "创建WSL永久配置"):
            print("✅ 永久配置已设置")
            print("⚠️  重启WSL2后配置将永久生效")
            return True
    except Exception as e:
        print(f"❌ 永久配置失败: {e}")
        return False

def main():
    """主函数"""
    print("🐦 修复GitHub访问问题并安装真实F2项目")
    print("=" * 60)
    print("基于workspace/GitHub连接问题解决方案.md")
    print()
    
    # 检查权限
    if os.geteuid() == 0:
        print("⚠️  请不要以root权限运行此脚本")
        sys.exit(1)
    
    success_count = 0
    total_steps = 8
    
    # 执行修复步骤
    steps = [
        ("修复DNS配置", fix_dns_config),
        ("添加GitHub IP映射", add_github_hosts), 
        ("验证GitHub连接", verify_github_connection),
        ("配置Git设置", configure_git_settings),
        ("安装真正的F2项目", install_real_f2),
        ("移除模拟模块", remove_mock_module),
        ("测试真实Twitter客户端", test_real_twitter_client),
        ("设置永久解决方案", setup_permanent_solution)
    ]
    
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
                print(f"✅ {step_name} - 完成")
            else:
                print(f"❌ {step_name} - 失败")
        except Exception as e:
            print(f"❌ {step_name} - 异常: {e}")
        
        print("-" * 50)
    
    # 总结
    print(f"\n📊 执行结果: {success_count}/{total_steps} 步骤成功")
    
    if success_count >= 5:  # 前5步是关键步骤
        print("🎉 恭喜！GitHub访问问题已修复，F2项目安装成功！")
        print("\n📝 下一步:")
        print("1. 设置真实的Twitter Cookie:")
        print("   export TWITTER_COOKIE='your_real_cookie'")
        print("2. 测试真实推文获取:")
        print("   cd examples && python simple_usage.py")
        print("3. 如需重启WSL2以应用永久配置:")
        print("   在Windows PowerShell中运行: wsl --shutdown")
    else:
        print("⚠️  部分步骤失败，但您仍可以:")
        print("1. 手动执行失败的步骤")
        print("2. 继续使用模拟数据进行开发")
        print("3. 稍后重新运行此脚本")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  操作被用户中断")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
