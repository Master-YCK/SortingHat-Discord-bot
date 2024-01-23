import setting
import discord
from discord.ext import commands

def run():
    #Discord intent setup for bot running
    intents = discord.Intents.default()
    hat = commands.Bot(command_prefix="./", intents = intents)

    @hat.event
    async def on_ready():
        print("--------------------")
        print(hat.user)
        print(hat.user.id)
        print("Magic Start")
        print("--------------------")

    hat.run(setting.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()

