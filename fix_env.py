#!/usr/bin/env python3
"""
修复.env文件格式
"""

from pathlib import Path

def fix_env_file():
    """修复.env文件格式"""
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        print("❌ .env文件不存在")
        return False
    
    print("🔧 修复.env文件格式...")
    
    # 读取当前内容
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"原始内容长度: {len(content)} 字符")
    
    # 查找Cookie内容
    lines = content.split('\n')
    cookie_content = ""
    
    for line in lines:
        if 'TWITTER_COOKIE' in line:
            # 提取Cookie值
            if '=' in line:
                cookie_part = line.split('=', 1)[1]
                # 移除引号
                cookie_part = cookie_part.strip('"\'')
                cookie_content += cookie_part
        elif cookie_content and line.strip():
            # 如果已经开始收集Cookie，继续添加
            line_clean = line.strip()
            if line_clean.endswith('"'):
                line_clean = line_clean[:-1]
            cookie_content += line_clean
    
    if not cookie_content:
        print("❌ 未找到Cookie内容")
        return False
    
    print(f"提取的Cookie长度: {len(cookie_content)}")
    print(f"包含auth_token: {'auth_token=' in cookie_content}")
    print(f"包含ct0: {'ct0=' in cookie_content}")
    
    # 创建新的.env文件内容
    new_content = f"""# Twitter推文拉取客户端环境变量配置
# Cookie已自动格式化

# Twitter Cookie (必需)
TWITTER_COOKIE={cookie_content}

# 日志级别
LOG_LEVEL=INFO
"""
    
    # 备份原文件
    backup_path = env_path.with_suffix('.env.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 原文件已备份到: {backup_path}")
    
    # 写入修复后的内容
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ .env文件已修复")
    
    # 验证修复结果
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv(env_path)
        cookie = os.getenv('TWITTER_COOKIE')
        
        if cookie:
            print(f"✅ Cookie验证成功 (长度: {len(cookie)})")
            print(f"✅ 包含认证信息: {'auth_token=' in cookie and 'ct0=' in cookie}")
            return True
        else:
            print("❌ Cookie验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 验证时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔧 修复.env文件格式工具")
    print("=" * 30)
    
    if fix_env_file():
        print("\n🎉 .env文件修复成功！")
        print("现在可以运行:")
        print("  python test_with_env.py")
    else:
        print("\n❌ 修复失败")
        print("请手动检查.env文件格式")

if __name__ == "__main__":
    main()
