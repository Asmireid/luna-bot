import logging
import os
import aiohttp

from discord import FFmpegPCMAudio
from discord.ext import commands
from utilities import *


class FFmpegPCMAudioWithTitle(FFmpegPCMAudio):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)
        # extracts the base filename to use as the title
        self.title = os.path.basename(source)


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tts_queue = asyncio.Queue()
        self.audio_queue = asyncio.Queue()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help="plays or queues local audio file in voice channel")
    async def play(self, ctx, path):
        voice = ctx.voice_client
        if not voice:
            await try_display_confirmation(ctx, "I'm not connected to a voice channel.")
            return

        if os.path.isdir(path):
            msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice",
                                   descr=f"Queuing files in {path} for play.")
            await try_display_confirmation(ctx, msg_embed)

            for filename in os.listdir(path):
                full_path = os.path.join(path, filename)
                if os.path.isfile(full_path):
                    await self.audio_queue.put(full_path)
        elif os.path.isfile(path):
            msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice",
                                   descr=f"Queuing {path} for play.")
            await try_display_confirmation(ctx, msg_embed)

            await self.audio_queue.put(path)
        else:
            await try_display_confirmation(ctx, "Invalid path or file format.")

        if not voice.is_playing():
            await self.play_audio(ctx)

    async def play_audio(self, ctx):
        voice = ctx.voice_client
        while not self.audio_queue.empty() and not voice.is_playing():
            next_audio = await self.audio_queue.get()
            try:
                source = FFmpegPCMAudioWithTitle(next_audio)
                voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_audio(ctx), ctx.bot.loop))
                await try_display_confirmation(ctx, f"Now playing: '{source.title}'")
            except Exception as e:
                logging.error(f"Play Error: {repr(e)}", exc_info=True)
                await try_reply(ctx, f"Error occurred: {repr(e)}")
                break

    @commands.command(help="displays the current audio queue.")
    async def queue(self, ctx):
        if self.audio_queue.empty():
            await ctx.send("The audio queue is currently empty.")
            return

        queue_list = list(self.audio_queue._queue)
        msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice", descr="Current Queue:")
        for index, item in enumerate(queue_list):
            msg_embed.add_field(name=f"{index + 1}", value=f"{os.path.basename(item)}", inline=False)
        await try_reply(ctx, msg_embed)

    @commands.command(help="pauses the current audio in voice channel")
    async def pause(self, ctx):
        voice = ctx.voice_client
        if voice and voice.is_playing():
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Voice",
                                   descr=f"Pausing '{voice.source.title}'.")
            await try_display_confirmation(ctx, msg_embed)

            voice.pause()
        else:
            await try_display_confirmation(ctx, "I'm not playing any audio.")

    @commands.command(help="resumes the current audio in voice channel")
    async def resume(self, ctx):
        voice = ctx.voice_client
        if voice and voice.is_paused():
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Voice",
                                   descr=f"Resuming '{voice.source.title}'.")
            await try_display_confirmation(ctx, msg_embed)

            voice.resume()
        else:
            await try_display_confirmation(ctx, "No audio is paused currently.")

    @commands.command(help="skips the current audio in voice channel")
    async def skip(self, ctx):
        voice = ctx.voice_client
        if voice and voice.is_playing():
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Voice",
                                   descr=f"Skipping '{voice.source.title}'.")
            await try_display_confirmation(ctx, msg_embed)

            await voice.stop()
        else:
            await try_display_confirmation(ctx, "I'm not playing any audio.")

    @commands.command(aliases=['活字印刷'],
                      help="text to speech conversion")
    async def tts(self, ctx, *, text):
        msg_embed = make_embed(ctx,
                               title=f"{Config().bot_name}'s Voice",
                               descr=f"Trying to convert '{text}' to speech.")
        conf = await try_reply(ctx, msg_embed)

        await self.tts_queue.put((text, ctx, conf))

        if self.tts_queue.qsize() == 1:  # start the TTS processor if it's not already running
            self.bot.loop.create_task(self.process_tts_queue())

    async def process_tts_queue(self):
        while not self.tts_queue.empty():
            text, ctx, conf = await self.tts_queue.get()
            try:
                await save_voice(text)
            except Exception as e:
                logging.error(f"TTS Error: {repr(e)}", exc_info=True)
                await try_reply(ctx, f"Error occurred: {repr(e)}")
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
    await bot.add_cog(Voice(bot))
