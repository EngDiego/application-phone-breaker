from src.config_loader import resource_path, load_config, save_config
import pygame
import asyncio
import time
import os
import discord
import sys
import math

from .gif import load_gif_frames
from .audio import carregar_audios, associar_emoji_com_audio, tocar_audio
from .utils import formatar_nome
from .pygame_utils import load_icon, draw_close_button, draw_button, draw_pagination_button

from .constants import (
    BG_COLOR_LOADING,
    TEXT_COLOR_LIGHT,
    CREDITS_APP_NAME,
    CREDITS_DEVELOPER,
    TEXT_COLOR_CREDITS,
    BG_COLOR_SELECTION,
    TEXT_COLOR_DARK,
    SELECTION_BTN_WIDTH,
    SELECTION_BTN_HEIGHT,
    SELECTION_BTN_SPACING,
    SELECTION_BTN_COLOR,
    SELECTION_BTN_TEXT_COLOR,
    SHADOW_COLOR,
    SHADOW_OFFSET,
    BUTTON_BORDER_RADIUS,
    BG_COLOR_MAIN,
    EFFECT_BTN_MIN_WIDTH,
    EFFECT_BTN_HEIGHT,
    EFFECT_BTN_SPACING_X,
    EFFECT_BTN_SPACING_Y,
    EFFECT_BTN_TEXT_COLOR,
    EFFECT_BTN_IDEAL_COLUMNS,
    EMOJI_SIZE_EFFECT_BUTTON,
    EFFECT_BTN_EMOJI_MARGIN_LEFT,
    EMOJI_TEXT_SPACING,
    EFFECT_BTN_TEXT_MARGIN_RIGHT,
    UI_MARGIN,
    HEADER_MARGIN,
    LOADING_GIF_RELATIVE_PATH,
    DEFAULT_EMOJIS_DIR,
    DEFAULT_EFEITOS_DIR,
    LOADING_TEXT_COLOR,
    ICON_RELATIVE_PATH,
    PAGINATION_AREA_HEIGHT,
    PAGINATION_BTN_WIDTH,
    PAGINATION_BTN_HEIGHT,
    PAGINATION_BTN_SPACING,
    PAGINATION_BTN_COLOR,
    PAGINATION_BTN_TEXT_COLOR,
    PAGINATION_BTN_DISABLED_COLOR,
    EFFECT_BTN_PLAYING_COLOR,
    SORT_ALFANUMERIC_ASC,
    SORT_ALFANUMERIC_DESC,
    SORT_OPTIONS,
    DEFAULT_SORT_ORDER,
    SORTING_AREA_HEIGHT,
    SORTING_BTN_WIDTH,
    SORTING_BTN_HEIGHT,
    SORTING_BTN_SPACING,
    SORTING_BTN_COLOR,
    SORTING_BTN_TEXT_COLOR,
    SORTING_BTN_DISABLED_COLOR,
)

SORT_CREATION_TIME_VALUE = "creation_time"

voice_client = None
is_playing_sound_effect = False

ui_config_path = None

