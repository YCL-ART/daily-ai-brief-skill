"""
测试配置
"""
import os
import tempfile
import yaml

TEST_CONFIG = {
    "rss_sources": [
        {
            "name": "Test RSS Feed",
            "url": "https://feeds.feedburner.com/Techcrunch",  # 一个真实的RSS源用于测试
            "language": "en",
            "enabled": True,
            "priority": 1,
            "num_items": 3,
        }
    ],
    "reddit_sources": [
        {
            "name": "Test Reddit",
            "type": "reddit",
            "subreddit": "python",
            "language": "en",
            "enabled": True,
            "priority": 2,
            "num_items": 2,
        }
    ],
    "fetch_config": {
        "timeout_seconds": 10,
        "user_agent": "Test Agent",
        "max_retries": 1,
    }
}


def create_test_config_file() -> str:
    """
    创建临时测试配置文件

    Returns:
        配置文件路径
    """
    # 创建临时文件
    fd, temp_path = tempfile.mkstemp(suffix='.yaml', prefix='test_config_')
    os.close(fd)

    # 写入测试配置
    with open(temp_path, 'w', encoding='utf-8') as f:
        yaml.dump(TEST_CONFIG, f, default_flow_style=False, allow_unicode=True)

    return temp_path


def cleanup_test_config_file(config_path: str):
    """
    清理测试配置文件

    Args:
        config_path: 配置文件路径
    """
    if os.path.exists(config_path):
        os.remove(config_path)