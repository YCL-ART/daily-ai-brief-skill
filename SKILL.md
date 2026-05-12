# AI每日简报技能

## 概述
一个简洁高效的AI新闻简报生成技能，专为Claude Code和OpenClaw优化。每日自动从多个可靠数据源采集AI领域最新动态，生成干净的Markdown格式简报，帮助您快速掌握AI行业前沿信息。

**核心价值**：
- 📰 **真实新闻**: 仅使用真实数据源，无生成内容
- ⚡ **即用即得**: 一键生成，开箱即用
- 🔗 **来源透明**: 每条新闻标注来源和原文链接
- 🎯 **简洁专注**: 去除冗余信息，专注核心内容

## 核心功能

### 智能数据采集
- **多源聚合**: 从8+个AI新闻RSS源实时采集（36氪、MIT Tech Review、TechCrunch等）
- **内容过滤**: 自动过滤广告和低质量内容
- **去重处理**: 智能识别并去除重复新闻
- **时效控制**: 仅保留72小时内的最新新闻

### 简洁报告生成
- **纯真实数据**: 100%真实新闻，零生成内容
- **透明标注**: 每条新闻清晰标注来源和原文链接
- **极简格式**: 移除摘要等冗余信息，专注新闻本身
- **自动保存**: 每日简报自动保存为Markdown文件

### 多平台适配
- **Claude Code原生集成**: 完美融入Claude Code工作流
- **OpenClaw API兼容**: 提供标准化的JSON输出接口
- **独立Python模块**: 可作为通用Python包使用
- **定时任务支持**: 支持每日自动运行

## 使用方法

### 基本使用
```bash
# 生成AI每日简报（自动显示摘要并保存报告）
python daily_brief.py
```

### Python API
```python
from daily_brief import EnhancedAIBrief

# 创建实例
brief = EnhancedAIBrief()

# 生成简报
result = brief.generate_daily_brief()

# 获取摘要
print(brief.get_summary(result))

# 获取完整报告
if result["success"]:
    print(result["report"])
```

### Claude Code集成示例
```python
# 在Claude Code中直接调用
from daily_brief import EnhancedAIBrief

brief = EnhancedAIBrief()
result = brief.generate_daily_brief()

if result["success"]:
    print("🎯 AI每日简报生成成功！")
    print(f"📊 统计信息:")
    print(f"  总条目数: {result.get('total_items', 0)} 条")
    print(f"  新闻来源: {result.get('real_items', 0)} 条")
    print(f"  保存位置: {result.get('filepath', '未知')}")
    
    # 显示简报摘要
    print(brief.get_summary(result))
```

### OpenClaw集成示例
```python
# 在OpenClaw中集成
from daily_brief import EnhancedAIBrief
import datetime

def generate_ai_daily_brief():
    """生成AI每日简报"""
    brief = EnhancedAIBrief()
    result = brief.generate_daily_brief()
    
    if result["success"]:
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "summary": "📰 AI每日简报生成成功",
                "total_items": result.get('total_items', 0),
                "real_items": result.get('real_items', 0),
                "generated_items": result.get('generated_items', 0),
                "filepath": result.get('filepath', '未知'),
                "report_preview": brief.get_summary(result)[:200] + "..." if len(brief.get_summary(result)) > 200 else brief.get_summary(result)
            }
        }
    else:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "message": result.get("error", "未知错误"),
            "details": str(result)
        }

# 调用函数
brief_result = generate_ai_daily_brief()
if brief_result["status"] == "success":
    print("✅ AI简报生成成功")
    print(brief_result["data"]["summary"])
```

## 技术特性

### 数据源架构设计
- **模块化设计**: 可扩展的数据源管理器架构
- **多源支持**: RSS、API、网页爬虫等多种数据源类型
- **缓存机制**: 内置智能缓存系统，减少重复请求
- **错误处理**: 完善的错误处理和重试机制

### 智能内容处理系统
- **内容过滤系统**:
  - 广告内容自动识别和过滤
  - 低质量内容筛选
  - 可配置的过滤规则

### 性能优化
- **缓存管理**: 数据缓存120分钟，减少网络请求
- **并行处理**: 多数据源并行获取，提高效率
- **错误恢复**: 自动重试机制和备用方案