async def run_interface(bot, initial_voice_client):
    global voice_client, is_playing_sound_effect, ui_config_path

    ui_config_data, ui_config_path = load_config()
    print(f"DEBUG UI: Loaded config for UI settings from {ui_config_path}")

    time_limit_seconds = ui_config_data.get("VAR_TIME_LIMIT_EFFECT", 5)
    print(f"DEBUG UI: Using VAR_TIME_LIMIT_EFFECT: {time_limit_seconds} seconds")

    voice_client = initial_voice_client

    if not pygame.get_init():
        pygame.init()
        print("✅ Pygame initialized.")
    else:
        print("ℹ️ Pygame already initialized.")

    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 20)

    emoji_font = None
    for font_name in [
        "Segoe UI Emoji",
        "Noto Color Emoji",
        "Apple Color Emoji",
        "Symbola",
        pygame.font.get_default_font(),
    ]:
        try:
            temp_font = pygame.font.SysFont(font_name, font.get_height())
            emoji_font = temp_font
            print(f"✅ Using font '{font_name}' for emojis.")
            break
        except pygame.error:
            pass
        except Exception as e:
            print(f"⚠️ Error trying font '{font_name}': {e}")

    if emoji_font is None:
        print(
            "⚠️ No system font supporting color emojis found. Using default font which may not display them correctly."
        )
        emoji_font = pygame.font.SysFont(None, font.get_height())

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(
        CREDITS_APP_NAME.split(": ")[-1]
    )

    icon_absolute_path = resource_path(ICON_RELATIVE_PATH)

    icon_surface = load_icon(icon_absolute_path)

    if icon_surface:
        try:
            pygame.display.set_icon(icon_surface)
            print("✅ Pygame window icon set.")
        except Exception as e:
            print(f"⚠️ Failed to set Pygame window icon: {e}")
    else:
        print(f"⚠️ Could not load icon surface from {icon_absolute_path}.")

    print("⏱️ Displaying loading screen...")
    loading_gif_path_abs = resource_path(LOADING_GIF_RELATIVE_PATH)
    loading_gif_frames = load_gif_frames(loading_gif_path_abs, size=(100, 100))
    current_frame_gif = 0
    last_frame_time = pygame.time.get_ticks()

    running = True
    loading_error_message = None # Variable to hold error message locally

    while running and not bot.is_ready():
        if bot.error_message: # Check for error message set by main task
            loading_error_message = bot.error_message
            print(f"❗ Displaying error on loading screen: {loading_error_message}")
            # Break the loop condition related to bot readiness, but keep running
            # to allow the user to close the window.
            # We could also just break out of this while loop entirely and show the error...
            # Let's keep the loop running but change display logic.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                fechar_rect = draw_close_button(screen, font)
                if fechar_rect.collidepoint(pos):
                    print("❌ Custom Close Button Clicked during loading.")
                    running = False
                    break

        if not running:
            break

        screen.fill(BG_COLOR_LOADING)

        fechar_rect = draw_close_button(screen, font)

        if loading_error_message:
            # Display the error message
            error_text_surf = font.render(loading_error_message, True, TEXT_COLOR_DARK) # Use dark color for error
            error_text_rect = error_text_surf.get_rect(
                center=(screen_width // 2, screen_height // 2)
            )
            screen.blit(error_text_surf, error_text_rect)
        else:
            # Display normal loading state
            loading_text_surf = font.render("Loading...", True, LOADING_TEXT_COLOR)
            loading_text_rect = loading_text_surf.get_rect(
                center=(screen_width // 2, screen_height // 2 - 80)
            )
            screen.blit(loading_text_surf, loading_text_rect)

            if loading_gif_frames:
                now = pygame.time.get_ticks()
                if 0 <= current_frame_gif < len(loading_gif_frames):
                    frame_surface, frame_duration = loading_gif_frames[current_frame_gif]

                    if now - last_frame_time > frame_duration:
                        last_frame_time = now
                        current_frame_gif = (current_frame_gif + 1) % len(loading_gif_frames)
                        frame_surface, frame_duration = loading_gif_frames[current_frame_gif]

                    gif_rect = frame_surface.get_rect(
                        center=(screen_width // 2, screen_height // 2)
                    )
                    screen.blit(frame_surface, gif_rect)
                else:
                     print("⚠️ Internal error: Invalid GIF frame index detected. Attempting reset.")
                     current_frame_gif = 0
                     if loading_gif_frames:
                         frame_surface, frame_duration = loading_gif_frames[current_frame_gif]
                         gif_rect = frame_surface.get_rect( center=(screen_width // 2, screen_height // 2) )
                         screen.blit(frame_surface, gif_rect)
                     else:
                         waiting_text_surf = font.render("Error loading GIF or no frames.", True, LOADING_TEXT_COLOR)
                         waiting_text_rect = waiting_text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
                         screen.blit(waiting_text_surf, waiting_text_rect)

            else:
                waiting_text_surf = font.render(
                    "Awaiting connection...", True, LOADING_TEXT_COLOR
                )
                waiting_text_rect = waiting_text_surf.get_rect(
                    center=(screen_width // 2, screen_height // 2)
                )
                screen.blit(waiting_text_surf, waiting_text_rect)

        credits_app_surf = small_font.render(CREDITS_APP_NAME, True, TEXT_COLOR_CREDITS)
        credits_dev_surf = small_font.render(
            CREDITS_DEVELOPER, True, TEXT_COLOR_CREDITS
        )

        credits_app_rect = credits_app_surf.get_rect(
            center=(
                screen_width // 2,
                screen_height - UI_MARGIN - credits_dev_surf.get_height() - 5,
            )
        )
        credits_dev_rect = credits_dev_surf.get_rect(
            center=(screen_width // 2, screen_height - UI_MARGIN)
        )

        screen.blit(credits_app_surf, credits_app_rect)
        screen.blit(credits_dev_surf, credits_dev_rect)

        pygame.display.update()

        await asyncio.sleep(0.01)

    # If we exited the loop because of an error message, the user needs to close it.
    # If we exited because bot.is_ready() became True, continue to next screen.
    if loading_error_message and running:
        print("Entering error display loop. User must close window.")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    fechar_rect = draw_close_button(screen, font)
                    if fechar_rect.collidepoint(pos):
                        print("❌ Custom Close Button Clicked on error screen.")
                        running = False
                        break
            pygame.display.update()
            await asyncio.sleep(0.01)


    if not running:
        print("🚪 Exiting after closing on loading/error screen.")
        pass # Program will exit via the main loop finishing


    # --- Guild Selection Screen ---
    selected_guild = None
    current_page_guild = 0

    if running and bot.is_ready(): # Only proceed if bot is ready and not exiting
        while running and not selected_guild:
            screen.fill(BG_COLOR_SELECTION)

            server_text_surf = font.render("Select a Server", True, TEXT_COLOR_DARK)
            server_text_rect = server_text_surf.get_rect(
                center=(screen.get_width() // 2, HEADER_MARGIN)
            )
            screen.blit(server_text_surf, server_text_rect)

            fechar_rect = draw_close_button(screen, font)

            guilds_to_display = bot.guilds

            if not guilds_to_display:
                text_no_guilds = font.render("No guilds found.", True, TEXT_COLOR_DARK)
                text_no_guilds_rect = text_no_guilds.get_rect(
                    center=(screen.get_width() // 2, screen.get_height() // 2)
                )
                screen.blit(text_no_guilds, text_no_guilds_rect)
                total_guilds = 0
                total_pages_guild = 1
                guild_button_rects = []
                prev_btn_rect_guild = None
                next_btn_rect_guild = None

            else:
                total_guilds = len(guilds_to_display)

                width, height = screen.get_size()
                selection_area_top = fechar_rect.bottom + HEADER_MARGIN
                selection_area_bottom = height - UI_MARGIN - PAGINATION_AREA_HEIGHT
                available_height_for_selection = selection_area_bottom - selection_area_top

                if available_height_for_selection < SELECTION_BTN_HEIGHT: available_height_for_selection = SELECTION_BTN_HEIGHT

                if (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING) > 0:
                     rows_per_page_guild = max(1, (available_height_for_selection + SELECTION_BTN_SPACING) // (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING))
                else:
                     rows_per_page_guild = 1

                columns_guild = 1
                button_width_guild = SELECTION_BTN_WIDTH

                buttons_per_page_guild = columns_guild * rows_per_page_guild
                if buttons_per_page_guild <= 0: buttons_per_page_guild = 1

                total_pages_guild = math.ceil(total_guilds / buttons_per_page_guild) if total_guilds > 0 else 1
                if total_pages_guild <= 0: total_pages_guild = 1

                if current_page_guild >= total_pages_guild:
                     current_page_guild = total_pages_guild - 1
                     if current_page_guild < 0: current_page_guild = 0

                start_index_guild = current_page_guild * buttons_per_page_guild
                end_index_guild = min(start_index_guild + buttons_per_page_guild, total_guilds)
                guilds_on_this_page = guilds_to_display[start_index_guild:end_index_guild]

                if len(guilds_on_this_page) > 0:
                     guild_grid_required_height = len(guilds_on_this_page) * (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING) - SELECTION_BTN_SPACING
                     if len(guilds_on_this_page) == 1: guild_grid_required_height = SELECTION_BTN_HEIGHT
                else:
                     guild_grid_required_height = 0

                guild_grid_start_y = selection_area_top + (available_height_for_selection - guild_grid_required_height) // 2
                guild_grid_start_y = max(guild_grid_start_y, selection_area_top + UI_MARGIN)

                guild_grid_start_x = (width - button_width_guild) // 2

                guild_button_rects = []

                for i, guild in enumerate(guilds_on_this_page):
                    col = 0
                    row = i

                    x = guild_grid_start_x + col * (button_width_guild + SELECTION_BTN_SPACING)
                    y = guild_grid_start_y + row * (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING)

                    rect = pygame.Rect(x, y, button_width_guild, SELECTION_BTN_HEIGHT)
                    guild_button_rects.append((rect, guild))

                    draw_button(
                        screen,
                        rect,
                        guild.name,
                        font,
                        SELECTION_BTN_COLOR,
                        SELECTION_BTN_TEXT_COLOR,
                        border_radius=BUTTON_BORDER_RADIUS,
                        shadow_color=SHADOW_COLOR,
                        shadow_offset=SHADOW_OFFSET
                    )

                pagination_y = height - UI_MARGIN - PAGINATION_BTN_HEIGHT
                pagination_area_center_y = pagination_y + PAGINATION_BTN_HEIGHT // 2

                prev_btn_rect_guild = None
                next_btn_rect_guild = None

                if current_page_guild > 0 and total_pages_guild > 1:
                    prev_btn_x = UI_MARGIN
                    prev_btn_rect_guild = pygame.Rect(prev_btn_x, pagination_y, PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT)
                    draw_pagination_button(screen, prev_btn_rect_guild, "< Anterior", font, enabled=True)

                if current_page_guild < total_pages_guild - 1 and total_pages_guild > 1:
                     next_btn_x = width - UI_MARGIN - PAGINATION_BTN_WIDTH
                     next_btn_rect_guild = pygame.Rect(next_btn_x, pagination_y, PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT)
                     draw_pagination_button(screen, next_btn_rect_guild, "Próximo >", font, enabled=True)

                page_info_text_guild = f"Página {current_page_guild + 1}/{total_pages_guild}"
                page_info_surface_guild = font.render(page_info_text_guild, True, TEXT_COLOR_DARK)
                page_info_rect_guild = page_info_surface_guild.get_rect(center=(width // 2, pagination_area_center_y))
                screen.blit(page_info_surface_guild, page_info_rect_guild)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    fechar_rect = draw_close_button(screen, font)
                    if fechar_rect.collidepoint(pos):
                        print("❌ Custom Close Button Clicked.")
                        running = False
                        break

                    if prev_btn_rect_guild and prev_btn_rect_guild.collidepoint(pos):
                         current_page_guild -= 1
                         print(f"➡️ Guilds: Moving to page {current_page_guild + 1}/{total_pages_guild}")
                         break

                    if next_btn_rect_guild and next_btn_rect_guild.collidepoint(pos):
                         current_page_guild += 1
                         print(f"➡️ Guilds: Moving to page {current_page_guild + 1}/{total_pages_guild}")
                         break

                    if running:
                         for rect, guild in guild_button_rects:
                             if rect.collidepoint(pos):
                                 selected_guild = guild
                                 print(f"✅ Guild selected: {guild.name}")
                                 break

            if not running:
                break

            await asyncio.sleep(0.01)

    if not running:
        print("🚪 Exiting after closing on guild selection screen.")
        pass


    # --- Channel Selection Screen ---
    selected_channel = None
    current_page_channel = 0

    if selected_guild and running:
        voice_channels_full_list = [
            c
            for c in selected_guild.voice_channels
            if c.permissions_for(selected_guild.me).connect
        ]
        total_channels = len(voice_channels_full_list)

        while running and not selected_channel:
            screen.fill(BG_COLOR_SELECTION)

            channel_text_surf = font.render(
                "Select a Voice Channel", True, TEXT_COLOR_DARK
            )
            channel_text_rect = channel_text_surf.get_rect(
                center=(screen.get_width() // 2, HEADER_MARGIN)
            )
            screen.blit(channel_text_surf, channel_text_rect)

            fechar_rect = draw_close_button(screen, font)


            if not voice_channels_full_list:
                text_no_channels = font.render(
                    f"No voice channels where the bot can connect in '{selected_guild.name}'.",
                    True,
                    TEXT_COLOR_DARK,
                )
                text_no_channels_rect = text_no_channels.get_rect(
                    center=(screen.get_width() // 2, screen.get_height() // 2)
                )
                screen.blit(text_no_channels, text_no_channels_rect)
                total_channels = 0
                total_pages_channel = 1
                channel_button_rects = []
                prev_btn_rect_channel = None
                next_btn_rect_channel = None

            else:
                total_channels = len(voice_channels_full_list)

                width, height = screen.get_size()
                selection_area_top = fechar_rect.bottom + HEADER_MARGIN
                selection_area_bottom = height - UI_MARGIN - PAGINATION_AREA_HEIGHT
                available_height_for_selection = selection_area_bottom - selection_area_top

                if available_height_for_selection < SELECTION_BTN_HEIGHT: available_height_for_selection = SELECTION_BTN_HEIGHT

                if (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING) > 0:
                     rows_per_page_channel = max(1, (available_height_for_selection + SELECTION_BTN_SPACING) // (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING))
                else:
                     rows_per_page_channel = 1

                columns_channel = 1
                button_width_channel = SELECTION_BTN_WIDTH

                buttons_per_page_channel = columns_channel * rows_per_page_channel
                if buttons_per_page_channel <= 0: buttons_per_page_channel = 1

                total_pages_channel = math.ceil(total_channels / buttons_per_page_channel) if total_channels > 0 else 1
                if total_pages_channel <= 0: total_pages_channel = 1

                if current_page_channel >= total_pages_channel:
                    current_page_channel = total_pages_channel - 1
                    if current_page_channel < 0: current_page_channel = 0

                start_index_channel = current_page_channel * buttons_per_page_channel
                end_index_channel = min(start_index_channel + buttons_per_page_channel, total_channels)
                channels_on_this_page = voice_channels_full_list[start_index_channel:end_index_channel]

                if len(channels_on_this_page) > 0:
                    channel_grid_required_height = len(channels_on_this_page) * (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING) - SELECTION_BTN_SPACING
                    if len(channels_on_this_page) == 1: channel_grid_required_height = SELECTION_BTN_HEIGHT
                else:
                    channel_grid_required_height = 0

                channel_grid_start_y = selection_area_top + (available_height_for_selection - channel_grid_required_height) // 2
                channel_grid_start_y = max(channel_grid_start_y, selection_area_top + UI_MARGIN)

                channel_grid_start_x = (width - button_width_channel) // 2

                channel_button_rects = []

                for i, channel in enumerate(channels_on_this_page):
                    col = 0
                    row = i

                    x = channel_grid_start_x + col * (button_width_channel + SELECTION_BTN_SPACING)
                    y = channel_grid_start_y + row * (SELECTION_BTN_HEIGHT + SELECTION_BTN_SPACING)

                    rect = pygame.Rect(x, y, button_width_channel, SELECTION_BTN_HEIGHT)
                    channel_button_rects.append((rect, channel))

                    draw_button(
                        screen,
                        rect,
                        channel.name,
                        font,
                        SELECTION_BTN_COLOR,
                        SELECTION_BTN_TEXT_COLOR,
                        border_radius=BUTTON_BORDER_RADIUS,
                        shadow_color=SHADOW_COLOR,
                        shadow_offset=SHADOW_OFFSET
                    )

                pagination_y = height - UI_MARGIN - PAGINATION_BTN_HEIGHT
                pagination_area_center_y = pagination_y + PAGINATION_BTN_HEIGHT // 2

                prev_btn_rect_channel = None
                next_btn_rect_channel = None

                if current_page_channel > 0 and total_pages_channel > 1:
                     prev_btn_x = UI_MARGIN
                     prev_btn_rect_channel = pygame.Rect(prev_btn_x, pagination_y, PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT)
                     draw_pagination_button(screen, prev_btn_rect_channel, "< Anterior", font, enabled=True)

                if current_page_channel < total_pages_channel - 1 and total_pages_channel > 1:
                      next_btn_x = width - UI_MARGIN - PAGINATION_BTN_WIDTH
                      next_btn_rect_channel = pygame.Rect(next_btn_x, pagination_y, PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT)
                      draw_pagination_button(screen, next_btn_rect_channel, "Próximo >", font, enabled=True)

                page_info_text_channel = f"Página {current_page_channel + 1}/{total_pages_channel}"
                page_info_surface_channel = font.render(page_info_text_channel, True, TEXT_COLOR_DARK)
                page_info_rect_channel = page_info_surface_channel.get_rect(center=(width // 2, pagination_area_center_y))
                screen.blit(page_info_surface_channel, page_info_rect_channel)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    fechar_rect = draw_close_button(screen, font)
                    if fechar_rect.collidepoint(pos):
                        print("❌ Custom Close Button Clicked.")
                        running = False
                        break

                    if prev_btn_rect_channel and prev_btn_rect_channel.collidepoint(pos):
                         current_page_channel -= 1
                         print(f"➡️ Channels: Moving to page {current_page_channel + 1}/{total_pages_channel}")
                         break

                    if next_btn_rect_channel and next_btn_rect_channel.collidepoint(pos):
                         current_page_channel += 1
                         print(f"➡️ Channels: Moving to page {current_page_channel + 1}/{total_pages_channel}")
                         break

                    if running:
                        for rect, channel in channel_button_rects:
                             if rect.collidepoint(pos):
                                 selected_channel = channel
                                 print(f"✅ Channel selected: {channel.name}")
                                 break

            if not running:
                break

            await asyncio.sleep(0.01)

    # --- Voice Channel Connection ---
    if selected_channel and running:
        try:
            if voice_client and voice_client.is_connected():
                print(f"🎤 Disconnecting from previous channel...")
                try:
                    await voice_client.disconnect()
                    print("✅ Disconnected.")
                except Exception as e:
                     print(f"⚠️ Error during prior disconnect: {e}")
                voice_client = None

            print(f"🎤 Connecting to channel: {selected_channel.name}...")
            voice_client = await asyncio.wait_for(
                selected_channel.connect(),
                timeout=10.0
            )
            print(f"🔊 Connected to channel: {selected_channel.name}")
        except asyncio.TimeoutError:
             print("⏰ Timeout connecting to voice channel.")
             voice_client = None
             running = False # Exit UI if voice connection fails here
        except discord.errors.ClientException as e:
            print(f"🚫 Error connecting to voice channel (ClientException): {e}")
            voice_client = None
            running = False # Exit UI if voice connection fails here
        except Exception as e:
            print(f"❌ Unexpected error connecting to voice channel: {e}")
            voice_client = None
            running = False # Exit UI if voice connection fails here


    # --- Main Interface Screen ---
    if voice_client and voice_client.is_connected() and running:

        effects_folder_name = ui_config_data.get("EFEITOS_DIR", DEFAULT_EFEITOS_DIR)
        emojis_folder_name = ui_config_data.get("EMOJIS_DIR", DEFAULT_EMOJIS_DIR)

        efeitos_dir_abs = resource_path(effects_folder_name)
        emojis_dir_abs = resource_path(emojis_folder_name)

        print(f"DEBUG: Attempting to load audios from: {efeitos_dir_abs}")

        AUDIO_PATHS = carregar_audios(efeitos_dir_abs)
        button_names_list = list(AUDIO_PATHS.keys())
        total_buttons = len(button_names_list)
        print(f"🎶 Loaded {total_buttons} sound effects.")

        def custom_sort_key(item):
            if not item:
                return (3, '')

            first_char = item[0]

            if first_char.isalpha():
                return (0, item.lower())
            elif first_char.isdigit():
                return (1, item.lower())
            else:
                return (2, item.lower())

        def apply_sorting(names_list, sort_method, audio_file_paths):

            if sort_method == SORT_ALFANUMERIC_ASC:
                names_list.sort(key=custom_sort_key)
            elif sort_method == SORT_ALFANUMERIC_DESC:
                names_list.sort(key=custom_sort_key)
                names_list.reverse()

            elif sort_method == SORT_CREATION_TIME_VALUE:
                def ctime_sort_key(item_name):
                    try:
                         file_path = audio_file_paths.get(item_name)
                         if file_path and os.path.exists(file_path):
                             ctime = os.path.getctime(file_path)
                             key = (ctime, item_name.lower())
                             return key
                         else:
                             key = (float('inf'), item_name.lower())
                             return key
                    except Exception as e:
                         print(f"⚠️ Error getting creation time for {item_name}: {e}")
                         key = (float('inf'), item_name.lower())
                         return key

                names_list.sort(key=ctime_sort_key, reverse=True)

            else:
                 print(f"⚠️ Unknown sort method '{sort_method}', defaulting to {DEFAULT_SORT_ORDER}")
                 names_list.sort(key=custom_sort_key)

        current_sort_method = ui_config_data.get("VAR_ORDER", DEFAULT_SORT_ORDER)
        valid_sort_methods = [opt[0] for opt in SORT_OPTIONS]
        if current_sort_method not in valid_sort_methods:
            print(f"⚠️ Invalid sort method '{current_sort_method}' found in config. Using default: {DEFAULT_SORT_ORDER}")
            current_sort_method = DEFAULT_SORT_ORDER
            ui_config_data["VAR_ORDER"] = current_sort_method
            if ui_config_path:
                 save_config(ui_config_data, ui_config_path)

        apply_sorting(button_names_list, current_sort_method, AUDIO_PATHS)
        print(f"✅ Initial sort order applied: {current_sort_method}")

        print(f"DEBUG: Attempting to load emojis from: {emojis_dir_abs}")
        button_emoji_map = associar_emoji_com_audio(
            emojis_dir_abs, efeitos_dir_abs
        )
        print(f"✨ Associated {len(button_emoji_map)} emojis with buttons.")

        def after_playback_callback(error):
            global is_playing_sound_effect
            is_playing_sound_effect = False
            if error:
                print(f"⚠️ Player error: {error}")

        current_page_effects = 0

        while running:
            screen.fill(BG_COLOR_MAIN)

            fechar_rect = draw_close_button(screen, font)

            width, height = screen.get_size()

            grid_area_top = fechar_rect.bottom + HEADER_MARGIN + SORTING_AREA_HEIGHT
            grid_area_bottom = height - UI_MARGIN - PAGINATION_AREA_HEIGHT
            available_height_for_grid = grid_area_bottom - grid_area_top
            available_width_for_grid = width - UI_MARGIN * 2

            if available_height_for_grid < EFFECT_BTN_HEIGHT: available_height_for_grid = EFFECT_BTN_HEIGHT
            if available_width_for_grid < EFFECT_BTN_MIN_WIDTH: available_width_for_grid = EFFECT_BTN_MIN_WIDTH

            calculated_button_width_for_ideal_cols = (available_width_for_grid - EFFECT_BTN_SPACING_X * (EFFECT_BTN_IDEAL_COLUMNS - 1)) // EFFECT_BTN_IDEAL_COLUMNS if EFFECT_BTN_IDEAL_COLUMNS > 0 else available_width_for_grid

            if calculated_button_width_for_ideal_cols >= EFFECT_BTN_MIN_WIDTH:
                 columns = EFFECT_BTN_IDEAL_COLUMNS
                 button_width = calculated_button_width_for_ideal_cols
            else:
                 max_columns = max(1, (available_width_for_grid + EFFECT_BTN_SPACING_X) // (EFFECT_BTN_MIN_WIDTH + EFFECT_BTN_SPACING_X))
                 columns = max_columns

                 if columns == 1:
                      button_width = available_width_for_grid
                 else:
                      button_width = (available_width_for_grid - EFFECT_BTN_SPACING_X * (columns - 1)) // columns

                 button_width = max(button_width, EFFECT_BTN_MIN_WIDTH)

            if (EFFECT_BTN_HEIGHT + EFFECT_BTN_SPACING_Y) > 0:
                max_rows_that_fit = max(1, (available_height_for_grid + EFFECT_BTN_SPACING_Y) // (EFFECT_BTN_HEIGHT + EFFECT_BTN_SPACING_Y))
            else:
                max_rows_that_fit = 1

            rows_per_page = max_rows_that_fit

            buttons_per_page_effects = columns * rows_per_page

            if buttons_per_page_effects <= 0: buttons_per_page_effects = 1
            if total_buttons == 0: buttons_per_page_effects = 1

            total_pages_effects = math.ceil(total_buttons / buttons_per_page_effects) if buttons_per_page_effects > 0 and total_buttons > 0 else 1
            if total_pages_effects <= 0: total_pages_effects = 1

            if current_page_effects >= total_pages_effects:
                 current_page_effects = total_pages_effects - 1
                 if current_page_effects < 0: current_page_effects = 0

            total_columns_width = columns * button_width + (columns - 1) * EFFECT_BTN_SPACING_X
            grid_start_x = (width - total_columns_width) // 2
            grid_start_x = max(UI_MARGIN, grid_start_x)

            grid_required_height = rows_per_page * (EFFECT_BTN_HEIGHT + EFFECT_BTN_SPACING_Y) - EFFECT_BTN_SPACING_Y
            if rows_per_page <= 0: grid_required_height = 0
            elif rows_per_page == 1: grid_required_height = EFFECT_BTN_HEIGHT

            grid_start_y = grid_area_top + (available_height_for_grid - grid_required_height) // 2
            grid_start_y = max(grid_start_y, grid_area_top + UI_MARGIN)
            grid_start_y = min(grid_start_y, grid_area_bottom - grid_required_height)

            start_index_effects = current_page_effects * buttons_per_page_effects
            end_index_effects = min(start_index_effects + buttons_per_page_effects, total_buttons)
            buttons_to_display = button_names_list[start_index_effects:end_index_effects]

            sound_button_rects = []

            for i, name in enumerate(buttons_to_display):
                col = i % columns
                row = i // columns

                x = grid_start_x + col * (button_width + EFFECT_BTN_SPACING_X)
                y = grid_start_y + row * (EFFECT_BTN_HEIGHT + EFFECT_BTN_SPACING_Y)

                rect = pygame.Rect(x, y, button_width, EFFECT_BTN_HEIGHT)
                sound_button_rects.append((rect, name))

                current_button_color = (
                    SELECTION_BTN_COLOR if not is_playing_sound_effect else EFFECT_BTN_PLAYING_COLOR
                )

                draw_button(
                    screen, rect, "", font,
                    current_button_color, EFFECT_BTN_TEXT_COLOR,
                    border_radius=BUTTON_BORDER_RADIUS, shadow_color=SHADOW_COLOR, shadow_offset=SHADOW_OFFSET
                )

                emoji_path_resolved = button_emoji_map.get(name)
                default_bundled_emoji_path = resource_path(os.path.join(DEFAULT_EMOJIS_DIR, "speaker.png"))

                final_emoji_to_load = None
                if emoji_path_resolved and os.path.exists(emoji_path_resolved):
                    final_emoji_to_load = emoji_path_resolved
                elif os.path.exists(default_bundled_emoji_path):
                    final_emoji_to_load = default_bundled_emoji_path
                else:
                    pass

                emoji_drawn = False
                text_x_start = rect.x + EFFECT_BTN_EMOJI_MARGIN_LEFT

                if final_emoji_to_load:
                    try:
                        emoji_img_surface = pygame.image.load(final_emoji_to_load).convert_alpha()
                        emoji_img_surface = pygame.transform.scale(emoji_img_surface, (EMOJI_SIZE_EFFECT_BUTTON, EMOJI_SIZE_EFFECT_BUTTON))
                        emoji_x = rect.x + EFFECT_BTN_EMOJI_MARGIN_LEFT
                        emoji_y = rect.y + (rect.height - emoji_img_surface.get_height()) // 2
                        screen.blit(emoji_img_surface, (emoji_x, emoji_y))
                        emoji_drawn = True
                        text_x_start = emoji_x + EMOJI_SIZE_EFFECT_BUTTON + EMOJI_TEXT_SPACING
                    except Exception as e:
                        text_x_start = rect.x + EFFECT_BTN_EMOJI_MARGIN_LEFT

                texto_curto = formatar_nome(name)
                text_surface = font.render(texto_curto, True, EFFECT_BTN_TEXT_COLOR)
                text_y = rect.y + (rect.height - text_surface.get_height()) // 2
                text_available_width = rect.width - (text_x_start - rect.x) - EFFECT_BTN_TEXT_MARGIN_RIGHT
                text_available_width = max(0, text_available_width)

                if text_surface.get_width() < text_available_width:
                    text_x = text_x_start + (text_available_width - text_surface.get_width()) // 2
                else:
                    text_x = text_x_start

                text_x = max(text_x, text_x_start)

                screen.blit(text_surface, (text_x, text_y))

            sorting_y = fechar_rect.bottom + HEADER_MARGIN + UI_MARGIN
            total_sorting_buttons_width = len(SORT_OPTIONS) * SORTING_BTN_WIDTH + (len(SORT_OPTIONS) - 1) * SORTING_BTN_SPACING
            sorting_start_x = (width - total_sorting_buttons_width) // 2
            sorting_start_x = max(UI_MARGIN, sorting_start_x)

            sorting_button_rects = []

            current_btn_x = sorting_start_x
            for sort_value, sort_text in SORT_OPTIONS:
                 rect = pygame.Rect(current_btn_x, sorting_y, SORTING_BTN_WIDTH, SORTING_BTN_HEIGHT)
                 sorting_button_rects.append((rect, sort_value))

                 btn_color = SORTING_BTN_COLOR
                 btn_text_color = SORTING_BTN_TEXT_COLOR
                 if sort_value == current_sort_method:
                      btn_color = (int(SORTING_BTN_COLOR[0] * 0.7), int(SORTING_BTN_COLOR[1] * 0.7), int(SORTING_BTN_COLOR[2] * 0.7))

                 draw_button(
                      screen, rect, sort_text, small_font,
                      btn_color, btn_text_color,
                      border_radius=BUTTON_BORDER_RADIUS, shadow_color=SHADOW_COLOR, shadow_offset=SHADOW_OFFSET
                 )
                 current_btn_x += SORTING_BTN_WIDTH + SORTING_BTN_SPACING

            pagination_y = height - UI_MARGIN - PAGINATION_BTN_HEIGHT
            pagination_area_center_y = pagination_y + PAGINATION_BTN_HEIGHT // 2

            prev_btn_rect_effects = None
            next_btn_rect_effects = None

            if current_page_effects > 0 and total_pages_effects > 1:
                prev_btn_x = UI_MARGIN
                prev_btn_rect_effects = pygame.Rect(prev_btn_x, pagination_y, PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT)
                draw_pagination_button(screen, prev_btn_rect_effects, "< Anterior", font, enabled=True)

            if current_page_effects < total_pages_effects - 1 and total_pages_effects > 1:
                 next_btn_x = width - UI_MARGIN - PAGINATION_BTN_WIDTH
                 next_btn_rect_effects = pygame.Rect(next_btn_x, pagination_y, PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT)
                 draw_pagination_button(screen, next_btn_rect_effects, "Próximo >", font, enabled=True)

            page_info_text_effects = f"Página {current_page_effects + 1}/{total_pages_effects}"
            page_info_surface_effects = font.render(page_info_text_effects, True, TEXT_COLOR_DARK)
            page_info_rect_effects = page_info_surface_effects.get_rect(center=(width // 2, pagination_area_center_y))
            screen.blit(page_info_surface_effects, page_info_rect_effects)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    fechar_rect = draw_close_button(screen, font)
                    if fechar_rect.collidepoint(pos):
                        print("❌ Custom Close Button Clicked.")
                        running = False
                        break

                    for rect, sort_value in sorting_button_rects:
                         if rect.collidepoint(pos):
                              if sort_value != current_sort_method:
                                   print(f"🔄 Changing sort order to: {sort_value}")
                                   current_sort_method = sort_value
                                   apply_sorting(button_names_list, current_sort_method, AUDIO_PATHS)
                                   current_page_effects = 0
                                   ui_config_data["VAR_ORDER"] = current_sort_method
                                   if ui_config_path:
                                        save_config(ui_config_data, ui_config_path)
                              break

                    if prev_btn_rect_effects and prev_btn_rect_effects.collidepoint(pos):
                         if current_page_effects > 0:
                              current_page_effects -= 1
                              print(f"➡️ Effects: Moving to page {current_page_effects + 1}/{total_pages_effects}")
                         break

                    if next_btn_rect_effects and next_btn_rect_effects.collidepoint(pos):
                         if current_page_effects < total_pages_effects - 1:
                              current_page_effects += 1
                              print(f"➡️ Effects: Moving to page {current_page_effects + 1}/{total_pages_effects}")
                         break

                    if running:
                         for rect, name in sound_button_rects:
                             if rect.collidepoint(pos):
                                  if is_playing_sound_effect:
                                      print("🚫 Sound is already playing. Ignoring click.")
                                  else:
                                      print(f"🎵 Clicked: {name}")
                                      if voice_client and voice_client.is_connected():
                                          is_playing_sound_effect = True
                                          print("DEBUG: is_playing_sound_effect set to True.")
                                          asyncio.create_task(
                                              tocar_audio(
                                                  AUDIO_PATHS,
                                                  name,
                                                  voice_client,
                                                  time_limit_seconds,
                                                  after=after_playback_callback
                                              )
                                          )
                                      else:
                                          print("⚠️ Voice client is not connected. Could not play audio.")
                                  break

            if not running:
                break

            await asyncio.sleep(0.01)

    print("🚪 Finalizing Pygame interface...")

    if pygame.get_init():
        try:
            pygame.quit()
            print("✅ Pygame finalized.")
        except Exception as e:
            print(f"⚠️ Error calling pygame.quit() in interface cleanup: {e}")

    print("🔌 Disconnecting voice channel...")
    # Only disconnect if voice_client is not None AND connected
    # (Avoids errors if connection failed earlier and voice_client is None)
    if voice_client and voice_client.is_connected():
        print("🎤 Disconnecting from voice channel...")
        try:
            await asyncio.sleep(0.5) # Give a moment for potential audio playback to finish
            await voice_client.disconnect()
            print("✅ Disconnected from voice channel.")
        except Exception as e:
            print(f"⚠️ Error disconnecting from voice channel: {e}")
        voice_client = None

    print("👋 Program finished (interface).")