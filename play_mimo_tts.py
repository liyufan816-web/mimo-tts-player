#!/usr/bin/env python3
"""
MiMo-V2-TTS 音频播放器
使用方法: python play_mimo_tts.py
"""

import requests
import base64
import io
import os
import sys
from pydub import AudioSegment
from pydub.playback import play

# 配置
# API_KEY = "test"  # 替换成你的真实 API Key
API_KEY = os.getenv("MIMO_API_KEY", "你的测试Key")
API_URL = "https://api.xiaomimimo.com/v1/chat/completions"

def generate_speech(text):
    """调用 MiMo API 生成语音"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mimo-v2-tts",
        "messages": [
            {
                #"role": "user",
                "role": "assistant",
                "content": text
            },
            {
                "role": "assistant",
                "content": "太棒了！"
            }
        ]
    }
    
    print(f"🎤 正在生成语音: {text[:50]}...")
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        audio_base64 = result['choices'][0]['message']['audio']['data']
        print("✅ 语音生成成功！")
        return audio_base64
    else:
        print(f"❌ API 调用失败: {response.status_code}")
        print(response.text)
        return None

def play_audio(audio_base64):
    """播放 Base64 编码的音频"""
    try:
        # 解码 Base64
        audio_bytes = base64.b64decode(audio_base64)
        
        # 加载音频（pydub 会自动识别格式）
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        print("🔊 正在播放...")
        # 播放音频
        play(audio)
        print("✅ 播放完成")
        
    except Exception as e:
        print(f"❌ 播放失败: {e}")
        print("\n💡 提示：如果遇到错误，请确保已安装 ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Ubuntu: sudo apt-get install ffmpeg")

def save_audio(audio_base64, filename="output.mp3"):
    """保存音频到文件"""
    audio_bytes = base64.b64decode(audio_base64)
    with open(filename, 'wb') as f:
        f.write(audio_bytes)
    print(f"💾 音频已保存为: {filename}")

def main():
    print("=" * 50)
    print("🎙️  MiMo-V2-TTS 语音播放器")
    print("=" * 50)
    
    # 测试文本列表
    test_texts = [
        "<style>东北话 开心</style>哎呀妈呀，这也太得劲儿了！",
        "<style>温柔</style>你好，很高兴认识你，今天天气真不错。",
        "<style>悄悄话</style>嘘...告诉你个小秘密，Python 真的很好玩。",
    ]
    
    # 如果命令行提供了参数，使用命令行参数
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        test_texts = [text]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 测试 {i}/{len(test_texts)}")
        
        # 生成语音
        audio_data = generate_speech(text)
        if not audio_data:
            continue
        
        # 保存音频（可选）
        save_audio(audio_data, f"output_{i}.mp3")
        
        # 播放音频
        play_audio(audio_data)
        
        if i < len(test_texts):
            input("\n按 Enter 继续下一个测试...")
    
    print("\n✨ 所有测试完成！")

if __name__ == "__main__":
    main()
