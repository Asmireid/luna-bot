import logging
import tempfile
import os
import aiohttp
import yt_dlp as youtube_dl
from discord import FFmpegPCMAudio
from discord.ext import commands
from utilities import *


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': None,  # Placeholder, will be set dynamically
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',  # Bind to IPv4
    }

    ytdl = None  # This will be initialized later with a specific temp path

    def __init__(self, source, *, data, temp_dir, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title', 'Unknown title')
        self.url = data.get('url')
        self.temp_dir = temp_dir  # Track the temp directory for cleanup

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        # Create a temporary directory for the downloads
        temp_dir = tempfile.mkdtemp()
        cls.YTDL_OPTIONS['outtmpl'] = os.path.join(temp_dir, '%(id)s.%(ext)s')  # Set outtmpl to temp dir
        cls.ytdl = youtube_dl.YoutubeDL(cls.YTDL_OPTIONS)  # Reinitialize with the new path

        # Extract video information
        data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=not stream))

        if 'entries' in data:  # Handle playlists, take the first entry
            data = data['entries'][0]

        filename = data['url'] if stream else cls.ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename), data=data, temp_dir=temp_dir)

    def cleanup(self):
        """Delete the temporary directory and its contents."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)


class FFmpegPCMAudioWithTitle(FFmpegPCMAudio):
    def __init__(self, source, title=None, **kwargs):
        """
        Custom FFmpegPCMAudio class that includes a title attribute.
        If `title` is not provided, it uses the base filename as the title.
        """
        super().__init__(source, **kwargs)
        self.title = title if title else os.path.basename(source)


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tts_queue = asyncio.Queue()
        self.audio_queue = asyncio.Queue()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    async def ensure_voice(self, ctx):
        if not ctx.voice_client:
            await try_display_confirmation(ctx, "I'm not connected to a voice channel.")
            return False
        return True

    @commands.command(help="plays or queues local audio file in voice channel")
    async def play_local(self, ctx, path):
        if not await self.ensure_voice(ctx): return
        voice = ctx.voice_client

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

    @commands.command(aliases=['唱'], help="Plays from a url (almost anything youtube_dl supports)")
    async def play_url(self, ctx, *, url):
        if not await self.ensure_voice(ctx): return
        voice = ctx.voice_client

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
                await self.audio_queue.put(player)
                msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice",
                                       descr=f"Queued video (predownload): {player.title}")
                await try_display_confirmation(ctx, msg_embed)
            except Exception as e:
                logging.error(f"YT Error: {repr(e)}", exc_info=True)
                await try_reply(ctx, f"Error occurred: {repr(e)}")
                return

        if not voice.is_playing():
            await self.play_audio(ctx)

    @commands.command(help="Streams from a url (same as yt, but doesn't predownload)")
    async def play_url_stream(self, ctx, *, url):
        if not await self.ensure_voice(ctx): return
        voice = ctx.voice_client

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                await self.audio_queue.put(player)
                msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice",
                                       descr=f"Queued video as stream: {player.title}")
                await try_display_confirmation(ctx, msg_embed)
            except Exception as e:
                logging.error(f"Stream Error: {repr(e)}", exc_info=True)
                await try_reply(ctx, f"Error occurred: {repr(e)}")
                return

        if not voice.is_playing():
            await self.play_audio(ctx)

    async def play_audio(self, ctx):
        voice = ctx.voice_client
        while not self.audio_queue.empty() and not voice.is_playing():
            next_audio = await self.audio_queue.get()
            try:
                if isinstance(next_audio, str):  # Local file
                    source = FFmpegPCMAudioWithTitle(next_audio)
                    title = source.title
                else:  # YTDLSource object
                    source = next_audio
                    title = source.title

                def after_playback(error):
                    if error:
                        logging.error(f"Playback error: {error}")
                    # Cleanup after playback finishes
                    if isinstance(next_audio, YTDLSource):
                        next_audio.cleanup()
                    # Trigger the next audio playback
                    asyncio.run_coroutine_threadsafe(self.play_audio(ctx), self.bot.loop)

                # Start playback
                voice.play(source, after=after_playback)

                # Notify user
                msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice",
                                       descr=f"Now playing: {title}")
                await try_display_confirmation(ctx, msg_embed)

            except Exception as e:
                logging.error(f"Play Error: {repr(e)}", exc_info=True)
                await try_reply(ctx, f"Error occurred: {repr(e)}")
                break

    @commands.command(help="displays the current audio queue.")
    async def queue(self, ctx):
        try:
            if self.audio_queue.empty():
                await try_reply(ctx, "The audio queue is currently empty.")
                return

            queue_list = list(self.audio_queue._queue)
            msg_embed = make_embed(ctx, title=f"{Config().bot_name}'s Voice", descr="Current Queue:")

            for index, item in enumerate(queue_list):
                if isinstance(item, str):  # i.e. local file
                    msg_embed.add_field(name=f"{index + 1}", value=f"{os.path.basename(item)}", inline=False)
                else:  # URL (YTDLSource object)
                    msg_embed.add_field(name=f"{index + 1}", value=f"{item.title}", inline=False)

            await try_reply(ctx, msg_embed)
        except Exception as e:
            logging.error(f"Queue Error: {repr(e)}", exc_info=True)
            await try_reply(ctx, f"Error occurred: {repr(e)}")

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
