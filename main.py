import setting
import response
import discord
import datetime
import random
import os
import typing
from components import embedComp
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from discord.ext import tasks
from hkobs import check_warnsum_periodically
from trans import translate_text


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


# Main function & bot running
def run():
    # Discord intent setup for bot running
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    hat = commands.Bot(command_prefix="./", intents=intents)

    # Sync the bot command
    async def sync_commands():
        try:
            extensions = ["ollama_chat", "hkobs", "trans"]
            for extension in extensions:
                await hat.load_extension(extension)
            synced = await hat.tree.sync()
            print("--------------------")
            print("Synced the following commands:")
            for command in synced:
                print(f"- {command.name} (Type: {command.type.name}, ID: {command.id})")
        except Exception as e:
            print(f"An error occurred: {e}")

    # MBTI list for the user to choose
    async def mbti_autocompletion(
        interaction: discord.interactions, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        mbti_types = [
            "INTJ",
            "INTP",
            "ENTJ",
            "ENTP",
            "INFJ",
            "INFP",
            "ENFJ",
            "ENFP",
            "ISTJ",
            "ISFJ",
            "ESTJ",
            "ESFJ",
            "ISTP",
            "ISFP",
            "ESTP",
            "ESFP",
        ]
        # Filter MBTI types based on the current input (case-insensitive)
        return [
            app_commands.Choice(name=item, value=item)
            for item in mbti_types
            if current.upper() in item.upper()
        ]

    # MBTI color for the user role
    def mbti_color(mbti_type: str) -> int:
        mbti_colors = {
            "INTJ": 0x88619A,
            "INTP": 0x88619A,
            "ENTJ": 0x88619A,
            "ENTP": 0x88619A,
            "INFJ": 0x33A474,
            "INFP": 0x33A474,
            "ENFJ": 0x33A474,
            "ENFP": 0x33A474,
            "ISTJ": 0x4298B4,
            "ISFJ": 0x4298B4,
            "ESTJ": 0x4298B4,
            "ESFJ": 0x4298B4,
            "ISTP": 0xE4AE3A,
            "ISFP": 0xE4AE3A,
            "ESTP": 0xE4AE3A,
            "ESFP": 0xE4AE3A,
        }
        return mbti_colors.get(
            mbti_type.upper(), 0xCCCCCC
        )  # Default color if not found

    # Bot running message
    @hat.event
    async def on_ready():
        await sync_commands()
        hat.loop.create_task(
            hat.change_presence(
                activity=discord.Game(name="Ah, yes. Uh, yeah. There you go! Magic!!!")
            )
        )
        # weather_warnsum.start()
        print("--------------------")
        print(hat.user)
        print(f"ID: {hat.user.id}")
        print("** Magic Start **")
        print("--------------------")

    # Welcome message and auto assign a user role
    @hat.event
    async def on_member_join(member):
        channel = hat.get_channel(setting.WELCOME_CHANNEL)
        role = discord.utils.get(member.guild.roles, name="麻瓜")
        await member.add_roles(role)

        embed = discord.Embed(
            title=f"**Welcome to {member.guild} !!!**",
            description=f"**{member.mention}** come to the {member.guild}, but he/she is a **{role.name}** !!!",
            color=0xFF55FF,
            timestamp=datetime.now(),
        )

        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"{member.guild}", icon_url=member.guild.icon)
        embed.add_field(name="User Name", value=member.name)
        embed.add_field(name="AKA.", value=member.display_name)
        embed.add_field(name="Server Serial", value=len(list(member.guild.members)))
        embed.add_field(
            name="Create At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        embed.add_field(
            name="Join At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        await channel.send(embed=embed)

        print(
            f"({member}) join the server at ({datetime.now()}), assigned roll: [{role.name}]"
        )

    # A member leave message
    @hat.event
    async def on_member_remove(member):
        channel = hat.get_channel(setting.WELCOME_CHANNEL)
        await channel.send(f"**{member.name}** has left the Hogwarts.")
        print(f"({member}) has leave the server at ({datetime.now()})]")

    # Error message handling with different type of error
    @hat.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            async with ctx.typing():
                await ctx.reply(
                    f"{ctx.author.mention}. We don't have this, check the memu try again !!!."
                )
            print(f"({ctx.author}) entered the wrong command")

        elif isinstance(error, commands.MissingRequiredArgument):
            async with ctx.typing():
                await ctx.reply(
                    f"{ctx.author.mention}. Child you missing something, think about that !!!."
                )
            print(f"({ctx.author}) entered the wrong argument")

        elif isinstance(error, commands.MissingPermissions):
            async with ctx.typing():
                await ctx.reply(
                    f"{ctx.authorweather_warnsum.start.mention}. How Dare You To Do This !!!."
                )
            print(f"({ctx.author}) entered the wrong permission")

    # Automation task to check the warnsum periodically
    # @tasks.loop(minutes=1)  # Example: send a message every minute
    # async def weather_warnsum():
    #     data = await check_warnsum_periodically()
    #     channel_id = [1185848222321754144]  # Replace with your channel ID
    #     for cid in channel_id:
    #         channel = hat.get_channel(cid)
    #         if channel and data is not None:
    #             embed = embedComp.cuz_embed(
    #                 "***Weather Warning Summary 實時天氣警告***", "", None, None
    #             )
    #             embed.set_thumbnail(url=data.get("URL"))
    #             embed.add_field(
    #                 name="Warning Type",
    #                 value=f"{data.get('WTS', {}).get('name', 'N/A')}",
    #             )
    #             await channel.send(embed=embed)

    # Bot command list
    # Bot Slash command list
    @hat.tree.command(name="hello", description="Say Hello to someone!")
    async def hello(interaction: discord.interactions, user: discord.Member):
        await interaction.response.send_message(f"Hi {user.mention} !!!")
        print(f"{interaction.user.name} used the slash command")

    # Slash command to assign a user role of user MBTI
    @hat.tree.command(name="mbti", description="Add your MBTI")
    @app_commands.autocomplete(mbti=mbti_autocompletion)
    async def mbti(interaction: discord.interactions, mbti: str):
        role = discord.utils.get(interaction.guild.roles, name=mbti)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"Role {role.name} added to {interaction.user.mention}"
            )
            print(f"{interaction.user.name} add the {role.name} role")
        elif not role:
            role = await interaction.guild.create_role(
                name=mbti, color=mbti_color(mbti)
            )
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"Role {role.name} added to {interaction.user.mention}"
            )
            print(f"{interaction.user.name} create a {role.name} role of the server")
        else:
            await interaction.response.send_message(
                "Can't assign the MBTI role for you", ephemeral=True
            )
            print(f"{interaction.user.name} used the slash command")

    # Slash command to check the bot latency
    @hat.tree.command(name="ping", description="Check the bot latency")
    async def ping(interaction: discord.interactions):
        await interaction.response.send_message(f"Pong! {round(hat.latency * 1000)}ms")
        print(f"{interaction.user.name} used the slash command")

    # Slash command to show the bot command list
    @hat.tree.command(name="help", description="Show the bot command list")
    async def help(interaction: discord.interactions):
        embed = embedComp.cuz_embed("Bot Command List", "", None, datetime.now())
        embed.add_field(name="Hello", value="Say Hello to someone!")
        embed.add_field(name="MBTI", value="Add your MBTI")
        embed.add_field(name="Ping", value="Check the bot latency")
        embed.add_field(name="Help", value="Show the bot command list")
        embed.add_field(name="Show Join Date", value="Show the user join date")
        embed.add_field(name="Show Role List", value="Show a user role he/she has")
        embed.add_field(name="My Role", value="Server user rock check (Self check)")
        embed.add_field(name="Talk", value="User message response")
        embed.add_field(name="Roll", value="Roll the dice game")
        await interaction.response.send_message(embed=embed)
        print(f"{interaction.user.name} used the slash command")

    # Slash command to test the bot
    @hat.tree.command(name="test", description="Test the bot")
    async def test(interaction: discord.interactions):
        await interaction.response.send_message("\x1b[38;2;233;30;99m")
        print(f"{interaction.user.name} used the slash command")

    # Slash command to roll the dice game
    @hat.tree.command(name="roll", description="Roll the dice game")
    async def roll(interaction: discord.Interaction):
        image_dir = "images/dice/"
        dice_image = os.listdir(image_dir)
        image_path = image_dir + random.choice(dice_image)
        image_file = discord.File(image_path)
        await interaction.response.send_message(
            f"Congratulation !!! {interaction.user.mention} you roll the number:",
            file=image_file,
        )
        print(f"({interaction.user.name}) roll the dice with [{image_path}]")

    # Menu command to show the user join date
    @hat.tree.context_menu(name="Show the User Join Date")
    async def user_info(interaction: discord.interactions, user: discord.Member):
        await interaction.response.send_message(
            f"Member Joined: {discord.utils.format_dt(user.joined_at)}", ephemeral=True
        )
        print(f"({interaction.user.name}) used the menu command")

    # Menu command to show a user role he/she has
    @hat.tree.context_menu(name="Show the User Role List")
    async def role_list(interaction: discord.interactions, user: discord.Member):
        roles = [role.name for role in user.roles if not role.is_default()]
        if not roles:
            await interaction.response.send_message(
                f"{user.mention} doesn't have any roles.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{user.mention} has the following roles: {', '.join(roles)}",
                ephemeral=True,
            )
        print(f"({interaction.user.name}) used the slash command")

    @hat.tree.context_menu(name="Translate")
    async def translate_message(
        interaction: discord.Interaction, message: discord.Message
    ):
        await interaction.response.defer(ephemeral=True)
        selected_text = message.content.strip() if message.content else None

        if not selected_text:
            await interaction.followup.send(
                "The selected message has no text to translate. Perhaps it's written in invisible ink like in the wizarding world!", ephemeral=True
            )
            return

        if len(selected_text) > 2000:
            await interaction.followup.send(
                "The selected message is too long to process (over 2000 characters). Even Hermione's enchanted bag can't hold this much text! Please select a shorter message.",
                ephemeral=True,
            )
            return

        try:
            translated_text = await translate_text(selected_text)
            max_length = 2000
            response_text = f"**Original Text:** {selected_text}\n\n**Translated Text:** {translated_text}"
            if len(response_text) > max_length:
                response_text = (
                    f"**Original Text:** {selected_text[:max_length//2]}...\n\n"
                    f"**Translated Text:** {translated_text[:max_length//2]}...\n\n"
                    f"**Note:** The text was truncated due to Discord's 2000-character limit. Even the Room of Requirement has its limits!"
                )
            await interaction.followup.send(response_text, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                f"An error occurred while translating the message: {str(e)}. It seems like a mischievous spell from Fred and George!",
                ephemeral=True,
            )

    # General bot command
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
    async def whisper(ctx: commands.Context, *, user_input):
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

    # Run the bot with the your discord API
    hat.run(setting.DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
