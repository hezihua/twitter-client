#!/bin/bash
# Twitter客户端命令行使用示例

echo "🐦 Twitter客户端命令行使用示例"
echo "================================"

cd "$(dirname "$0")/.."

echo ""
echo "1️⃣ 获取基本推文:"
python -m src.twitter_client.cli fetch 25073877 --count 3

echo ""
echo "2️⃣ 获取更多推文并保存到文件:"
python -m src.twitter_client.cli fetch 25073877 --count 5 --output examples/output_tweets.json

echo ""
echo "3️⃣ 流式获取推文:"
python -m src.twitter_client.cli fetch 25073877 --stream --count 3

echo ""
echo "4️⃣ 查看配置:"
python -m src.twitter_client.cli config --show

echo ""
echo "5️⃣ 验证配置:"
python -m src.twitter_client.cli config --validate

echo ""
echo "✅ 命令行示例完成！"
