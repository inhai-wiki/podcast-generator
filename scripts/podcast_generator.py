#!/usr/bin/env python3
"""
播客生成器 - 基于阿里云百炼通义千问TTS
支持多角色对话、男女混声、自动拼接

使用方法：
    from podcast_generator import PodcastGenerator
    
    generator = PodcastGenerator()
    script = [
        ("F", "大家好！"),
        ("M", "欢迎收听！"),
    ]
    generator.generate(script, output="podcast.wav")
"""

import os
import subprocess
import requests
from typing import List, Tuple, Dict, Optional

# 检查并导入 dashscope
try:
    import dashscope
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
except ImportError:
    raise ImportError("请安装 dashscope: pip install dashscope")


# 默认音色配置
DEFAULT_VOICES = {
    "F": "Cherry",    # 女声 - 温柔甜美
    "M": "Ethan",     # 男声 - 成熟稳重
}

# 可用音色列表
AVAILABLE_VOICES = {
    "Cherry": {"gender": "女", "style": "温柔甜美"},
    "Serena": {"gender": "女", "style": "知性优雅"},
    "Chelsie": {"gender": "女", "style": "活泼可爱"},
    "Ethan": {"gender": "男", "style": "成熟稳重"},
}


class PodcastGenerator:
    """播客生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化播客生成器
        
        Args:
            api_key: 阿里云百炼 API Key，默认从环境变量 DASHSCOPE_API_KEY 获取
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "请设置 DASHSCOPE_API_KEY 环境变量或传入 api_key 参数\n"
                "获取 API Key: https://bailian.console.aliyun.com/?source_channel=github#/api-key"
            )
        
        # 检查 ffmpeg
        if not self._check_ffmpeg():
            raise RuntimeError(
                "未找到 ffmpeg，请先安装:\n"
                "  macOS: brew install ffmpeg\n"
                "  Ubuntu: sudo apt install ffmpeg"
            )
    
    def _check_ffmpeg(self) -> bool:
        """检查 ffmpeg 是否可用"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True)
            return True
        except FileNotFoundError:
            return False
    
    def _synthesize_line(
        self, 
        text: str, 
        voice: str, 
        output_file: str,
        language: str = "Chinese"
    ) -> bool:
        """
        合成单句语音
        
        Args:
            text: 要合成的文本
            voice: 音色名称
            output_file: 输出文件路径
            language: 语种
            
        Returns:
            是否成功
        """
        try:
            response = dashscope.MultiModalConversation.call(
                model="qwen3-tts-flash",
                api_key=self.api_key,
                text=text,
                voice=voice,
                language_type=language
            )
            
            if response.status_code == 200:
                audio_url = response.output.audio.url
                audio_data = requests.get(audio_url).content
                
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                return True
            else:
                print(f"❌ 合成失败: {response.code} - {response.message}")
                return False
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
    
    def _concat_audio(
        self, 
        segment_files: List[str], 
        output_file: str, 
        silence_ms: int = 300
    ) -> bool:
        """
        使用 ffmpeg 拼接音频
        
        Args:
            segment_files: 片段文件列表
            output_file: 输出文件路径
            silence_ms: 片段间的静音时长（毫秒）
            
        Returns:
            是否成功
        """
        list_file = "/tmp/ffmpeg_concat_list.txt"
        silence_file = "/tmp/silence.wav"
        
        # 生成静音文件
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"anullsrc=r=22050:cl=mono:d={silence_ms/1000}",
            "-acodec", "pcm_s16le", silence_file
        ], capture_output=True)
        
        # 写入拼接列表
        with open(list_file, "w") as f:
            for i, seg in enumerate(segment_files):
                f.write(f"file '{seg}'\n")
                if i < len(segment_files) - 1:
                    f.write(f"file '{silence_file}'\n")
        
        # 执行拼接
        result = subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", list_file, "-acodec", "pcm_s16le", output_file
        ], capture_output=True)
        
        return result.returncode == 0
    
    def generate(
        self,
        script: List[Tuple[str, str]],
        output: str = "podcast.wav",
        voices: Optional[Dict[str, str]] = None,
        language: str = "Chinese",
        silence_ms: int = 300,
        verbose: bool = True
    ) -> Optional[str]:
        """
        生成播客音频
        
        Args:
            script: 脚本列表，格式为 [(角色, 台词), ...]
            output: 输出文件路径
            voices: 角色音色映射，如 {"F": "Cherry", "M": "Ethan"}
            language: 语种
            silence_ms: 片段间静音时长（毫秒）
            verbose: 是否显示进度
            
        Returns:
            输出文件路径，失败返回 None
            
        Example:
            script = [
                ("F", "大家好！"),
                ("M", "欢迎收听播客！"),
            ]
            generator.generate(script, output="my_podcast.wav")
        """
        if not script:
            print("❌ 脚本为空")
            return None
        
        # 合并音色配置
        voice_map = {**DEFAULT_VOICES, **(voices or {})}
        
        if verbose:
            print(f"🎙️  开始生成播客")
            print(f"📝 共 {len(script)} 句对话\n")
        
        # 创建临时目录
        temp_dir = "/tmp/podcast_segments"
        os.makedirs(temp_dir, exist_ok=True)
        
        segment_files = []
        
        for i, (speaker, text) in enumerate(script):
            voice = voice_map.get(speaker, "Cherry")
            
            if verbose:
                print(f"  [{i+1:02d}/{len(script)}] {voice}: {text[:25]}...")
            
            output_seg = os.path.join(temp_dir, f"segment_{i:02d}.wav")
            
            if self._synthesize_line(text, voice, output_seg, language):
                segment_files.append(output_seg)
            else:
                print(f"    ⚠️  跳过第 {i+1} 句")
        
        if not segment_files:
            print("❌ 没有成功生成任何片段")
            return None
        
        if verbose:
            print(f"\n🔧 正在拼接 {len(segment_files)} 个片段...")
        
        # 确保输出路径是绝对路径
        if not os.path.isabs(output):
            output = os.path.join(os.getcwd(), output)
        
        if self._concat_audio(segment_files, output, silence_ms):
            file_size = os.path.getsize(output)
            
            # 获取时长
            result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", output
            ], capture_output=True, text=True)
            duration_sec = float(result.stdout.strip()) if result.stdout.strip() else 0
            
            if verbose:
                print(f"\n✅ 播客生成完成！")
                print(f"📁 文件: {output}")
                print(f"⏱️  时长: {int(duration_sec // 60)}分{int(duration_sec % 60)}秒")
                print(f"📊 大小: {file_size / 1024 / 1024:.1f} MB")
            
            return output
        else:
            print("❌ 音频拼接失败")
            return None
    
    @staticmethod
    def list_voices():
        """列出可用音色"""
        print("\n🎤 可用音色列表:\n")
        print(f"{'音色ID':<12} {'性别':<6} {'风格'}")
        print("-" * 35)
        for voice_id, info in AVAILABLE_VOICES.items():
            print(f"{voice_id:<12} {info['gender']:<6} {info['style']}")
        print()


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="播客生成器")
    parser.add_argument("--list-voices", action="store_true", help="列出可用音色")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    
    args = parser.parse_args()
    
    if args.list_voices:
        PodcastGenerator.list_voices()
        return
    
    if args.demo:
        # 演示脚本
        script = [
            ("F", "大家好，欢迎收听本期播客！"),
            ("M", "今天我们来聊一个有趣的话题。"),
            ("F", "好的，让我们开始吧！"),
            ("M", "感谢收听，下期再见！"),
        ]
        
        generator = PodcastGenerator()
        generator.generate(script, output="demo_podcast.wav")
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()

