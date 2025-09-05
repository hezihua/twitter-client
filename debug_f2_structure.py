#!/usr/bin/env python3
"""
调试F2数据结构
理解DouyinHandler返回的数据格式
"""

import asyncio
import json
from f2.apps.douyin.handler import DouyinHandler

async def debug_f2_data():
    """调试F2数据结构"""
    print("🔍 调试F2抖音数据结构")
    print("=" * 40)
    
    handler = DouyinHandler({'headers': {'User-Agent': 'test'}, 'cookie': ''})
    
    try:
        async for video_data in handler.fetch_user_post_videos(
            sec_user_id='MS4wLjABAAAAssihLDGWRZQW6LPBR9aTi5UTO-vgXikwTObIvrMCz_Q',
            max_counts=1,
            page_counts=1,
            max_cursor=0
        ):
            print(f"1. 原始对象: {type(video_data)}")
            print(f"2. 对象名称: {video_data.__class__.__name__}")
            print(f"3. 对象模块: {video_data.__class__.__module__}")
            
            # 查看所有可用方法
            methods = [m for m in dir(video_data) if not m.startswith('__')]
            print(f"4. 可用方法({len(methods)}个): {methods}")
            
            # 测试各种数据获取方法
            print("\n📊 测试数据获取方法:")
            
            # _to_dict()
            try:
                dict_result = video_data._to_dict()
                print(f"_to_dict(): {type(dict_result)} - {dict_result}")
            except Exception as e:
                print(f"_to_dict() 错误: {e}")
            
            # _to_raw()
            try:
                raw_result = video_data._to_raw()
                print(f"_to_raw(): {type(raw_result)}")
                if isinstance(raw_result, str):
                    print(f"  长度: {len(raw_result)}")
                    print(f"  预览: {raw_result[:200]}...")
                    
                    # 尝试解析JSON
                    try:
                        json_data = json.loads(raw_result)
                        print(f"  JSON解析成功: {type(json_data)}")
                        if isinstance(json_data, dict):
                            print(f"  JSON键: {list(json_data.keys())}")
                            if 'aweme_list' in json_data:
                                aweme_list = json_data['aweme_list']
                                print(f"  aweme_list长度: {len(aweme_list)}")
                                if aweme_list:
                                    print(f"  第一个视频键: {list(aweme_list[0].keys())[:10]}")
                    except json.JSONDecodeError as e:
                        print(f"  JSON解析失败: {e}")
                elif isinstance(raw_result, dict):
                    print(f"  字典键: {list(raw_result.keys())}")
                else:
                    print(f"  其他格式: {raw_result}")
            except Exception as e:
                print(f"_to_raw() 错误: {e}")
            
            # 尝试其他可能的方法
            for method_name in ['_to_list', 'to_dict', 'to_list', 'data', 'items']:
                if hasattr(video_data, method_name):
                    try:
                        method = getattr(video_data, method_name)
                        if callable(method):
                            result = method()
                        else:
                            result = method
                        print(f"{method_name}: {type(result)} - {str(result)[:100]}")
                    except Exception as e:
                        print(f"{method_name} 错误: {e}")
            
            # 检查是否有数据属性
            for attr in ['data', 'content', 'items', 'videos', 'aweme_list']:
                if hasattr(video_data, attr):
                    try:
                        attr_value = getattr(video_data, attr)
                        print(f"属性 {attr}: {type(attr_value)} - {str(attr_value)[:100]}")
                    except Exception as e:
                        print(f"属性 {attr} 错误: {e}")
            
            break
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_f2_data())
