import os
import re
import json
import discord
import time

def carregar_audios(efeitos_dir):
    audio_files = [f for f in os.listdir(efeitos_dir) if f.endswith(".mp3")]
    return {os.path.splitext(f)[0]: os.path.join(efeitos_dir, f) for f in audio_files}

def associar_emoji_com_audio(emojis_dir, efeitos_dir):
    from src.emoji import carregar_emojis, get_emoji_image

    carregar_emojis(emojis_dir)
    audio_files = [f for f in os.listdir(efeitos_dir) if f.endswith(".mp3")]
    audio_emoji_map = {}
    for audio_file in audio_files:
        audio_name = os.path.splitext(audio_file)[0]
        emoji_path = get_emoji_image(audio_name, emojis_dir)
        audio_emoji_map[audio_name] = emoji_path
    return audio_emoji_map

async def tocar_audio(AUDIO_PATHS, audio_name, voice_client, time_limit_seconds, after=None):
    if voice_client is None or not voice_client.is_connected():
        print("Bot não está conectado a um canal de voz.")
        if after and callable(after):
             try:
                 after(None)
             except Exception as e:
                 print(f"Error in 'after' callback after connection check: {e}")
        return

    if voice_client.is_playing():
        voice_client.stop()

    audio_path = AUDIO_PATHS.get(audio_name)
    if audio_path:
        ffmpeg_options = f"-nostdin -t {time_limit_seconds}"
        source = discord.FFmpegPCMAudio(
            audio_path, before_options=ffmpeg_options, options="-af loudnorm"
        )
        voice_client.play(source, after=after)
        print(f"🔊 Tocando: {audio_name}")
    else:
        print(f"Audio path not found for: {audio_name}")
        if after and callable(after):
            try:
                after(None)
            except Exception as e:
                print(f"Error in 'after' callback after audio path check: {e}")