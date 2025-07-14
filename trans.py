import discord
import asyncio
from discord import app_commands
from googletrans import Translator


async def translate_text(text: str, dest_language: str = "zh-tw") -> str:
    translator = Translator()
    try:
        translated = await translator.translate(text, dest=dest_language)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails


class Translation(app_commands.Group):
    @app_commands.command(
        name="translate", description="Translate text to a different language."
    )
    @app_commands.describe(text="Text to translate")
    async def translate(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer(ephemeral=True)
        translated_text = await translate_text(text)
        await interaction.followup.send(
            f"**Original Text:** {text}\n\n**Translated Text:** {translated_text}",
            ephemeral=True,
        )


async def setup(hat):
    hat.tree.add_command(
        Translation(
            name="translator",
            description="Translate text to a different language.",
        )
    )
