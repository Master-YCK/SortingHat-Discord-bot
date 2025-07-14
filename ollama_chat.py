import discord
import setting
import asyncio
from discord import app_commands
from ollama import Client

client = Client(
    host=setting.OLLAMA_API_URL,
)


class OllamaChat(app_commands.Group):
    lock = asyncio.Lock()  # Class-level lock to prevent concurrent access

    @app_commands.command(
        name="ask", description="Interact with the Sorting Hat's magical AI wisdom!"
    )
    @app_commands.describe(prompt="Your message to the Sorting Hat")
    async def chat(self, interaction: discord.Interaction, prompt: str):
        try:
            await interaction.response.defer()  # Defer the response to avoid timeout
            harry_potter_prompt = (
                f"You are the Sorting Hat from Harry Potter, ancient and wise, residing atop the heads of Hogwarts students. "
                f"Speak in a whimsical, magical, and slightly mischievous tone, weaving references to Hogwarts, its four houses, famous wizards, magical creatures, and spells. "
                f"Offer guidance, riddles, or playful advice as the Sorting Hat would, and always stay in character. "
                f"Reply to the user's question in Traditional Chinese. "
                f"User's question: {prompt}"
            )
            async with OllamaChat.lock:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(
                    None, lambda: client.generate("llama3.1:8b", harry_potter_prompt)
                )
            reply = f"> {prompt}\n\n**Sorting Hat says:** {response.response}"
            if len(reply) > 2000:
                chunks = [reply[i : i + 2000] for i in range(0, len(reply), 2000)]
                await interaction.followup.send(chunks[0])
                for chunk in chunks[1:]:
                    await interaction.channel.send(chunk)
            else:
                await interaction.followup.send(reply)
        except Exception as e:
            print("Error Info:", e)
            await interaction.followup.send(
                "Alas! The magic faltered. Please try again, young wizard."
            )


async def setup(hat):
    hat.tree.add_command(
        OllamaChat(
            name="chatgpt",
            description="Converse with the Sorting Hat's magical AI wisdom!",
        )
    )
