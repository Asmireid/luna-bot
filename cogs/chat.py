import json
import os

import requests
from discord.ext import commands

from utilities import *

url = 'http://localhost:5001/api/v1/generate'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Define the request data as a Python dictionary
request_data = {
    "prompt": "",
    "temperature": 0.5,
    "top_p": 0.9
}


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help=f"chats with user: {Config().command_prefix}chat example_text")
    async def chat(self, ctx, *, question):
        try:
            # Clean input
            user_input = "###instruction: " + question
            request_data['prompt'] = user_input
            print(user_input)
            # Convert the request data to JSON format
            data = json.dumps(request_data)
            # Send the POST request
            response = requests.post(url, headers=headers, data=data)
            # Check if the request was successful (HTTP status code 200)
            # response_chat = ''
            text = "Can't get response..."
            if response.status_code == 200:
                # Parse and print the response as JSON
                response_data = response.json()
                text = response_data["results"][0]["text"]
                print(text)
            await try_reply(ctx, text)
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Chat(bot))
