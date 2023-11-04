import json

from utilities import *


def get_status():
    try:
        with open("config/config.json", "r") as f:
            bot_config = json.load(f)

    except FileNotFoundError:
        print("File not found. Make sure the file path is correct.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Make sure the JSON file contains valid JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return bot_config["status"]


def update_status(new_status):
    try:
        with open("config/config.json", "r") as f:
            bot_config = json.load(f)

        bot_config["status"] = new_status

        with open("config/config.json", "w") as f:
            json.dump(bot_config, f, indent=4)
        print('updated successfully')

    except FileNotFoundError:
        print("File not found. Make sure the file path is correct.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Make sure the JSON file contains valid JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")


class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
    async def set_status(self, ctx, *, new_status: str):
        update_status(new_status)
        await self.bot.change_presence(activity=discord.CustomActivity(name=new_status))
        msg = f"My new status is: {new_status}."
        await try_reply(ctx, msg)


async def setup(bot):
    await bot.add_cog(Update(bot))
