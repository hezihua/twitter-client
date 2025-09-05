"""
Twitter推文拉取客户端安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Twitter推文拉取客户端，基于F2项目的Twitter API封装"

# 读取requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # 移除注释
                    package = line.split('#')[0].strip()
                    if package:
                        requirements.append(package)
    return requirements

setup(
    name="twitter-client",
    version="1.0.0",
    author="Twitter Client Developer",
    author_email="developer@example.com",
    description="Twitter推文拉取客户端，基于F2项目的Twitter API封装",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/twitter-client",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "analysis": [
            "pandas>=1.5.0",
            "numpy>=1.24.0",
            "matplotlib>=3.6.0",
            "seaborn>=0.12.0",
        ],
        "text": [
            "jieba>=0.42.1",
            "wordcloud>=1.9.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "twitter-client=twitter_client.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
