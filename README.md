# 🎙️ Podcast Generator

基于阿里云百炼通义千问TTS的多角色播客生成器。支持男女混声、多角色配音、自动拼接，轻松生成专业级播客音频。

## ✨ 特性

- 🎭 **多角色支持** - 支持多个角色，自由分配音色
- 🔊 **男女混声** - 内置多种音色，支持男女对谈
- 🔗 **自动拼接** - 使用 ffmpeg 无缝拼接音频片段
- ⚡ **简单易用** - 只需定义脚本，一键生成播客
- 🌍 **多语言** - 支持中、英、日、韩等多种语言

## 📦 安装

### 1. 克隆仓库

```bash
git clone <repository-url>
cd podcast-generator
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
```

### 3. 安装 Python 依赖

```bash
pip install dashscope requests
```

### 4. 安装 ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载并添加到 PATH
```

### 5. 配置 API Key

```bash
# 从百炼控制台获取 API Key
# https://bailian.console.aliyun.com/?source_channel=github#/api-key

export DASHSCOPE_API_KEY="sk-your-api-key"
```

## 🚀 快速开始

### 基础用法

```python
from scripts.podcast_generator import PodcastGenerator

# 创建生成器
generator = PodcastGenerator()

# 定义脚本 (角色, 台词)
script = [
    ("F", "大家好，欢迎收听本期播客！"),
    ("M", "今天我们来聊聊人工智能。"),
    ("F", "好的，让我们开始吧！"),
]

# 生成播客
generator.generate(script, output="my_podcast.wav")
```

### 自定义音色

```python
# 自定义角色到音色的映射
voices = {
    "host": "Cherry",      # 主持人 - 温柔女声
    "guest": "Ethan",      # 嘉宾 - 成熟男声
    "narrator": "Serena",  # 旁白 - 知性女声
}

script = [
    ("host", "欢迎来到我们的节目！"),
    ("guest", "很高兴参加这期节目。"),
    ("narrator", "这是一个关于科技的故事..."),
]

generator.generate(script, voices=voices, output="podcast.wav")
```

### 命令行使用

```bash
# 列出可用音色
python scripts/podcast_generator.py --list-voices

# 运行演示
python scripts/podcast_generator.py --demo
```

## 🎤 可用音色

| 音色ID | 性别 | 风格 | 推荐场景 |
|--------|------|------|---------|
| `Cherry` | 女 | 温柔甜美 | 播客主持、情感内容 |
| `Serena` | 女 | 知性优雅 | 新闻播报、专业讲解 |
| `Chelsie` | 女 | 活泼可爱 | 娱乐节目、年轻受众 |
| `Ethan` | 男 | 成熟稳重 | 专业讲解、深度对话 |

## 📁 项目结构

```
podcast-generator/
├── README.md                 # 本文件
├── SKILL.md                  # Claude Skill 说明
├── scripts/
│   └── podcast_generator.py  # 核心生成脚本
├── examples/
│   ├── simple_podcast.py     # 简单示例
│   └── claude_code_intro.py  # Claude Code 介绍播客
└── reference/
    └── voices.md             # 音色参考文档
```

## 📖 示例

### 运行示例

```bash
cd examples

# 简单示例
python simple_podcast.py

# Claude Code 介绍（约2分钟）
python claude_code_intro.py
```

### 示例脚本

参见 `examples/claude_code_intro.py`，这是一个约2分钟的男女对谈播客，介绍 Claude Code。

## ⚙️ API 参数

### `PodcastGenerator.generate()`

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `script` | List[Tuple] | 必填 | 脚本列表 `[(角色, 台词), ...]` |
| `output` | str | `"podcast.wav"` | 输出文件路径 |
| `voices` | Dict | `{"F": "Cherry", "M": "Ethan"}` | 角色音色映射 |
| `language` | str | `"Chinese"` | 语种 |
| `silence_ms` | int | `300` | 片段间静音时长（毫秒）|
| `verbose` | bool | `True` | 是否显示进度 |

## 🌍 支持的语言

- `Chinese` - 中文
- `English` - 英文
- `Japanese` - 日语
- `Korean` - 韩语
- `French` - 法语
- `German` - 德语
- `Spanish` - 西班牙语
- `Auto` - 自动识别

## 📝 编写脚本的技巧

1. **自然对话** - 加入语气词，如"嗯"、"对对对"、"哇"等
2. **控制时长** - 2分钟播客约需300-400字
3. **角色互动** - 设计问答、接话等互动形式
4. **节奏把控** - 长句和短句交替，避免单调
5. **开头结尾** - 设计吸引人的开场和自然的结束语

## ⚠️ 注意事项

- 单次合成最长 **600 字符**，超长台词会被截断
- 生成的音频URL有效期 **24小时**
- API 调用会消耗字符配额，请注意用量
- 确保网络通畅，API 调用需要访问阿里云服务

## 🔗 相关链接

- [阿里云百炼控制台](https://bailian.console.aliyun.com/?source_channel=github)
- [通义千问TTS文档](https://help.aliyun.com/zh/model-studio/developer-reference/cosyvoice-tts?source_channel=github)
- [获取 API Key](https://bailian.console.aliyun.com/?source_channel=github#/api-key)

## 📄 License

MIT License

