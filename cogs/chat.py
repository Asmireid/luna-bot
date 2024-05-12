import json
import os
import logging

import aiohttp
from discord.ext import commands

from utilities import *

# define the request data as a Python dictionary
request_data = {
    "prompt": "",
    "temperature": 0.5,
    "top_p": 0.9
}

# save chat history globally
context = []

# message queue
chat_queue = asyncio.Queue()


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['说话'], help="chats with user")
    async def chat(self, ctx, *, message):
        new_message = {'role': ctx.author.nick or ctx.author.name, 'content': message}
        params = {'temperature': Config().temperature, 'top_p': Config().top_p, 'top_k': Config().top_k,
                  'max_new_tokens': Config().max_new_tokens}
        await manage_context(new_message)
        await chat_queue.put((context.copy(), params, ctx))
        if chat_queue.qsize() == 1:
            self.bot.loop.create_task(process_chat_queue())

    @commands.command(aliases=['清空', "忘记一切"], help="clears chat history")
    async def reset_chat(self, ctx):
        global context
        context = []
        await try_reply(ctx, "阿巴阿巴! 我忘记了一切!")


async def manage_context(new_message):
    global context
    context.append(new_message)
    if len(context) > 20:
        context.pop(0)


async def process_chat_queue():
    while not chat_queue.empty():
        curr_context, params, ctx = await chat_queue.get()
        try:
            await chat_with_bot(curr_context, params, ctx)
        except Exception as e:
            logging.error(f"Chat Error: {repr(e)}", exc_info=True)


async def chat_with_bot(curr_context, params, ctx):
    async with aiohttp.ClientSession() as session:
        cleaned_sys_prompt = Config().system_prompt.replace("{{char}}", Config().bot_name).replace("{{user}}",
                                                                                                   ctx.author.nick or ctx.author.name)
        curr_context_with_system_prompt = [{'role': 'system', 'content': cleaned_sys_prompt}] + curr_context
        params['context'] = curr_context_with_system_prompt
        async with session.post(Config().api_url, json=params) as response:
            if response.status == 200:
                response_data = await response.json()
                response = {'role': Config().bot_name, 'content': response_data['response']}
                await manage_context(response)
                await try_reply(ctx, response_data['response'])
            else:
                raise Exception("Error fetching chat response. Status code: " + str(response.status))


async def setup(bot):
    await bot.add_cog(Chat(bot))
