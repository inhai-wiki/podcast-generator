---
name: podcast-generator
description: 使用阿里云百炼通义千问TTS生成男女对谈播客音频；当用户需要生成播客、音频对话、多人配音或语音内容时使用本Skill。
---

# 播客生成器 Skill

## 概述

本 Skill 基于阿里云百炼通义千问TTS（qwen3-tts-flash）模型，实现多角色对话播客的自动生成。支持男女混声、多角色配音、自动拼接等功能。

## 使用场景

当用户提到以下需求时，应触发此 Skill：

- 生成播客/电台节目
- 创建多人对话音频
- 制作男女对谈内容
- 生成语音介绍/教程
- 配音或有声内容制作

## 前置准备

### 1. 获取 API Key

```bash
# 访问百炼控制台获取 API Key
# https://bailian.console.aliyun.com/#/api-key

# 配置环境变量
export DASHSCOPE_API_KEY="sk-your-api-key"
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 Python 依赖
pip install dashscope requests

# 确保安装 ffmpeg（用于音频拼接）
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## 快速开始

### 基础用法

```python
from podcast_generator import PodcastGenerator

# 创建生成器
generator = PodcastGenerator()

# 定义脚本（F=女声, M=男声）
script = [
    ("F", "大家好，欢迎收听本期播客！"),
    ("M", "今天我们来聊一个有趣的话题。"),
    ("F", "让我们开始吧！"),
]

# 生成播客
generator.generate(script, output="my_podcast.wav")
```

### 自定义音色

```python
# 自定义角色音色映射
voices = {
    "host": "Cherry",      # 女主持
    "guest": "Ethan",      # 男嘉宾
    "narrator": "Serena",  # 旁白
}

script = [
    ("host", "欢迎来到我们的节目！"),
    ("guest", "很高兴参加这期节目。"),
    ("narrator", "这是一个关于AI的故事..."),
]

generator.generate(script, voices=voices, output="podcast.wav")
```

## 支持的音色

| 音色ID | 性别 | 风格 |
|--------|------|------|
| `Cherry` | 女 | 温柔甜美 |
| `Serena` | 女 | 知性优雅 |
| `Chelsie` | 女 | 活泼可爱 |
| `Ethan` | 男 | 成熟稳重 |

## 文件结构

```
podcast-generator/
├── SKILL.md              # Skill 说明文档
├── README.md             # 使用说明
├── scripts/
│   └── podcast_generator.py  # 核心生成脚本
├── examples/
│   ├── simple_podcast.py     # 简单示例
│   └── claude_code_intro.py  # Claude Code 介绍播客
└── reference/
    └── voices.md             # 音色参考
```

## 最佳实践

1. **脚本设计**：对话要自然，加入语气词和互动
2. **时长控制**：2分钟播客约300-400字
3. **角色分配**：明确区分不同角色的音色
4. **环境变量**：API Key 使用环境变量，不要硬编码

## 相关链接

- [百炼控制台](https://bailian.console.aliyun.com)
- [通义千问TTS文档](https://help.aliyun.com/zh/model-studio/developer-reference/cosyvoice-tts)

