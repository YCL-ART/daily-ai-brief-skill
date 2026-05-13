"""
报告生成器
将抓取结果保存为文件
"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

from .base_fetcher import NewsItem
from .hotness_evaluator import HotnessEvaluator


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: str = None):
        """
        初始化报告生成器

        Args:
            output_dir: 输出目录，默认为项目根目录下的reports目录
        """
        if output_dir is None:
            # 默认输出目录
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.output_dir = os.path.join(current_dir, "..", "reports")
        else:
            self.output_dir = output_dir

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

        self.logger = logging.getLogger(__name__)
        self.hotness_evaluator = HotnessEvaluator()

    def generate_daily_report(self, items: List[NewsItem]) -> str:
        """
        生成每日报告

        Args:
            items: 新闻条目列表

        Returns:
            报告文件路径
        """
        # 评估热度
        evaluated_items = self.hotness_evaluator.evaluate_all(items)

        # 生成报告文件名
        date_str = datetime.now().strftime("%Y%m%d")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_report_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        # 生成报告内容
        report_content = self.hotness_evaluator.generate_hotness_report(evaluated_items)

        # 添加统计信息
        stats = self._generate_statistics(evaluated_items)
        report_content += "\n\n## 统计信息\n"
        report_content += stats

        # 保存报告
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)

        self.logger.info(f"报告已保存: {filepath}")
        return filepath

    def generate_json_report(self, items: List[NewsItem]) -> str:
        """
        生成JSON格式报告

        Args:
            items: 新闻条目列表

        Returns:
            JSON报告文件路径
        """
        # 评估热度
        evaluated_items = self.hotness_evaluator.evaluate_all(items)

        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_report_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        # 转换为字典列表
        items_dict = [item.to_dict() for item in evaluated_items]

        # 添加元数据
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_items": len(items_dict),
                "source_count": len(set(item["source"] for item in items_dict)),
            },
            "items": items_dict
        }

        # 保存JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)

        self.logger.info(f"JSON报告已保存: {filepath}")
        return filepath

    def generate_summary_report(self, items: List[NewsItem], top_n: int = 10) -> str:
        """
        生成摘要报告（简洁版）

        Args:
            items: 新闻条目列表
            top_n: 显示前N个条目

        Returns:
            摘要报告文件路径
        """
        # 评估热度
        evaluated_items = self.hotness_evaluator.evaluate_all(items)

        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_summary_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        # 生成摘要内容
        summary_lines = []
        summary_lines.append("# AI新闻摘要")
        summary_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append(f"总条目数: {len(evaluated_items)}")
        summary_lines.append("")

        # 按热度分组
        hot_items = [item for item in evaluated_items if item.hotness_score >= 7.0]
        medium_items = [item for item in evaluated_items if 4.0 <= item.hotness_score < 7.0]
        low_items = [item for item in evaluated_items if item.hotness_score < 4.0]

        # 热门新闻
        if hot_items:
            summary_lines.append("## 🔥 热门新闻")
            for i, item in enumerate(hot_items[:top_n], 1):
                summary_lines.append(f"{i}. **{item.title}**")
                summary_lines.append(f"   - 热度: {item.hotness_score:.1f}")
                summary_lines.append(f"   - 来源: {item.source}")
                summary_lines.append(f"   - 链接: {item.url}")
                summary_lines.append("")

        # 中等热度新闻
        if medium_items:
            summary_lines.append("## 📰 一般新闻")
            for i, item in enumerate(medium_items[:top_n], 1):
                summary_lines.append(f"{i}. {item.title}")
                summary_lines.append(f"   - 来源: {item.source}")
                summary_lines.append(f"   - 链接: {item.url}")
                summary_lines.append("")

        # 统计信息
        summary_lines.append("## 📊 统计信息")
        summary_lines.append(f"- 热门新闻（≥7分）: {len(hot_items)} 条")
        summary_lines.append(f"- 一般新闻（4-7分）: {len(medium_items)} 条")
        summary_lines.append(f"- 其他新闻: {len(low_items)} 条")

        # 来源分布
        source_counts = {}
        for item in evaluated_items:
            source_counts[item.source] = source_counts.get(item.source, 0) + 1

        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        summary_lines.append("\n## 📈 热门来源")
        for source, count in top_sources:
            summary_lines.append(f"- {source}: {count} 条")

        # 保存摘要
        summary_content = "\n".join(summary_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        self.logger.info(f"摘要报告已保存: {filepath}")
        return filepath

    def _generate_statistics(self, items: List[NewsItem]) -> str:
        """
        生成统计信息

        Args:
            items: 新闻条目列表

        Returns:
            统计信息文本
        """
        if not items:
            return "无数据"

        # 基本统计
        total_items = len(items)
        hot_items = len([item for item in items if item.hotness_score >= 7.0])

        # 来源统计
        source_counts = {}
        source_type_counts = {}
        language_counts = {}
        for item in items:
            source_counts[item.source] = source_counts.get(item.source, 0) + 1
            source_type_counts[item.source_type] = source_type_counts.get(item.source_type, 0) + 1
            language_counts[item.language] = language_counts.get(item.language, 0) + 1

        # 时间统计
        now = datetime.now()
        recent_24h = len([item for item in items
                         if item.publish_date and (now - item.publish_date).total_seconds() <= 86400])

        # 生成统计文本
        stats_lines = []
        stats_lines.append(f"- 总条目数: {total_items}")
        stats_lines.append(f"- 热门条目（≥7分）: {hot_items}")
        stats_lines.append(f"- 24小时内新闻: {recent_24h}")
        stats_lines.append("")

        stats_lines.append("### 来源分布")
        for source_type, count in sorted(source_type_counts.items(), key=lambda x: x[1], reverse=True):
            stats_lines.append(f"- {source_type}: {count} 条")

        stats_lines.append("")
        stats_lines.append("### 语言分布")
        for language, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True):
            stats_lines.append(f"- {language}: {count} 条")

        stats_lines.append("")
        stats_lines.append("### 热门来源（前5）")
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for source, count in top_sources:
            stats_lines.append(f"- {source}: {count} 条")

        return "\n".join(stats_lines)

    def generate_all_reports(self, items: List[NewsItem]) -> Dict[str, str]:
        """
        生成所有类型的报告

        Args:
            items: 新闻条目列表

        Returns:
            报告文件路径字典
        """
        reports = {}

        try:
            reports["daily"] = self.generate_daily_report(items)
        except Exception as e:
            self.logger.error(f"生成每日报告失败: {e}")

        try:
            reports["json"] = self.generate_json_report(items)
        except Exception as e:
            self.logger.error(f"生成JSON报告失败: {e}")

        try:
            reports["summary"] = self.generate_summary_report(items)
        except Exception as e:
            self.logger.error(f"生成摘要报告失败: {e}")

        return reports