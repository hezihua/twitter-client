#!/usr/bin/env python3
"""
使用模拟数据的Twitter客户端示例
当真实API访问受限时的完整解决方案
"""

import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def demonstrate_mock_twitter_client():
    """演示使用模拟数据的Twitter客户端功能"""
    print("🎭 Twitter模拟数据客户端演示")
    print("=" * 50)
    
    try:
        # 导入模拟的TwitterHandler
        from f2.apps.twitter.handler import TwitterHandler
        
        # 使用任意配置（模拟环境下不需要真实Cookie）
        mock_config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "proxies": {},
            "cookie": "mock_cookie_for_testing"
        }
        
        print("⚙️ 创建模拟Twitter客户端...")
        handler = TwitterHandler(mock_config)
        print("✅ 客户端创建成功!")
        
        # 测试不同用户的推文获取
        test_users = ["elonmusk", "Twitter", "OpenAI", "github", "cellinlab"]
        
        all_tweets = []
        
        for user in test_users:
            print(f"\n🔍 获取用户 @{user} 的推文...")
            
            try:
                tweet_count = 0
                async for tweet_list in handler.fetch_post_tweet(
                    userId=user,
                    page_counts=1,
                    max_counts=5
                ):
                    # 获取推文数据
                    tweets = tweet_list._to_dict()
                    tweet_count = len(tweets)
                    
                    print(f"📊 获取到 {tweet_count} 条推文")
                    
                    if tweets:
                        # 显示第一条推文的详细信息
                        first_tweet = tweets[0]
                        print(f"📝 示例推文:")
                        print(f"   内容: {first_tweet.get('text', 'N/A')[:100]}...")
                        print(f"   作者: @{first_tweet.get('author', {}).get('username', 'N/A')}")
                        print(f"   时间: {first_tweet.get('created_at', 'N/A')}")
                        print(f"   点赞: {first_tweet.get('metrics', {}).get('like_count', 0)}")
                        print(f"   转发: {first_tweet.get('metrics', {}).get('retweet_count', 0)}")
                        
                        # 收集所有推文用于后续分析
                        all_tweets.extend(tweets)
                    
                    break  # 只处理第一页
                    
            except Exception as e:
                print(f"❌ 获取 @{user} 推文失败: {e}")
                continue
        
        # 数据分析演示
        if all_tweets:
            print(f"\n📈 数据分析演示")
            print("=" * 30)
            
            # 统计信息
            total_tweets = len(all_tweets)
            total_likes = sum(tweet.get('metrics', {}).get('like_count', 0) for tweet in all_tweets)
            total_retweets = sum(tweet.get('metrics', {}).get('retweet_count', 0) for tweet in all_tweets)
            
            print(f"📊 总推文数: {total_tweets}")
            print(f"❤️ 总点赞数: {total_likes}")
            print(f"🔄 总转发数: {total_retweets}")
            print(f"📈 平均点赞数: {total_likes/total_tweets:.1f}")
            print(f"📈 平均转发数: {total_retweets/total_tweets:.1f}")
            
            # 用户活跃度分析
            user_stats = {}
            for tweet in all_tweets:
                username = tweet.get('author', {}).get('username', 'Unknown')
                if username not in user_stats:
                    user_stats[username] = {
                        'tweets': 0,
                        'total_likes': 0,
                        'total_retweets': 0
                    }
                
                user_stats[username]['tweets'] += 1
                user_stats[username]['total_likes'] += tweet.get('metrics', {}).get('like_count', 0)
                user_stats[username]['total_retweets'] += tweet.get('metrics', {}).get('retweet_count', 0)
            
            print(f"\n👥 用户活跃度排行:")
            for username, stats in sorted(user_stats.items(), key=lambda x: x[1]['total_likes'], reverse=True):
                print(f"   @{username}: {stats['tweets']}条推文, {stats['total_likes']}点赞, {stats['total_retweets']}转发")
        
        # 导出数据演示
        export_data = {
            "export_time": datetime.now().isoformat(),
            "total_tweets": len(all_tweets),
            "users_analyzed": len(test_users),
            "summary": {
                "total_likes": sum(tweet.get('metrics', {}).get('like_count', 0) for tweet in all_tweets),
                "total_retweets": sum(tweet.get('metrics', {}).get('retweet_count', 0) for tweet in all_tweets),
                "avg_engagement": sum(tweet.get('metrics', {}).get('like_count', 0) + tweet.get('metrics', {}).get('retweet_count', 0) for tweet in all_tweets) / len(all_tweets) if all_tweets else 0
            },
            "tweets": all_tweets[:10]  # 只保存前10条作为示例
        }
        
        # 保存到文件
        export_file = "mock_twitter_data_export.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 数据已导出到: {export_file}")
        print(f"📄 导出文件大小: {os.path.getsize(export_file)} 字节")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("💡 请确保F2模拟模块已正确安装")
        return False
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def show_mock_advantages():
    """展示模拟数据的优势"""
    print(f"\n🎯 模拟数据解决方案的优势")
    print("=" * 40)
    
    advantages = [
        "✅ 无需处理403访问限制问题",
        "✅ 数据结构与真实API完全一致", 
        "✅ 可以进行完整的功能开发和测试",
        "✅ 不受网络环境和Cookie限制影响",
        "✅ 适合学习Twitter API的使用方法",
        "✅ 支持所有核心功能：获取推文、用户信息、数据分析",
        "✅ 可以无缝切换到真实API（当网络条件允许时）",
        "✅ 提供稳定、可预测的开发环境"
    ]
    
    for advantage in advantages:
        print(f"  {advantage}")
    
    print(f"\n💡 使用建议:")
    print("1. 🔧 使用模拟数据完成所有功能开发")
    print("2. 📊 基于模拟数据进行数据分析和可视化")
    print("3. 🧪 编写完整的测试用例")
    print("4. 📝 准备切换到真实API的文档")
    print("5. 🚀 当网络环境改善时，一键切换到真实数据")

def show_real_api_transition_guide():
    """显示切换到真实API的指南"""
    print(f"\n🔄 切换到真实API指南")
    print("=" * 30)
    
    steps = [
        "1. 确保网络可以访问GitHub和Twitter API",
        "2. 删除模拟模块: rm -rf src/f2_mock/",
        "3. 安装真实F2项目: pip install git+https://github.com/JohnstonLiu/F2.git",
        "4. 获取最新的Twitter Cookie",
        "5. 更新.env文件中的Cookie",
        "6. 运行测试脚本验证连接",
        "7. 现有代码无需修改，直接使用真实数据"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n⚠️ 注意事项:")
    print("- 真实API可能有访问限制和频率限制")
    print("- 需要有效的Twitter账户和Cookie")
    print("- 可能需要处理网络超时和错误重试")
    print("- 建议保留模拟模块作为备用方案")

async def main():
    """主函数"""
    print("🐦 Twitter客户端 - 模拟数据解决方案")
    print("=" * 60)
    
    # 演示模拟客户端功能
    success = await demonstrate_mock_twitter_client()
    
    if success:
        print(f"\n🎉 模拟数据演示成功完成!")
        
        # 显示优势和指南
        show_mock_advantages()
        show_real_api_transition_guide()
        
        print(f"\n🚀 下一步建议:")
        print("1. 基于模拟数据开发更多功能（数据分析、可视化等）")
        print("2. 完善错误处理和用户体验")
        print("3. 编写完整的测试用例")
        print("4. 准备生产环境部署")
        
    else:
        print(f"\n❌ 演示失败，请检查F2模拟模块安装")

if __name__ == "__main__":
    asyncio.run(main())
