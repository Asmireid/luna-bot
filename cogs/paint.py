import random
import os
from dataclasses import dataclass

from discord.ext import commands

from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageResolution, UCPreset, ImageSampler
from util.boilerplate import API

from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

from pathlib import Path

from utilities import *

import logging


@dataclass
class Session:
    is_active: bool = False


painting = Session()
prompt_generating = Session()


class Paint(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help="image generation with NAI V3")
    async def paint(self, ctx, *, prompt):
        # somehow capitalized letters stuck the image generation
        prompt = prompt.lower()

        d = Path("NAI_cache")
        d.mkdir(exist_ok=True)

        configs = Config()

        if painting.is_active:
            await try_reply(ctx, configs.wait_message)
            return
        painting.is_active = True

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        async with API(configs.nai_username, configs.nai_password) as api_handler:
            api = api_handler.api

            preset = ImagePreset()
            preset.uc_preset = UCPreset(int(configs.uc_preset))
            preset.n_samples = 1
            preset.sampler = ImageSampler(configs.sampler)
            preset.uc = configs.uc_base
            preset.seed = random.randint(1, 9999999999) if configs.seed == -1 else configs.seed
            preset.resolution = ImageResolution(tuple(map(int, configs.resolution.split(', '))))
            preset.decrisper = configs.decrisper
            preset.quality_toggle = configs.quality_toggle
            prompt_prefix = configs.prompt_prefix

            conf = await try_reply(ctx, f'Painting "{prompt_prefix} {prompt}"...')
            try:
                async for _, img in api.high_level.generate_image(prompt_prefix + prompt, ImageModel.Anime_v3, preset):
                    (d / f"cache.png").write_bytes(img)
            except Exception as e:
                logging.error(f"NAI API Error: {repr(e)}", exc_info=True)
                await try_reply(ctx, f"Error occurred: {repr(e)}")
            else:
                await try_reply(ctx, "Painted!", file=discord.File(d / f"cache.png"))
            finally:
                await try_delete_confirmation(conf)
                painting.is_active = False

    @commands.command(name="pgen", help="generte danbooru tags using FredZhang7/danbooru-tag-generator")
    async def prompt_extend(self, ctx, *, prompt):
        if prompt_generating.is_active:
            await try_reply(ctx, Config().wait_message)
            return
        prompt_generating.is_active = True
        tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model = GPT2LMHeadModel.from_pretrained('FredZhang7/danbooru-tag-generator')

        nlp = pipeline('text-generation', model=model, tokenizer=tokenizer)
        outs = nlp(prompt, max_length=74, num_return_sequences=4, do_sample=True, repetition_penalty=1.2,
                   temperature=0.7, top_k=4, early_stopping=False)
        for i in range(len(outs)):
            # remove trailing commas and double spaces
            outs[i] = str(outs[i]['generated_text']).replace('  ', '').rstrip(',')
        await try_reply(ctx, '\n\n'.join(outs))
        prompt_generating.is_active = False


async def setup(bot):
    await bot.add_cog(Paint(bot))
