import logging
import os

import aiohttp
import requests
from discord.ext import commands
from utilities import *

tts_queue = asyncio.Queue()


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['活字印刷'],
                      help="text to speech conversion")
    async def tts(self, ctx, *, text):
        msg_embed = make_embed(ctx,
                               title=f"{Config().bot_name}'s Voice",
                               descr=f"Trying to convert '{text}' to speech.")
        conf = await try_reply(ctx, msg_embed)

        await tts_queue.put((text, ctx, conf))

        if tts_queue.qsize() == 1:  # start the TTS processor if it's not already running
            self.bot.loop.create_task(process_tts_queue())


async def process_tts_queue():
    while not tts_queue.empty():
        text, ctx, conf = await tts_queue.get()
        try:
            await save_voice(text)
        except Exception as e:
            logging.error(f"TTS Error: {repr(e)}", exc_info=True)
            await ctx.send(f"Error occurred: {repr(e)}")
        else:
            await try_reply(ctx, "Spoken!", file=discord.File("cache/cache.wav"))
        finally:
            await try_delete_confirmation(conf)


async def save_voice(chosen_text, cache_folder='cache'):
    api_url = f"https://mahiruoshi-bert-vits2-api.hf.space/?text={{{chosen_text}}}&speaker={Config().speaker}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                os.makedirs(cache_folder, exist_ok=True)
                local_path = os.path.join(cache_folder, 'cache.wav')
                with open(local_path, 'wb') as wav_file:
                    wav_file.write(await response.read())
            else:
                raise Exception("Error fetching voice response. Status code: " + str(response.status))


async def setup(bot):
    await bot.add_cog(TTS(bot))
