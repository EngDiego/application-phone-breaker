from src.config_loader import load_config
import nacl
import nacl.encoding
import nacl.public
import nacl.secret
import nacl.signing
import os
import logging
import sys
import asyncio
import discord
from discord.ext import commands
import pygame
from src.ui import run_interface

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
for libname in ("discord", "discord.http", "discord.client", "discord.gateway"):
    logger = logging.getLogger(libname)
    logger.setLevel(logging.ERROR)
    if not logger.handlers:
        logger.addHandler(handler)

config_data_initial, config_path_initial = load_config()

TOKEN = config_data_initial.get("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("❌ Error: Discord bot TOKEN not found in config.json.")
    print("Ensure you have the 'DISCORD_BOT_TOKEN' key with your token.")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = False
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)
voice_client = None

@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")
    print(f"🤖 Ready to operate in {len(bot.guilds)} guild(s).")

async def main():
    global voice_client

    bot_task = None
    interface_task = None

    bot.error_message = None # Initialize error message attribute

    try:
        bot_task = asyncio.create_task(bot.start(TOKEN))
        interface_task = asyncio.create_task(run_interface(bot, voice_client))
        await interface_task # Wait for the interface to finish (user closes window)

    except asyncio.CancelledError:
        print("\n🚫 Operation cancelled.")
        bot.error_message = "🚫 Operation Cancelled." # Set error on cancellation too
    except asyncio.TimeoutError:
        print("❌ Timeout connecting to Discord bot.")
        bot.error_message = "❌ Connection Timeout: Could not connect to Discord."
    except discord.errors.LoginFailure:
        print("❌ Login error: Invalid Discord token.")
        bot.error_message = "❌ Login Failed: Invalid Discord token."
    except discord.errors.ConnectionClosed as e:
         print(f"❌ Connection closed prematurely: {e}")
         bot.error_message = f"❌ Connection Closed: {e}"
    except discord.errors.RateLimited as e: # Specific Rate Limited exception
        print(f"❌ Rate Limited by Discord API: {e}")
        bot.error_message = f"❌ Rate Limited by Discord API. Try again later."
    except Exception as e:
        print(f"❌ An unexpected error occurred during main execution: {e}")
        bot.error_message = f"❌ Unexpected Error: {e}"

    finally:
        print("Executing final cleanup in main...")

        if bot_task and not bot_task.done():
             print("Cleanup: Attempting graceful bot shutdown...")
             try:
                 await bot.close()
                 print("Cleanup: Bot client closed.")
             except Exception as e:
                 print(f"⚠️ Error closing bot client gracefully: {e}")

        if bot_task and not bot_task.done():
            print("Cleanup: Waiting for bot task to complete...")
            try:
                await asyncio.wait_for(bot_task, timeout=3.0)
                print("Cleanup: Bot task finished.")
            except asyncio.TimeoutError:
                print("Cleanup: Timeout waiting for bot task. It might be stuck.")
            except Exception as e:
                 print(f"⚠️ Unexpected error waiting for bot task: {e}")

        if pygame.get_init():
            print("Cleanup: Calling pygame.quit() (final safeguard).")
            try:
                pygame.quit()
            except Exception as e:
                print(f"⚠️ Error calling pygame.quit() in cleanup: {e}")

    print("👋 Program finished.")

if __name__ == "__main__":
    try:
        print("🚀 Starting Quebra Fone application...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🚫 Interrupted by user (Ctrl+C).")
    except Exception as e:
        print(f"❌ An error occurred in the __main__ block: {e}")

    finally:
        if pygame.get_init():
            print("Cleanup: Calling pygame.quit() in final __main__ block.")
            try:
                pygame.quit()
            except Exception as e:
                print(f"⚠️ Error calling pygame.quit() in final cleanup: {e}")

    print("👋 Program finished (finally).")