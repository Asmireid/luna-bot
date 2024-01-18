import random
import os
from dataclasses import dataclass

import requests
from discord.ext import commands

from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageResolution, UCPreset, ImageSampler
from util.boilerplate import API

from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

from pathlib import Path

from utilities import *


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
        d = Path("NAI_cache")
        d.mkdir(exist_ok=True)

        if painting.is_active:
            await try_reply(ctx, "急神魔？")
            return
        painting.is_active = True

        async with API() as api_handler:
            api = api_handler.api

            preset = ImagePreset()
            preset.uc_preset = UCPreset.Preset_Heavy
            preset.n_samples = 1
            preset.sampler = ImageSampler.k_euler
            preset.uc = "lowres, bad anatomy, bad mouth, bad hands, bad feet, extra limbs, text, error, bad fingers, " \
                        "missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, " \
                        "normal quality, jpeg artifacts, signature, watermark, username, blurry, simple background"

            preset.seed = random.randint(1, 9999999999)
            if random.randint(0, 10) < 5:
                preset.resolution = ImageResolution.Normal_Portrait_v3
            else:
                preset.resolution = ImageResolution.Normal_Landscape_v3

            prompt_prefix = "{{{amazing quality, very aesthetic, ultra-detailed character, illustration, painting, " \
                            "8K UHD Wallpaper, modern day}}}, "
            await try_reply(ctx, "Painting...")
            try:
                async for _, img in api.high_level.generate_image(prompt_prefix + prompt, ImageModel.Anime_v3, preset):
                    (d / f"cache.png").write_bytes(img)
            except Exception as e:
                raise Exception(f"NAI API Error: {repr(e)}")
        await ctx.send("Painted!", file=discord.File(d / f"cache.png"))
        painting.is_active = False

    @commands.command(name="pgen", help="generte danbooru tags using FredZhang7/danbooru-tag-generator")
    async def prompt_extend(self, ctx, *, prompt):
        if prompt_generating.is_active:
            await try_reply(ctx, "急急急急牛魔")
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