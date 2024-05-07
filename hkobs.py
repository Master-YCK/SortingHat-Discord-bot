# It's the discord bot command list using the HKOBS API to get the weather infomation.
import discord
import requests
from discord import app_commands

def get_weather(dataType, lang):
    # Get the weather data from the HKO API
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={dataType}&lang={lang}"
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print('Error Info:', e)
        return None

class HKOBS(app_commands.Group):
    @app_commands.command()
    async def flw(self, interaction: discord.Interaction):
        # Get the forecast data
        data = get_weather('flw', 'en')
        if data:
            await interaction.response.send_message(data)
        else:
            await interaction.response.send_message('Failed to get the weather data.')

async def setup(hat):
    hat.tree.add_command(HKOBS(name='hkobs', description='Get the weather information from the HKOBS'))