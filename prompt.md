## 项目介绍

AI Daily News Aggregator Skill for OpenClaw, Claude Code & Hermes Agent

## 项目结构框架

```
daily-ai-brief-skill/
├── src/                    # 源码目录
│   ├── test                # 测试脚本目录（生成的测试脚本必须放在此目录）
├── requirements.txt        # 依赖列表
├── SKILL.md                # 技能描述
├── README.md               # 项目描述
└── reports                 # 报告文件存放目录（生成的日报结果必须放在此目录）
```

## 任务步骤

### Step1:
读取[data_sources.yaml](src/data_sources.yaml)，根据不同的信息渠道，生成不同的抓取文件