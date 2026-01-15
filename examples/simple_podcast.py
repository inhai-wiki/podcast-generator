#!/usr/bin/env python3
"""
简单播客示例
"""

import sys
sys.path.insert(0, "../scripts")

from podcast_generator import PodcastGenerator

# 创建生成器
generator = PodcastGenerator()

# 定义脚本
script = [
    ("F", "大家好，欢迎收听本期播客！我是小樱。"),
    ("M", "大家好，我是阿森。今天我们来聊聊人工智能。"),
    ("F", "是的，AI现在真的越来越强大了。"),
    ("M", "没错，让我们开始今天的话题吧！"),
    ("F", "好的，感谢大家收听，下期再见！"),
    ("M", "拜拜！"),
]

# 生成播客
generator.generate(
    script=script,
    output="simple_podcast.wav",
    voices={
        "F": "Cherry",  # 女声
        "M": "Ethan",   # 男声
    }
)

