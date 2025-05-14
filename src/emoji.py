# src\emoji.py
# -*- coding: utf-8 -*-

import os
import re
from PIL import Image

emoji_cache = {}


def carregar_emojis(emojis_dir):
    global emoji_cache
    emoji_cache = {}
    emoji_files = [f for f in os.listdir(emojis_dir) if f.endswith(".png")]
    for emoji_file in emoji_files:
        emoji_name = os.path.splitext(emoji_file)[0].lower()
        emoji_cache[emoji_name] = os.path.join(emojis_dir, emoji_file)


def get_emoji_image(audio_name, emojis_dir):
    audio_words = re.findall(r"[a-zA-Z0-9]+(?:\'[a-zA-Z0-9]+)*", audio_name.lower())
    audio_words.sort(key=len, reverse=True)

    for word in audio_words:
        for emoji_name in emoji_cache:
            if word in emoji_name:
                return emoji_cache[emoji_name]
    return os.path.join(emojis_dir, "speaker.png")
