# AI每日简报生成器

一个智能的AI领域简报生成工具，每日生成AI热点和趋势分析报告。

## ✨ 特性

- **智能生成**: 自动分析并生成AI领域热点内容
- **多平台兼容**: 支持OpenClaw、Claude Code、Hermes Agent、Cursor等平台
- **分类清晰**: 内容按专业分类组织，便于阅读
- **格式友好**: 生成标准Markdown格式，易于分享和使用
- **配置灵活**: 支持自定义分类和输出格式

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基本使用
```bash
# 生成今日AI简报
python daily_brief.py --generate

# 显示摘要信息
python daily_brief.py --summary

# 显示完整报告
python daily_brief.py --report
```

## 🔧 API使用

### Python集成
```python
from daily_brief import DailyAIBrief

# 创建实例
brief = DailyAIBrief()

# 生成简报
result = brief.get_brief()

# 获取摘要
summary = brief.get_summary(result)

# 获取完整报告
report = brief.get_formatted_report(result)
```

### 各平台集成示例

#### OpenClaw
```python
from daily_brief import DailyAIBrief

brief = DailyAIBrief()
result = brief.get_brief()
if result["success"]:
    print(brief.get_summary(result))
```

#### Claude Code
```python
# 在Claude Code中直接使用
from daily_brief import DailyAIBrief
brief = DailyAIBrief()
print(brief.get_summary(brief.get_brief()))
```

## ⚙️ 配置说明

### 配置文件
编辑 `brief_config.yaml` 文件:
```yaml
# 分类定义
categories:
  model_updates: "模型更新"
  tech_breakthroughs: "技术突破"
  industry_trends: "行业趋势"

# 输出配置
output:
  format: "markdown"
  max_items_per_category: 10
```

### 内容模板
配置文件中包含内容模板，可以扩展和修改以增加生成内容的多样性。

## 📊 输出示例

### 成功生成时
```
📰 AI每日简报

**平台**: openclaw
**状态**: ✅ 已生成
**内容数量**: 12 条
**内容分类**:
- 模型更新: 3 条
- 技术突破: 2 条
- 行业趋势: 4 条
- 研究论文: 2 条
- 产品动态: 1 条

**生成时间**: 2026-05-11T18:15:00
```

### 完整报告示例
```markdown
# 2026-05-11 AI热点简报

今日AI领域重点关注方向，涵盖5个主要领域

## 模型更新

1. 🔥 **AI模型能力持续提升**
   最新AI模型在复杂任务处理能力上展现显著进步

2. ⭐ **多模态技术优化**
   视觉-语言模型在理解和生成方面取得新进展
```

## 📁 文件结构

```
ai-daily-brief/
├── daily_brief.py          # 主程序入口
├── ai_brief_generator.py   # 简报生成器核心
├── brief_config.yaml       # 配置文件
├── requirements.txt        # 依赖列表
├── README.md              # 本文件
└── briefs/                # 生成的简报文件目录
```

## 🕐 定时任务

### 每日自动运行
```bash
# 每天上午9点自动生成简报
0 9 * * * cd /path/to/ai-daily-brief && python daily_brief.py --generate
```

### 平台特定定时
```bash
# OpenClaw平台定时任务
0 9 * * * cd /path/to/ai-daily-brief && python daily_brief.py --generate

# Claude Code平台定时任务  
0 10 * * * cd /path/to/ai-daily-brief && python daily_brief.py --generate
```

## 🔍 故障排除

### 常见问题
1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install PyYAML
   ```

2. **配置文件错误**
   - 检查YAML格式是否正确
   - 确保文件编码为UTF-8

3. **生成内容较少**
   - 检查配置文件中的分类定义
   - 确认内容模板配置

### 调试模式
```bash
# 查看详细输出
python daily_brief.py --generate --summary 2>&1

# 测试配置文件
python -c "import yaml; print('✅ 配置文件格式正确')"
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交改进建议和功能扩展！