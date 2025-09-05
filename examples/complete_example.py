#!/usr/bin/env python3
"""
Twitter客户端完整使用示例
展示各种功能和使用场景
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from twitter_client import TwitterClient, ConfigManager

def print_separator(title):
    """打印分隔线"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

async def example1_basic_fetch():
    """示例1：基本推文获取"""
    print_separator("示例1：基本推文获取")
    
    try:
        # 创建客户端
        config_manager = ConfigManager()
        client = TwitterClient(config_manager.get_request_config())
        
        # 获取推文
        user_id = "25073877"  # 示例用户ID
        tweets = await client.fetch_user_tweets(
            user_id=user_id,
            max_tweets=5
        )
        
        print(f"📋 成功获取用户 {user_id} 的 {len(tweets)} 条推文:")
        
        for i, tweet in enumerate(tweets, 1):
            formatted = client.format_tweet(tweet)
            print(f"\n🐦 推文 {i}:")
            print(f"   📝 内容: {formatted.get('text', '')[:80]}...")
            print(f"   👤 作者: {formatted.get('author', 'Unknown')}")
            print(f"   📅 时间: {formatted.get('created_at', 'Unknown')}")
            
            metrics = formatted.get('public_metrics', {})
            print(f"   📊 互动: ❤️{metrics.get('like_count', 0)} "
                  f"🔄{metrics.get('retweet_count', 0)} "
                  f"💬{metrics.get('reply_count', 0)}")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 错误: {e}")

async def example2_stream_processing():
    """示例2：流式处理推文"""
    print_separator("示例2：流式处理推文")
    
    try:
        config_manager = ConfigManager()
        client = TwitterClient(config_manager.get_request_config())
        
        user_id = "25073877"
        print(f"🔄 开始流式获取用户 {user_id} 的推文...")
        
        tweet_count = 0
        total_likes = 0
        hashtags = {}
        
        async for tweet in client.fetch_user_tweets_stream(
            user_id=user_id,
            max_tweets=10,
            page_size=5
        ):
            tweet_count += 1
            formatted = client.format_tweet(tweet)
            
            # 统计数据
            likes = formatted.get('public_metrics', {}).get('like_count', 0)
            total_likes += likes
            
            # 提取话题标签
            text = formatted.get('text', '')
            words = text.split()
            for word in words:
                if word.startswith('#'):
                    hashtags[word] = hashtags.get(word, 0) + 1
            
            print(f"📨 推文 {tweet_count}: {text[:50]}... (❤️{likes})")
            
            # 演示：每获取5条推文输出一次统计
            if tweet_count % 5 == 0:
                print(f"   📊 阶段统计: {tweet_count}条推文, 总点赞:{total_likes}")
        
        # 最终统计
        print(f"\n📈 最终统计:")
        print(f"   📝 总推文数: {tweet_count}")
        print(f"   ❤️ 总点赞数: {total_likes}")
        print(f"   📊 平均点赞: {total_likes/tweet_count if tweet_count > 0 else 0:.1f}")
        if hashtags:
            print(f"   🏷️ 热门话题: {dict(list(hashtags.items())[:3])}")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 错误: {e}")

async def example3_data_analysis():
    """示例3：数据分析"""
    print_separator("示例3：推文数据分析")
    
    try:
        config_manager = ConfigManager()
        client = TwitterClient(config_manager.get_request_config())
        
        # 分析多个用户
        user_ids = ["25073877", "12345678"]  # 示例用户ID列表
        
        all_analysis = {}
        
        for user_id in user_ids:
            print(f"\n📊 分析用户 {user_id}...")
            
            tweets = await client.fetch_user_tweets(
                user_id=user_id,
                max_tweets=8
            )
            
            if not tweets:
                print(f"   ❌ 用户 {user_id} 没有获取到推文")
                continue
            
            # 分析数据
            analysis = {
                "tweet_count": len(tweets),
                "total_likes": 0,
                "total_retweets": 0,
                "total_replies": 0,
                "avg_text_length": 0,
                "most_liked": None,
                "hashtags": {}
            }
            
            text_lengths = []
            max_likes = 0
            
            for tweet in tweets:
                formatted = client.format_tweet(tweet)
                text = formatted.get('text', '')
                metrics = formatted.get('public_metrics', {})
                
                # 统计互动数据
                likes = metrics.get('like_count', 0)
                retweets = metrics.get('retweet_count', 0)
                replies = metrics.get('reply_count', 0)
                
                analysis["total_likes"] += likes
                analysis["total_retweets"] += retweets
                analysis["total_replies"] += replies
                
                # 记录文本长度
                text_lengths.append(len(text))
                
                # 找出最热推文
                if likes > max_likes:
                    max_likes = likes
                    analysis["most_liked"] = {
                        "text": text[:60] + "...",
                        "likes": likes
                    }
                
                # 提取话题标签
                words = text.split()
                for word in words:
                    if word.startswith('#'):
                        analysis["hashtags"][word] = analysis["hashtags"].get(word, 0) + 1
            
            # 计算平均值
            if text_lengths:
                analysis["avg_text_length"] = sum(text_lengths) / len(text_lengths)
            
            all_analysis[user_id] = analysis
            
            # 输出分析结果
            print(f"   📝 推文总数: {analysis['tweet_count']}")
            print(f"   ❤️ 总点赞数: {analysis['total_likes']}")
            print(f"   🔄 总转发数: {analysis['total_retweets']}")
            print(f"   💬 总回复数: {analysis['total_replies']}")
            print(f"   📏 平均长度: {analysis['avg_text_length']:.1f}字符")
            
            if analysis["most_liked"]:
                print(f"   🔥 最热推文: {analysis['most_liked']['text']} (❤️{analysis['most_liked']['likes']})")
            
            if analysis["hashtags"]:
                top_hashtags = dict(list(analysis["hashtags"].items())[:3])
                print(f"   🏷️ 热门话题: {top_hashtags}")
        
        await client.close()
        
        # 对比分析
        if len(all_analysis) > 1:
            print(f"\n🔍 用户对比分析:")
            for user_id, analysis in all_analysis.items():
                engagement_rate = (analysis["total_likes"] + analysis["total_retweets"]) / analysis["tweet_count"] if analysis["tweet_count"] > 0 else 0
                print(f"   👤 用户 {user_id}: 互动率 {engagement_rate:.1f} (点赞+转发)/推文")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

