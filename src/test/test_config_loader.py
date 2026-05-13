"""
测试配置加载器
"""
import unittest
import os
import tempfile
import yaml

# 添加模块路径
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.config import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """测试配置加载器"""

    def setUp(self):
        """测试前置设置"""
        # 创建临时配置文件
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.yaml')

        test_config = {
            "rss_sources": [
                {
                    "name": "Test RSS",
                    "url": "https://example.com/feed",
                    "language": "en",
                    "enabled": True,
                }
            ],
            "fetch_config": {
                "timeout_seconds": 30,
                "user_agent": "Test Agent",
            }
        }

        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(test_config, f)

    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_load_config(self):
        """测试加载配置"""
        loader = ConfigLoader(self.config_path)
        config = loader.load()

        self.assertIsInstance(config, dict)
        self.assertIn('rss_sources', config)
        self.assertIn('fetch_config', config)

        rss_sources = config['rss_sources']
        self.assertEqual(len(rss_sources), 1)
        self.assertEqual(rss_sources[0]['name'], 'Test RSS')

    def test_get_rss_sources(self):
        """测试获取RSS源"""
        loader = ConfigLoader(self.config_path)
        loader.load()

        rss_sources = loader.get_rss_sources()
        self.assertEqual(len(rss_sources), 1)
        self.assertEqual(rss_sources[0]['name'], 'Test RSS')

    def test_get_fetch_config(self):
        """测试获取抓取配置"""
        loader = ConfigLoader(self.config_path)
        loader.load()

        fetch_config = loader.get_fetch_config()
        self.assertEqual(fetch_config['timeout_seconds'], 30)
        self.assertEqual(fetch_config['user_agent'], 'Test Agent')

    def test_config_file_not_found(self):
        """测试配置文件不存在"""
        loader = ConfigLoader('/nonexistent/path/config.yaml')
        with self.assertRaises(FileNotFoundError):
            loader.load()

    def test_invalid_yaml(self):
        """测试无效YAML"""
        invalid_path = os.path.join(self.temp_dir, 'invalid.yaml')
        with open(invalid_path, 'w', encoding='utf-8') as f:
            f.write('invalid: yaml: : :')

        loader = ConfigLoader(invalid_path)
        with self.assertRaises(ValueError):
            loader.load()


if __name__ == '__main__':
    unittest.main()