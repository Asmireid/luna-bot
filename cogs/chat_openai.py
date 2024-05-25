import os
import logging
from openai import OpenAI
from discord.ext import commands
from utilities import *


class ChatOpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return  # ignore bot's own response

        bot_member = message.guild.get_member(self.bot.user.id)
        bot_nickname = bot_member.nick
        bot_username = bot_member.name

        if (bot_nickname and bot_nickname.lower() in message.content.lower()) or (
                bot_username.lower() in message.content.lower()):
            ctx = await self.bot.get_context(message)
            await self.chat_openai(ctx, message=message.content)

    @commands.command(help="chats with user")
    async def chat_openai(self, ctx, *, message):
        try:
            configs = Config()

            client = OpenAI(api_key=configs.openai_api_key)

            messages = [{'role': 'system', 'content': configs.system_prompt}]

            new_message = {'role': 'user', 'content': message}
            messages.append(new_message)

            response = client.chat.completions.create(
                model='gpt-4o',
                messages=messages,
                max_tokens=configs.max_new_tokens,
            )

            gpt_response = response.choices[0].message.content.strip()

            await try_reply(ctx, gpt_response)
        except Exception as e:
            logging.error(f"Chat Error: {repr(e)}", exc_info=True)
            await try_reply(ctx, f"Error occurred: {repr(e)}")


async def setup(bot):
    await bot.add_cog(ChatOpenAI(bot))
