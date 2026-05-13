#!/usr/bin/env python3
"""
运行所有测试
"""
import unittest
import sys
import os


def discover_and_run_tests():
    """发现并运行测试"""
    # 添加src目录到路径
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    # 发现测试
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('src/test', pattern='test_*.py')

    # 运行测试
    test_runner = unittest.TextTestRunner(verbosity=2, failfast=False)
    result = test_runner.run(test_suite)

    # 返回退出代码
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("运行AI新闻聚合器测试...")
    exit_code = discover_and_run_tests()
    sys.exit(exit_code)