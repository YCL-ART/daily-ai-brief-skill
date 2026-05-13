"""
测试RSS抓取器
"""
import unittest
import asyncio
from unittest.mock import patch, MagicMock

# 添加模块路径
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.rss_fetcher import RSSFetcher
from modules.base_fetcher import NewsItem


class TestRSSFetcher(unittest.TestCase):
    """测试RSS抓取器"""

    def setUp(self):
        """测试前置设置"""
        self.config = {
            "name": "Test RSS",
            "url": "https://example.com/feed",
            "language": "en",
            "enabled": True,
            "priority": 1,
            "num_items": 5,
        }
        self.fetcher = RSSFetcher(self.config)

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.fetcher.name, "Test RSS")
        self.assertEqual(self.fetcher.url, "https://example.com/feed")
        self.assertEqual(self.fetcher.language, "en")
        self.assertTrue(self.fetcher.enabled)
        self.assertEqual(self.fetcher.priority, 1)
        self.assertEqual(self.fetcher.max_items, 5)

    def test_disabled_fetcher(self):
        """测试禁用的抓取器"""
        config = self.config.copy()
        config["enabled"] = False
        fetcher = RSSFetcher(config)

        # 模拟异步执行
        async def test():
            result = await fetcher.fetch()
            return result

        result = asyncio.run(test())
        self.assertEqual(len(result), 0)

    def test_empty_url(self):
        """测试空URL"""
        config = self.config.copy()
        config["url"] = ""
        fetcher = RSSFetcher(config)

        async def test():
            result = await fetcher.fetch()
            return result

        result = asyncio.run(test())
        self.assertEqual(len(result), 0)

    @patch('modules.rss_fetcher.feedparser.parse')
    def test_fetch_success(self, mock_parse):
        """测试成功抓取"""
        # 模拟feedparser响应
        mock_feed = MagicMock()
        mock_entry = MagicMock()
        mock_entry.title = "Test Article"
        mock_entry.link = "https://example.com/article"
        mock_entry.summary = "Test summary"
        mock_entry.description = "Test description"
        mock_entry.published_parsed = (2026, 5, 13, 10, 30, 0, 0, 0, 0)
        mock_entry.author = "Test Author"
        mock_entry.tags = []
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed

        async def test():
            result = await self.fetcher.fetch()
            return result

        result = asyncio.run(test())

        # 验证结果
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], NewsItem)
        self.assertEqual(result[0].title, "Test Article")
        self.assertEqual(result[0].url, "https://example.com/article")
        self.assertEqual(result[0].source, "Test RSS")

    @patch('modules.rss_fetcher.feedparser.parse')
    def test_fetch_empty_feed(self, mock_parse):
        """测试空订阅"""
        mock_feed = MagicMock()
        mock_feed.entries = []
        mock_parse.return_value = mock_feed

        async def test():
            result = await self.fetcher.fetch()
            return result

        result = asyncio.run(test())
        self.assertEqual(len(result), 0)

    @patch('modules.rss_fetcher.feedparser.parse')
    def test_fetch_exception(self, mock_parse):
        """测试抓取异常"""
        mock_parse.side_effect = Exception("Network error")

        async def test():
            result = await self.fetcher.fetch()
            return result

        result = asyncio.run(test())
        self.assertEqual(len(result), 0)

    def test_apply_filters(self):
        """测试应用过滤器"""
        # 创建测试条目
        items = [
            NewsItem(
                title="AI breakthrough in machine learning",
                url="https://example.com/1",
                content="This is about AI and machine learning",
                source="Test",
                source_type="rss"
            ),
            NewsItem(
                title="Weather forecast for tomorrow",
                url="https://example.com/2",
                content="Sunny with a chance of rain",
                source="Test",
                source_type="rss"
            ),
        ]

        # 测试包含关键词过滤
        config = self.config.copy()
        config["filters"] = {
            "include_keywords": ["AI", "machine learning"]
        }
        fetcher = RSSFetcher(config)

        filtered = fetcher.apply_filters(items)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "AI breakthrough in machine learning")

        # 测试排除关键词过滤
        config["filters"] = {
            "exclude_keywords": ["weather"]
        }
        fetcher = RSSFetcher(config)
        filtered = fetcher.apply_filters(items)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "AI breakthrough in machine learning")

    def test_validate_item(self):
        """测试验证条目"""
        # 有效条目
        valid_item = NewsItem(
            title="Valid Title",
            url="https://example.com/article",
            content="Some content",
            source="Test",
            source_type="rss"
        )
        self.assertTrue(self.fetcher.validate_item(valid_item))

        # 无效标题
        invalid_title = NewsItem(
            title="",  # 空标题
            url="https://example.com/article",
            source="Test",
            source_type="rss"
        )
        self.assertFalse(self.fetcher.validate_item(invalid_title))

        # 无效URL
        invalid_url = NewsItem(
            title="Valid Title",
            url="not-a-url",  # 无效URL
            source="Test",
            source_type="rss"
        )
        self.assertFalse(self.fetcher.validate_item(invalid_url))


if __name__ == '__main__':
    unittest.main()