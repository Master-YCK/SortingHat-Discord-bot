# Project file import
import setting
import response
import gamme

# Discord.py import
import asyncio
import discord
from discord.ext import commands

# Python import
import datetime
import random
import os


class SimpleView(discord.ui.View):

    foo: bool = None

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        return

    # @discord.ui.button(label="Hello", style=discord.ButtonStyle.success)
    # async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await interaction.response.send_message("World!")
    #     self.foo = True
    #     self.stop()

    @discord.ui.button(label="Retry", style=discord.ButtonStyle.red)
    async def retry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("The Retry Generate: ")
        self.foo = True
        self.stop()


# Main function
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
        print(
            f"({member}) join the server at ({datetime.datetime.now()}), assigned roll: [{role.name}]"
        )

    # Server user rock check (Self check)
    @hat.command()
    async def myrole(ctx):
        user = ctx.author
        roles = [role.name for role in user.roles if not role.is_default()]
        if not roles:
            await ctx.send(f"{ctx.author.mention} doesn't have any roles.")
        else:
            await ctx.send(
                f"{ctx.author.mention} has the following roles: {', '.join(roles)}"
            )
        print(f"({ctx.author}) check the role")

    # User message response
    @hat.command()
    async def talk(ctx, *, user_input):
        bot_response = response.handle_response(user_input)
        # Console log to check user input
        print(f"({ctx.author}) said: [{user_input}] to the bot")

        if bot_response == None:
            image_path = "images/what 7 you said.jpg"
            image_file = discord.File(image_path)
            await ctx.send(
                f"{ctx.author.mention}, Sor, What 7 You Said Ar???", file=image_file
            )
            print(f"Bot response to ({ctx.author}) with no understand input text")
        else:
            await ctx.send(f"{ctx.author.mention}, {bot_response}")
            print(f"Bot response to ({ctx.author}) with [{bot_response}]")

    @hat.command()
    async def response(ctx, input):
        async with ctx.typing():
            await asyncio.sleep(3)
        await ctx.send(f"Hello, {ctx.author.mention}! You said: {input}")
        
    # Roll the dice game
    @hat.command()
    async def roll(ctx):
        image_dir = "images/dice/"
        dice_image = os.listdir(image_dir)
        image_path = image_dir + random.choice(dice_image)
        image_file = discord.File(image_path)
        await ctx.send(
            f"Congratulation !!! {ctx.author.mention} you roll the number:",
            file=image_file,
        )
        print(f"({ctx.author}) roll the dice with [{image_path}]")

    # Chat with the bot using the Google Gamme 2b Model
    @hat.command()
    async def chat(ctx: commands.Context, *, user_input):
        async with ctx.typing():
            await asyncio.sleep(6)

        bot_response = gamme.genText(user_input)

        view = SimpleView(timeout=5)

        message = await ctx.reply(f"{ctx.author.mention}, {bot_response}", view=view, ephemeral=True)
        view.message = message
        print(f"Bot response to ({ctx.author}) with: [{bot_response}]")

        await view.wait()
        await view.disable_buttons()

        if view.foo is None:
            print("No button was clicked")
        elif view.foo is True:
            async with ctx.typing():
                await asyncio.sleep(6)
            bot_response = gamme.genText(user_input)
            await ctx.reply(f"{ctx.author.mention}, {bot_response}", ephemeral=True)
            print(f"({ctx.author}) retry to generate the text context: [{bot_response}]")
            
    # Run the bot with the your discord API
    hat.run(setting.DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
