"""
测试抓取器工厂
"""
import unittest

# 添加模块路径
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.fetcher_factory import FetcherFactory


class TestFetcherFactory(unittest.TestCase):
    """测试抓取器工厂"""

    def setUp(self):
        """测试前置设置"""
        self.factory = FetcherFactory()

    def test_create_rss_fetcher(self):
        """测试创建RSS抓取器"""
        config = {
            "name": "Test RSS",
            "url": "https://example.com/feed",
            "language": "en",
            "enabled": True,
            "priority": 1,
        }

        fetcher = self.factory.create_fetcher("rss", config)
        self.assertIsNotNone(fetcher)
        self.assertEqual(fetcher.name, "Test RSS")
        self.assertEqual(fetcher.__class__.__name__, "RSSFetcher")

    def test_create_disabled_fetcher(self):
        """测试创建禁用的抓取器"""
        config = {
            "name": "Test Disabled",
            "url": "https://example.com/feed",
            "enabled": False,
        }

        fetcher = self.factory.create_fetcher("rss", config)
        self.assertIsNone(fetcher)

    def test_create_unknown_type(self):
        """测试创建未知类型抓取器"""
        config = {
            "name": "Test Unknown",
            "enabled": True,
        }

        fetcher = self.factory.create_fetcher("unknown_type", config)
        self.assertIsNone(fetcher)

    def test_create_fetchers_from_config(self):
        """测试从配置创建抓取器"""
        config = {
            "rss_sources": [
                {
                    "name": "RSS Test 1",
                    "url": "https://example.com/feed1",
                    "enabled": True,
                },
                {
                    "name": "RSS Test 2",
                    "url": "https://example.com/feed2",
                    "enabled": False,  # 禁用
                },
            ],
            "reddit_sources": [
                {
                    "name": "Reddit Test",
                    "subreddit": "python",
                    "enabled": True,
                }
            ],
            "x_sources": [
                {
                    "name": "Twitter Test",
                    "username": "testuser",
                    "enabled": True,
                }
            ],
        }

        fetchers = self.factory.create_fetchers_from_config(config)

        # 应该创建3个抓取器（1个禁用的不算）
        self.assertEqual(len(fetchers), 3)

        # 检查类型
        fetcher_types = [f.__class__.__name__ for f in fetchers]
        self.assertIn("RSSFetcher", fetcher_types)
        self.assertIn("RedditFetcher", fetcher_types)
        self.assertIn("XFetcher", fetcher_types)

    def test_create_by_source_type(self):
        """测试根据数据源类型创建抓取器"""
        config = {
            "name": "Test Source",
            "url": "https://example.com/feed",
            "enabled": True,
        }

        # 测试RSS源
        fetcher = self.factory.create_fetcher_by_source_type("rss_sources", config)
        self.assertIsNotNone(fetcher)
        self.assertEqual(fetcher.__class__.__name__, "RSSFetcher")

        # 测试Reddit源
        reddit_config = {
            "name": "Test Reddit",
            "subreddit": "python",
            "enabled": True,
        }
        fetcher = self.factory.create_fetcher_by_source_type("reddit_sources", reddit_config)
        self.assertIsNotNone(fetcher)
        self.assertEqual(fetcher.__class__.__name__, "RedditFetcher")

        # 测试未知源类型（默认回退到RSS）
        fetcher = self.factory.create_fetcher_by_source_type("unknown_sources", config)
        self.assertIsNotNone(fetcher)
        self.assertEqual(fetcher.__class__.__name__, "RSSFetcher")


if __name__ == '__main__':
    unittest.main()