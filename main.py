# Project file import
import setting
import response
import gamme
import stable_diffusion

# Discord.py import
import asyncio
import discord
from discord.ext import commands

# Python import
import datetime
from datetime import datetime
import random
import os


# The button view class
class SimpleView(discord.ui.View):

    foo: bool = None

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        return

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
        metion = member.mention
        guild = member.guild
        await member.add_roles(role)

        embed = discord.Embed(
            title=f"**Welcome to Hogwarts !**",
            description=f"**{metion}** come to the {guild}, but he/she is a **{role.name}** !!!",
            color=0xFF55FF,
            timestamp=datetime.now(),
        )

        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"{member.guild}", icon_url=member.guild.icon)
        embed.add_field(name="User ID", value=member.name)
        embed.add_field(name="User Name", value=member.display_name)
        embed.add_field(name="Server Serial", value=len(list(guild.members)))
        embed.add_field(name="Create At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Join At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        await channel.send(embed=embed)

        print(
            f"({member}) join the server at ({datetime.now()}), assigned roll: [{role.name}]"
        )

    # Leave message
    @hat.event
    async def on_member_remove(member):
        channel = hat.get_channel(setting.WELCOME_CHANNEL)
        await channel.send(f"**{member}** has left the Hogwarts.")
        print(f"({member}) has leave the server at ({datetime.now()})]")

    # Server user rock check (Self check)
    @hat.command()
    async def myrole(ctx: commands.Context):
        user = ctx.author
        roles = [role.name for role in user.roles if not role.is_default()]
        if not roles:
            async with ctx.typing():
                await ctx.reply(f"{ctx.author.mention} doesn't have any roles.")
        else:
            async with ctx.typing():
                await ctx.reply(
                    f"{ctx.author.mention} has the following roles: {', '.join(roles)}"
                )
        print(f"({ctx.author}) check the role")

    # User message response
    @hat.command()
    async def talk(ctx: commands.Context, *, user_input):
        bot_response = response.handle_response(user_input)
        # Console log to check user input
        print(f"({ctx.author}) said: [{user_input}] to the bot")

        if bot_response == None:
            image_path = "images/what 7 you said.jpg"
            image_file = discord.File(image_path)
            async with ctx.typing():
                await ctx.reply(
                    f"{ctx.author.mention}, Sor, What 7 You Said Ar???", file=image_file
                )
            print(f"Bot response to ({ctx.author}) with no understand input text")
        else:
            async with ctx.typing():
                await ctx.reply(f"{ctx.author.mention}, {bot_response}")
            print(f"Bot response to ({ctx.author}) with [{bot_response}]")

    # Roll the dice game
    @hat.command()
    async def roll(ctx: commands.Context):
        image_dir = "images/dice/"
        dice_image = os.listdir(image_dir)
        image_path = image_dir + random.choice(dice_image)
        image_file = discord.File(image_path)
        async with ctx.typing():
            await ctx.reply(
                f"Congratulation !!! {ctx.author.mention} you roll the number:",
                file=image_file,
            )
        print(f"({ctx.author}) roll the dice with [{image_path}]")

    # Chat with the bot using the Google Gamme 2b Model
    @hat.command()
    async def chat(ctx: commands.Context, *, user_input):
        async with ctx.typing():
            begTime = datetime.now()
            bot_response = gamme.genText(user_input)

        view = SimpleView(timeout=5)

        message = await ctx.reply(
            f"{ctx.author.mention}, {bot_response}", view=view, ephemeral=True
        )
        timeElapsed = (datetime.now() - begTime) * 0.001
        view.message = message
        print(
            f"Bot response to ({ctx.author}) with: [{bot_response}] and Time: [{timeElapsed}]"
        )

        await view.wait()
        await view.disable_buttons()

        if view.foo is None:
            print("No button was clicked")
        elif view.foo is True:
            async with ctx.typing():
                bot_response = gamme.genText(user_input)
            await ctx.reply(f"{ctx.author.mention}, {bot_response}", ephemeral=True)
            print(
                f"({ctx.author}) retry to generate the text context: [{bot_response}]"
            )

    # Chat with the bot using the RunwayML Stable Diffusion Model
    @hat.command()
    async def img(ctx: commands.Context, *, user_input):
        async with ctx.typing():
            stable_diffusion.generate_image(user_input)
            image_file = discord.File("generated.png")

            async with ctx.typing():
                await ctx.reply(
                    f"{ctx.author.mention} generated the image picture with:",
                    file=image_file,
                )

        print(f"({ctx.author}) generated the image")

    # Run the bot with the your discord API
    hat.run(setting.DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
