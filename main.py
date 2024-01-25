import setting
import response

import discord
from discord.ext import commands

import datetime

def run():
    # Discord intent setup for bot running
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    hat = commands.Bot(command_prefix="./", intents=intents)

    # Bot running message
    @hat.event
    async def on_ready():
        print("--------------------")
        print(hat.user)
        print(hat.user.id)
        print("** Magic Start **")
        print("--------------------")

    # Welcome message and auto assign a user role
    @hat.event
    async def on_member_join(member):
        channel = hat.get_channel(setting.WELCOME_CHANNEL)
        role = discord.utils.get(member.guild.roles, name="麻瓜")
        await member.add_roles(role)

        embed = discord.Embed(
            title=f"**Welcome to Hogwarts !**",
            description=f"**{member.mention}** come to the Hogwarts, but he/she is a **{role.name}** !!!",
            color=0xFF55FF,
            timestamp=datetime.datetime.now(),
        )

        await channel.send(embed=embed)

    # Server user rock check (Self check)
    @hat.command()
    async def myrole(ctx):
        user = ctx.author
        roles = [role.name for role in user.roles if not role.is_default()]
        if not roles:
            await ctx.send(f"{ctx.author.mention} doesn't have any roles.")
        else:
            await ctx.send(f"{ctx.author.mention} has the following roles: {', '.join(roles)}")

    # User message response
    @hat.command()
    async def talk(ctx, *, user_input):
        bot_response = response.handle_response(user_input)

        if bot_response == None:
            image_path = "images/what 7 you said.jpg"
            image_file = discord.File(image_path)
            await ctx.send(f"{ctx.author.mention}, Sor, What 7 You Said Ar???",file = image_file)
        else:
            await ctx.send(f"{ctx.author.mention}, {bot_response}")

    # Run the bot with the your discord API
    hat.run(setting.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()