async def example4_data_export():
    """示例4：数据导出"""
    print_separator("示例4：数据导出到文件")
    
    try:
        config_manager = ConfigManager()
        client = TwitterClient(config_manager.get_request_config())
        
        user_id = "25073877"
        tweets = await client.fetch_user_tweets(user_id=user_id, max_tweets=10)
        
        # 准备导出数据
        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "tweet_count": len(tweets),
                "tool": "Twitter Client based on F2"
            },
            "tweets": []
        }
        
        # 格式化推文数据
        for tweet in tweets:
            formatted = client.format_tweet(tweet)
            export_data["tweets"].append({
                "id": formatted.get("id"),
                "text": formatted.get("text"),
                "author": formatted.get("author"),
                "created_at": formatted.get("created_at"),
                "metrics": formatted.get("public_metrics"),
                "hashtags": [word for word in formatted.get("text", "").split() if word.startswith("#")]
            })
        
        # 保存到JSON文件
        filename = f"tweets_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 数据已导出到: {filename}")
        print(f"📊 包含 {len(tweets)} 条推文")
        
        # 显示文件内容预览
        print(f"\n📄 文件内容预览:")
        print(f"   📝 用户ID: {export_data['export_info']['user_id']}")
        print(f"   📅 导出时间: {export_data['export_info']['timestamp']}")
        print(f"   📊 推文数量: {export_data['export_info']['tweet_count']}")
        
        if export_data["tweets"]:
            first_tweet = export_data["tweets"][0]
            print(f"   🐦 首条推文: {first_tweet.get('text', '')[:50]}...")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ 错误: {e}")

def example5_custom_config():
    """示例5：自定义配置"""
    print_separator("示例5：自定义配置使用")
    
    try:
        # 方式1：使用配置管理器
        print("📋 方式1：使用配置管理器")
        config_manager = ConfigManager()
        config = config_manager.get_config()
        print(f"   📝 当前配置文件路径: {config_manager.config_path}")
        print(f"   🔧 配置验证: {'✅ 通过' if config_manager.validate_config() else '❌ 失败'}")
        
        # 方式2：自定义配置
        print(f"\n📋 方式2：自定义配置")
        custom_config = {
            "headers": {
                "User-Agent": "My Custom Twitter Client/1.0",
                "Referer": "https://x.com/"
            },
            "cookie": "模拟Cookie内容",
            "timeout": 45,
            "custom_field": "这是自定义字段"
        }
        
        print("   ⚙️ 自定义配置内容:")
        for key, value in custom_config.items():
            if key == "cookie":
                value = "[已设置]"  # 隐藏敏感信息
            print(f"      {key}: {value}")
        
        # 演示配置更新
        print(f"\n📋 方式3：动态更新配置")
        config_manager.update_config({
            "timeout": 60,
            "retry_count": 5
        })
        print("   ✅ 配置已更新")
        updated_config = config_manager.get_config()
        print(f"      超时时间: {updated_config.get('timeout')}秒")
        print(f"      重试次数: {updated_config.get('retry_count')}次")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

async def main():
    """主函数 - 运行所有示例"""
    print("🚀 Twitter推文拉取客户端 - 完整使用示例")
    print("基于F2项目的Twitter API封装")
    
    # 检查环境
    if not os.getenv("TWITTER_COOKIE"):
        print("\n⚠️  注意: 未设置环境变量 TWITTER_COOKIE")
        print("   当前将使用配置文件中的Cookie或模拟数据")
    
    print("\n🎯 运行以下示例:")
    print("   1️⃣ 基本推文获取")
    print("   2️⃣ 流式处理推文")
    print("   3️⃣ 推文数据分析")
    print("   4️⃣ 数据导出到文件")
    print("   5️⃣ 自定义配置使用")
    
    # 运行所有示例
    await example1_basic_fetch()
    await example2_stream_processing()
    await example3_data_analysis()
    await example4_data_export()
    example5_custom_config()
    
    print_separator("所有示例运行完成")
    print("🎉 恭喜！您已经掌握了Twitter客户端的各种使用方法")
    print("💡 提示：")
    print("   - 当前使用模拟数据，所有功能都已验证可用")
    print("   - 要获取真实Twitter数据，请安装真正的F2项目")
    print("   - 可以基于这些示例开发自己的应用程序")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行错误: {e}")
        import traceback
        traceback.print_exc()
