import logging
import os
import requests
from dataclasses import dataclass
from discord.ext import commands
from utilities import *


@dataclass
class Session:
    is_active: bool = False


tts_converting = Session()


def save_voice(chosen_text, cache_folder='cache'):
    api_url = f"https://mahiruoshi-bert-vits2-api.hf.space/?text={{{chosen_text}}}&speaker={Config().speaker}"
    response = requests.get(api_url)

    if response.status_code == 200:
        os.makedirs(cache_folder, exist_ok=True)

        local_path = os.path.join(cache_folder, 'cache.wav')

        with open(local_path, 'wb') as wav_file:
            wav_file.write(response.content)
    else:
        raise Exception("Error fetching voice response. Status code: " + str(response.status_code))


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['活字印刷'],
                      help="text to speech conversion")
    async def tts(self, ctx, *, expression):
        if tts_converting.is_active:
            await try_reply(ctx, Config().wait_message)
            return
        tts_converting.is_active = True

        msg_embed = make_embed(ctx,
                               title=f"{Config().bot_name}'s Voice",
                               descr=f"Trying to convert '{expression}' to speech.")
        conf = await try_reply(ctx, msg_embed)
        try:
            save_voice(expression)
        except Exception as e:
            logging.error(f"TTS Error: {repr(e)}", exc_info=True)
            await ctx.send(f"Error occurred: {repr(e)}")
        else:
            await try_reply(ctx, "Spoken!", file=discord.File("cache/cache.wav"))
        finally:
            await try_delete_confirmation(conf)
            tts_converting.is_active = False


async def setup(bot):
    await bot.add_cog(TTS(bot))