## 项目结构

```
daily-ai-brief-skill/
├── daily_brief.py           # 主程序（增强版）
├── data_source_manager.py   # 数据源管理器
├── config.yaml              # 主配置文件
├── data_sources.yaml        # 数据源配置文件
├── requirements.txt         # 依赖列表
├── SKILL.md                # 本文件
├── README.md               # 详细文档
│
├── test/                   # 测试目录
│   ├── test_data_sources.py        # 数据源测试
│   ├── test_channel_sources.py     # 渠道测试
│   ├── demo_enhanced_features.py   # 功能演示
│   └── run_all_tests.py           # 完整测试套件
│
├── reports/                # 生成的简报文件
└── cache/                 # 数据缓存目录
```

## 配置说明

### 快速配置示例
在Claude Code或OpenClaw中快速使用：

```python
# 最小化配置示例
from daily_brief import EnhancedAIBrief

# 使用默认配置
brief = EnhancedAIBrief()

# 或使用自定义配置
brief = EnhancedAIBrief(
    config_path="my_config.yaml",
    data_source_config="my_data_sources.yaml"
)

# 生成简报
result = brief.generate_daily_brief()
```

### 配置参数
- **auto_save**: 是否自动保存报告（默认：true）
- **format**: 输出格式（默认："markdown"）
- **data_source_config**: 数据源配置文件路径（默认："data_sources.yaml"）

## 输出格式

### Claude Code友好格式
```
🎯 AI每日简报生成成功！
📊 统计信息:
  总条目数: 8 条
  新闻来源: 8 条
  保存位置: ./reports/今日AI简报_2026-05-12.md

📰 今日热点新闻:
1. 🤖 OpenAI发布GPT-4.5新版本
2. 🔬 Google AI在医疗影像诊断取得突破
3. 🛠️ Anthropic开源金融AI全栈模板
```

### OpenClaw友好格式
```json
{
  "status": "success",
  "timestamp": "2026-05-12 14:30:00",
  "data": {
    "total_items": 8,
    "real_items": 8,
    "filepath": "./reports/今日AI简报_2026-05-12.md",
    "summary": "📰 AI每日简报生成成功"
  }
}
```

## 定时任务集成

### Claude Code定时任务
```bash
# 每天上午9点自动生成简报
0 9 * * * cd /path/to/daily-ai-brief-skill && python daily_brief.py

# 每天下午6点更新简报
0 18 * * * cd /path/to/daily-ai-brief-skill && python daily_brief.py
```

### OpenClaw定时任务
在OpenClaw中设置定时任务调用简报生成API。

## 故障排除

### 常见问题
1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install PyYAML feedparser requests beautifulsoup4 lxml
   ```

2. **数据源获取失败**
   ```bash
   # 检查网络连接
   curl https://www.ithome.com/rss/
   ```

3. **配置文件错误**
   - 检查YAML格式是否正确
   - 确保文件编码为UTF-8
   - 验证配置文件路径

### 调试模式
```bash
# 查看数据源状态
python -c "from data_source_manager import DataSourceManager; m = DataSourceManager(); print(m.get_ai_news_summary(max_items=3))"
```

## 扩展开发

### 添加新的数据源
1. 在 `data_sources.yaml` 中添加新的数据源配置
2. 测试数据获取功能

### 集成到其他系统
```python
# 示例：将AI简报集成到工作流系统
def integrate_ai_brief_to_workflow():
    from daily_brief import EnhancedAIBrief
    
    brief = EnhancedAIBrief()
    result = brief.generate_daily_brief()
    
    if result["success"]:
        # 发送到工作流系统
        send_to_workflow_system({
            "type": "ai_daily_brief",
            "content": result,
            "timestamp": datetime.now().isoformat()
        })
        return True
    return False
```

## 许可证
MIT License

## 技术支持
- 问题反馈：检查日志文件
- 功能建议：编辑配置文件
- 定制开发：扩展数据源管理器

---

**技能名称**: AI每日简报  
**版本**: 2.0 (增强版)  
**最后更新**: 2026-05-12  
**状态**: ✅ 生产就绪  
**兼容性**: Claude Code ✅ OpenClaw ✅  
**推荐用途**: 每日AI趋势跟踪、团队技术分享、个人学习参考