#!/usr/bin/env python3
"""
音声ファイル再生スクリプト
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def play_audio_system(file_path: str):
    """システムのデフォルトプレイヤーで音声を再生"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        subprocess.run(["afplay", file_path])
    elif system == "Linux":
        # 利用可能なプレイヤーを順番に試す
        players = ["aplay", "paplay", "mpv", "vlc"]
        for player in players:
            if subprocess.run(["which", player], capture_output=True).returncode == 0:
                subprocess.run([player, file_path])
                break
        else:
            print("音声プレイヤーが見つかりません")
    elif system == "Windows":
        os.startfile(file_path)
    else:
        print(f"サポートされていないOS: {system}")

def play_audio_pygame(file_path: str):
    """pygameを使用して音声を再生"""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # 再生完了まで待機
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
            
    except ImportError:
        print("pygameがインストールされていません")
        print("インストール: pip install pygame")
    except Exception as e:
        print(f"再生エラー: {e}")

def play_audio_playsound(file_path: str):
    """playsoundを使用して音声を再生"""
    try:
        from playsound import playsound
        playsound(file_path)
    except ImportError:
        print("playsoundがインストールされていません")
        print("インストール: pip install playsound")
    except Exception as e:
        print(f"再生エラー: {e}")

def list_audio_files():
    """現在のディレクトリの音声ファイルを一覧表示"""
    audio_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac']
    audio_files = []
    
    for file in Path('.').iterdir():
        if file.suffix.lower() in audio_extensions:
            audio_files.append(file.name)
    
    return sorted(audio_files)

def main():
    """メイン関数"""
    audio_files = list_audio_files()
    
    if not audio_files:
        print("音声ファイルが見つかりません")
        return
    
    print("利用可能な音声ファイル:")
    for i, file in enumerate(audio_files, 1):
        print(f"{i}. {file}")
    
    if len(sys.argv) > 1:
        # コマンドライン引数でファイル指定
        file_path = sys.argv[1]
    else:
        # インタラクティブに選択
        try:
            choice = int(input("\n再生するファイル番号を選択: ")) - 1
            if 0 <= choice < len(audio_files):
                file_path = audio_files[choice]
            else:
                print("無効な選択です")
                return
        except (ValueError, KeyboardInterrupt):
            print("\n終了します")
            return
    
    if not os.path.exists(file_path):
        print(f"ファイルが見つかりません: {file_path}")
        return
    
    print(f"\n再生中: {file_path}")
    
    # 再生方法を選択
    method = input("再生方法を選択 (1: システム, 2: pygame, 3: playsound) [1]: ").strip()
    
    if method == "2":
        play_audio_pygame(file_path)
    elif method == "3":
        play_audio_playsound(file_path)
    else:
        play_audio_system(file_path)

if __name__ == "__main__":
    main()
