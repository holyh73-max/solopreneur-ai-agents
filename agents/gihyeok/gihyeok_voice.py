import asyncio
import edge_tts
import pygame
import os
import sys
import argparse
import time

# 기획실장 기혁이 전용 차분하고 이성적인 남성 보이스 (HyunsuMultilingualNeural)
VOICE = "ko-KR-HyunsuMultilingualNeural"

async def generate_and_play(text, rate, pitch):
    timestamp = int(time.time())
    output_file = f"gihyeok_voice_{timestamp}.mp3"
    
    # 1. 음성 생성 (edge-tts)
    communicate = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
    await communicate.save(output_file)
    
    # 2. 음성 재생 (pygame)
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload() # 파일 핸들 해제
    finally:
        pygame.mixer.quit()
    
    # 임시 파일 삭제
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gihyeok Voice Engine")
    parser.add_argument("text", nargs="?", default="안녕하십니까, 대표님! 기혁 실장입니다. 📝")
    parser.add_argument("--rate", default="+5%", help="Voice speed (calm but steady)")
    parser.add_argument("--pitch", default="-2Hz", help="Voice pitch (rational and deep)")
    
    args = parser.parse_args()
    asyncio.run(generate_and_play(args.text, args.rate, args.pitch))
