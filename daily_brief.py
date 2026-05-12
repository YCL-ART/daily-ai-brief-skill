#!/usr/bin/env python3
"""
增强版AI每日简报生成器
集成真实数据源，从RSS和API获取AI新闻
"""

import os
import sys
import json
import yaml
from datetime import datetime
from typing import Dict, Any, Optional, List
import random

# 导入数据源管理器
try:
    from data_source_manager import DataSourceManager
    DATA_SOURCE_AVAILABLE = True
except ImportError:
    print("⚠️ 数据源管理器不可用，将使用随机生成内容")
    DATA_SOURCE_AVAILABLE = False

class EnhancedAIBrief:
    """增强版AI日报生成器（集成真实数据源）"""
    
    def __init__(self, config_path: Optional[str] = None, data_source_config: Optional[str] = None):
        """初始化"""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.reports_dir = os.path.join(self.base_dir, "reports")
        
        # 创建必要目录
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # 加载简报配置
        self.config = self.load_config(config_path)
        
        # 初始化数据源管理器
        self.data_source_manager = None
        if DATA_SOURCE_AVAILABLE:
            try:
                self.data_source_manager = DataSourceManager(data_source_config)
                print("✅ 数据源管理器初始化成功")
            except Exception as e:
                print(f"⚠️ 数据源管理器初始化失败: {e}")
                self.data_source_manager = None
        
        # 从配置中获取备用数据
        self.ai_topics = self.config.get("topics", [
            "大语言模型进展",
            "AI工具更新", 
            "开源项目发布",
            "AI研究突破",
            "行业应用案例",
            "AI安全与伦理",
            "AI硬件发展",
            "AI政策动态"
        ])
        
        self.ai_models = self.config.get("models", [
            "GPT-4", "Claude 3", "Gemini", "Llama 3", "Mistral",
            "Qwen", "DeepSeek", "Yi", "Baichuan", "通义千问"
        ])
        
        self.companies = self.config.get("companies", [
            "OpenAI", "Anthropic", "Google", "Meta", "Microsoft",
            "阿里云", "腾讯", "百度", "字节跳动", "华为"
        ])
        
        self.generation_config = self.config.get("generation", {
            "num_items": 5,
            "auto_save": True,
            "format": "markdown",
            "use_real_data": True,  # 新增：是否使用真实数据
            "min_real_items": 3,    # 新增：最少真实数据项数
            "fallback_enabled": True  # 新增：是否启用备用生成
        })
    
    def load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(self.base_dir, "config.yaml")
        
        if not os.path.exists(config_path):
            # 返回默认配置
            return {}
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}")
            return {}
    
    def get_real_ai_news(self) -> Dict[str, Any]:
        """从真实数据源获取AI新闻"""
        if not self.data_source_manager:
            return {
                "success": False,
                "error": "数据源管理器不可用",
                "items": [],
                "total": 0
            }
        
        try:
            num_items = self.generation_config.get("num_items", 5)
            summary = self.data_source_manager.get_ai_news_summary(max_items=num_items * 2)
            
            if summary["success"]:
                print(f"✅ 成功获取 {summary['total']} 条真实新闻")
                return summary
            else:
                print(f"⚠️ 真实数据获取失败: {summary.get('error', '未知错误')}")
                return summary
                
        except Exception as e:
            print(f"❌ 真实数据获取异常: {e}")
            return {
                "success": False,
                "error": str(e),
                "items": [],
                "total": 0
            }
    
    def generate_fallback_content(self, num_items: int) -> List[Dict]:
        """生成备用内容（当真实数据不足时）"""
        brief_items = []
        
        # 随机选择话题
        num_topics = min(num_items, len(self.ai_topics))
        if num_topics < 3:
            num_topics = 3
        selected_topics = random.sample(self.ai_topics, num_topics)
        
        for topic in selected_topics:
            # 随机选择模型和公司
            model = random.choice(self.ai_models)
            company = random.choice(self.companies)
            
            # 生成不同类型的简报项
            item_type = random.choice(["update", "release", "research", "application"])
            
            if item_type == "update":
                title = f"{company}发布{model}新版本"
                description = f"{company}宣布推出{model}的最新版本，性能提升显著。"
            elif item_type == "release":
                title = f"新AI工具：{model}助手"
                description = f"基于{model}的新AI助手发布，支持多种任务。"
            elif item_type == "research":
                title = f"{topic}领域新研究"
                description = f"研究人员在{topic}领域取得新突破。"
            else:
                title = f"{company}在{topic}的应用"
                description = f"{company}展示了{model}在{topic}的实际应用案例。"
            
            brief_items.append({
                "title": title,
                "description": description,
                "topic": topic,
                "type": item_type,
                "source": "生成内容",
                "category": self.map_topic_to_category(topic),
                "is_fallback": True
            })
        
        return brief_items
    
    def map_topic_to_category(self, topic: str) -> str:
        """将话题映射到分类"""
        category_map = {
            "大语言模型进展": "模型更新",
            "AI工具更新": "工具更新",
            "开源项目发布": "工具更新",
            "AI研究突破": "研究突破",
            "行业应用案例": "行业动态",
            "AI安全与伦理": "安全伦理",
            "AI硬件发展": "硬件发展",
            "AI政策动态": "行业动态"
        }
        
        return category_map.get(topic, "其他")
    
    def format_news_item(self, item: Dict, index: int) -> str:
        """格式化新闻项"""
        title = item.get("title", "")
        description = item.get("description", "")
        source = item.get("source", "未知来源")
        category = item.get("category", "其他")
        
        # 添加分类标签
        category_emoji = {
            "模型更新": "🤖",
            "研究突破": "🔬",
            "工具更新": "🛠️",
            "行业动态": "📈",
            "安全伦理": "🛡️",
            "硬件发展": "💻"
        }.get(category, "📰")
        
        formatted = f"### {index}. {category_emoji} {title}\n"
        
        if description:
            formatted += f"{description}\n\n"
        
        formatted += f"*来源: {source}*  "
        
        # 添加链接（如果有）
        link = item.get("link", "")
        if link:
            formatted += f"[阅读原文]({link})\n\n"
        else:
            formatted += "\n\n"
        
        return formatted
    
    def generate_daily_brief(self) -> Dict[str, Any]:
        """生成每日AI简报（集成真实数据）"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 检查是否使用真实数据
            use_real_data = self.generation_config.get("use_real_data", True)
            min_real_items = self.generation_config.get("min_real_items", 3)
            fallback_enabled = self.generation_config.get("fallback_enabled", True)
            
            real_news = None
            fallback_items = []
            combined_items = []
            
            # 获取真实数据
            if use_real_data and self.data_source_manager:
                real_news = self.get_real_ai_news()
                
                if real_news.get("success", False):
                    real_items = real_news.get("items", [])
                    
                    # 转换真实数据格式
                    for item in real_items:
                        combined_items.append({
                            "title": item.get("title", ""),
                            "description": item.get("description", ""),
                            "source": item.get("source", "未知"),
                            "category": item.get("category", "其他"),
                            "link": item.get("link", ""),
                            "published": item.get("published", ""),
                            "is_real": True
                        })
            
            # 检查是否需要备用内容
            num_required = self.generation_config.get("num_items", 5)
            
            if len(combined_items) < min_real_items and fallback_enabled:
                print(f"⚠️ 真实数据不足 ({len(combined_items)}/{min_real_items})，使用备用生成")
                
                # 生成备用内容
                num_fallback = num_required - len(combined_items)
                if num_fallback > 0:
                    fallback_items = self.generate_fallback_content(num_fallback)
                    combined_items.extend(fallback_items)
            
            # 如果仍然没有内容，完全使用备用内容
            if not combined_items and fallback_enabled:
                print("⚠️ 无真实数据，完全使用备用生成")
                combined_items = self.generate_fallback_content(num_required)
            
            # 生成Markdown报告
            report = f"# {today} AI每日简报\n\n"
            
            # 添加摘要信息
            real_count = sum(1 for item in combined_items if item.get("is_real", False))
            fallback_count = len(combined_items) - real_count
            
            report += f"## 📊 简报摘要\n\n"
            report += f"- **总条目数**: {len(combined_items)} 条\n"
            report += f"- **真实新闻**: {real_count} 条\n"
            if fallback_count > 0:
                report += f"- **生成内容**: {fallback_count} 条\n"
            report += f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # 添加分类统计
            categories = {}
            for item in combined_items:
                category = item.get("category", "其他")
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            if categories:
                report += f"## 🏷️ 内容分类\n\n"
                for category, count in categories.items():
                    report += f"- **{category}**: {count} 条\n"
                report += "\n"
            
            # 添加详细内容
            report += f"## 📰 今日AI热点\n\n"
            
            for i, item in enumerate(combined_items, 1):
                report += self.format_news_item(item, i)
            
            # 添加趋势分析
            report += f"## 📈 趋势分析\n\n"
            
            # 根据内容生成趋势分析
            if real_count > 0:
                report += "1. **真实新闻覆盖全面**：今日简报包含多个来源的真实AI新闻\n"
                report += "2. **行业动态活跃**：AI技术在各行业应用持续扩展\n"
                report += "3. **技术迭代加速**：大模型和AI工具更新频繁\n"
                report += "4. **安全关注提升**：AI伦理和安全讨论日益重要\n"
            else:
                report += "1. **大模型持续优化**：各大厂商持续改进模型性能\n"
                report += "2. **应用场景扩展**：AI在更多行业找到实际应用\n"
                report += "3. **开源生态活跃**：开源AI项目持续涌现\n"
                report += "4. **安全关注提升**：AI安全与伦理讨论增多\n"
            
            report += "\n"
            
            # 添加建议关注
            report += f"## 💡 建议关注\n\n"
            report += "- 关注主流AI模型的更新动态\n"
            report += "- 探索开源AI工具的实际应用\n"
            report += "- 注意AI应用的合规与安全\n"
            report += "- 关注AI硬件和技术基础设施发展\n\n"
            
            # 添加数据来源说明
            if real_count > 0:
                sources = set()
                for item in combined_items:
                    if item.get("is_real", False):
                        sources.add(item.get("source", "未知"))
                
                if sources:
                    report += f"## 🔗 数据来源\n\n"
                    report += "今日简报数据来自以下来源：\n"
                    for source in sorted(sources):
                        report += f"- {source}\n"
                    report += "\n"
            
            report += f"---\n"
            report += f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
            
            if fallback_count > 0:
                report += f"*注：部分内容为生成示例，实际内容以真实新闻为准*\n"
            elif real_count == 0:
                report += f"*注：此简报为生成示例，建议配置真实数据源获取实际新闻*\n"
            
            # 保存报告
            filename = f"今日AI简报_{today}.md"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            
            return {
                "success": True,
                "has_data": len(combined_items) > 0,
                "total_items": len(combined_items),
                "real_items": real_count,
                "fallback_items": fallback_count,
                "report": report,
                "filepath": filepath,
                "timestamp": datetime.now().isoformat(),
                "used_real_data": real_count > 0
            }
            
        except Exception as e:
            print(f"❌ 简报生成失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "has_data": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_summary(self) -> str:
        """获取简报摘要"""
        result = self.generate_daily_brief()
        
        if not result.get("success", False):
            return f"❌ AI简报生成失败\n原因: {result.get('error', '未知错误')}"
        
        summary = f"📰 AI每日简报（增强版）\n\n"
        
        if result.get("used_real_data", False):
            summary += f"**数据来源**: ✅ 真实数据 + 生成内容\n"
        else:
            summary += f"**数据来源**: ⚠️ 仅生成内容\n"
        
        summary += f"**状态**: ✅ 已生成\n"
        summary += f"**内容数量**: {result.get('total_items', 0)} 条\n"
        
        real_items = result.get("real_items", 0)
        if real_items > 0:
            summary += f"**真实新闻**: {real_items} 条\n"
        
        fallback_items = result.get("fallback_items", 0)
        if fallback_items > 0:
            summary += f"**生成内容**: {fallback_items} 条\n"
        
        summary += f"**保存位置**: {result.get('filepath', '未知')}\n"
        summary += f"**生成时间**: {result.get('timestamp', '未知')}\n\n"
        summary += "使用 `--report` 查看完整内容"
        
        return summary
    
    def show_report(self):
        """显示完整报告"""
        result = self.generate_daily_brief()
        
        if not result.get("success", False):
            print(f"❌ AI简报生成失败\n原因: {result.get('error', '未知错误')}")
            return
        
        print(result.get("report", "报告内容不可用"))

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="增强版AI每日简报生成器（集成真实数据源）")
    parser.add_argument("--summary", action="store_true", help="显示摘要")
    parser.add_argument("--report", action="store_true", help="显示完整报告")
    parser.add_argument("--generate", action="store_true", help="生成简报")
    parser.add_argument("--config", help="指定配置文件路径")
    parser.add_argument("--data-config", help="指定数据源配置文件路径")
    parser.add_argument("--test-data", action="store_true", help="测试数据源功能")
    
    args = parser.parse_args()
    
    # 测试数据源功能
    if args.test_data:
        if DATA_SOURCE_AVAILABLE:
            try:
                from data_source_manager import test_data_sources
                test_data_sources()
            except:
                print("❌ 数据源测试失败")
        else:
            print("❌ 数据源管理器不可用，请安装依赖：pip install feedparser requests beautifulsoup4 lxml")
        return
    
    brief = EnhancedAIBrief(args.config, args.data_config)
    
    if args.summary:
        print(brief.get_summary())
    elif args.report:
        brief.show_report()
    elif args.generate:
        result = brief.generate_daily_brief()
        if result.get("success", False):
            print("✅ AI简报已生成")
            print(f"保存到: {result.get('filepath')}")
            
            if result.get("used_real_data", False):
                print(f"使用了 {result.get('real_items', 0)} 条真实新闻")
            else:
                print("⚠️ 未使用真实数据，请检查数据源配置")
        else:
            print(f"❌ 生成失败: {result.get('error')}")
    else:
        # 默认显示摘要
        print(brief.get_summary())

if __name__ == "__main__":
    main()