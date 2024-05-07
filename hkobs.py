# It's the discord bot command list using the HKOBS API to get the weather infomation.
import discord
import requests
import json
import datetime
from datetime import datetime
from components import embedComp
from discord import app_commands

file = discord.File("images/hkobs/hko_trade_mark.png", filename="hko_trade_mark.png")

def get_weather(dataType, lang):
    # Get the weather data from the HKO API
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={dataType}&lang={lang}"
    try:
        response = requests.get(url)
        # Load the JSON response
        data = response.json()

        # Access specific data from the JSON response
        print(f"API JSON DATA: {json.dumps(data, indent=4)}")  # Replace 'key' with the actual key you want to access

        return data
    except requests.exceptions.RequestException as e:
        print('Error Info:', e)

def replace_null(data):
    # Replace the null value with a string
    for key, value in data.items():
        if value == "":
            data[key] = 'N/A'
    return data

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
        data = replace_null(get_weather('flw', f"{lang.value}"))
        if data:
            embed = embedComp.cuz_embed("***Weather forecast for Hong Kong***", "", 0x004a87, datetime.now())
            embed.add_field(name="Overview", value=data['generalSituation'])
            embed.add_field(name="Tropical Cyclone Information", value=data['tcInfo'])
            embed.add_field(name="Fire Hazard Warning Information", value=data['fireDangerWarning'])
            embed.add_field(name="Forecast period", value=data['forecastPeriod'])
            embed.add_field(name="Forecast", value=data['forecastDesc'])
            embed.add_field(name="Outlook", value=data['outlook'])
            embed.add_field(name="Update time", value=datetime.fromisoformat(data['updateTime'].removesuffix('Z')).strftime('%Y-%m-%d %H:%M:%S'))
            embed.set_footer(text="Data provided by the Hong Kong Observatory", icon_url="attachment://hko_trade_mark.png")
            await interaction.response.send_message(file=file, embed=embed)
        else:
            await interaction.response.send_message('Failed to get the weather data.')

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        embed = embedComp.cuz_embed("***My Embed***", "", 0x004a87)

        await interaction.response.send_message(embed=embed)    

async def setup(hat):
    hat.tree.add_command(HKOBS(name="hkobs", description="Weather Info From HKOBS API"))