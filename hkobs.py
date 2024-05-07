# It's the discord bot command list using the HKOBS API to get the weather infomation.
import discord
import requests
from discord import app_commands

def get_weather(dataType, lang):
    # Get the weather data from the HKO API
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={dataType}&lang={lang}"
    try:
        response = requests.get(url)
        # Load the JSON response
        data = response.json()

        # Access specific data from the JSON response
        print(f"API JSON DATA: {data['generalSituation']}")  # Replace 'key' with the actual key you want to access

        return data
    except requests.exceptions.RequestException as e:
        print('Error Info:', e)

class HKOBS(app_commands.Group):
    @app_commands.command(name="flw", description="本港地區天氣預報")
    @app_commands.describe(lang="Choose the language")
    @app_commands.choices(lang=[
        discord.app_commands.Choice(name='English', value='en'),
        discord.app_commands.Choice(name='繁體中文', value='tc'),
        discord.app_commands.Choice(name='简体中文', value='sc')
    ])
    async def flw(self, interaction: discord.Interaction, lang: discord.app_commands.Choice[str]):
        # Get the forecast data
        data = get_weather('flw', f"{lang.value}")
        if data:

            await interaction.response.send_message(f"{data['generalSituation']}")
        else:
            await interaction.response.send_message('Failed to get the weather data.')

async def setup(hat):
    hat.tree.add_command(HKOBS(name="hkobs", description="Weather Info From HKOBS API"))