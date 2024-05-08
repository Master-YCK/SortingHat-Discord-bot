# It's the discord bot command list using the HKOBS API to get the weather infomation.
import discord
import requests
import json
import datetime
from datetime import datetime
from components import embedComp
from discord import app_commands

file = discord.File("images/hkobs/hko_trade_mark.png", filename="hko_trade_mark.png")

def replace_null(data):
    # Replace the null value with a string
    for key, value in data.items():
        if value == "":
            data[key] = 'N/A'
    return data

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

def place_name():
    enData = replace_null(get_weather('rhrread', 'en'))
    cnData = replace_null(get_weather('rhrread', 'tc'))
    placeList = []
    for i in range(len(enData['temperature']['data'])):
        placeList.append(discord.app_commands.Choice(name=f"{cnData['temperature']['data'][i]['place']}({enData['temperature']['data'][i]['place']})", value=i))
    return placeList[0:25]

class HKOBS(app_commands.Group):
    # The commands checking the weather information
    @app_commands.command(name="flw", description="本港地區天氣預報(Weather Forecast)")
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
            if data['tcInfo'] != 'N/A':
                embed.add_field(name="Tropical Cyclone Information", value=data['tcInfo'])
            if data['fireDangerWarning'] != 'N/A':
                embed.add_field(name="Fire Hazard Warning Information", value=data['fireDangerWarning'])
            embed.add_field(name="Outlook", value=data['outlook'])
            embed.add_field(name="Forecast", value=data['forecastDesc'])
            embed.add_field(name="Forecast period", value=data['forecastPeriod'])
            embed.add_field(name="Update time", value=datetime.fromisoformat(data['updateTime'].removesuffix('Z')).strftime('%Y-%m-%d %H:%M:%S'))
            embed.set_footer(text="Data provided by the Hong Kong Observatory", icon_url="attachment://hko_trade_mark.png")
            await interaction.response.send_message(file=file, embed=embed)
        else:
            await interaction.response.send_message('Failed to get the weather data.')

    # Get the weather information for today
    @app_commands.command(name="today", description="今日天氣概況(Weather Today)")
    @app_commands.describe(lang="Choose the language")
    @app_commands.choices(lang=[
        discord.app_commands.Choice(name='English', value='en'),
        discord.app_commands.Choice(name='繁體中文', value='tc'),
        discord.app_commands.Choice(name='简体中文', value='sc')
    ])
    @app_commands.describe(place="Choose the place")
    @app_commands.choices(place=place_name())

    async def today(self, interaction: discord.Interaction, lang: discord.app_commands.Choice[str], place: discord.app_commands.Choice[int]):
        # Get the today data
        data = replace_null(get_weather('rhrread', f"{lang.value}"))
        if data:
            place_name()
            embed = embedComp.cuz_embed(f"***Today's weather in {data['temperature']['data'][place.value]['place']}***", "", 0x004a87, datetime.now())
            embed.add_field(name="Place", value=data['temperature']['data'][place.value]['place'])
            embed.add_field(name="Temperature", value=f"{data['temperature']['data'][place.value]['value']}°")
            embed.add_field(name="Humidity", value=f"{data['humidity']['data'][0]['value']}%")
            embed.add_field(name="UV Index", value=data['uvindex']['data'][0]['value'])
            embed.add_field(name="UV Index Desc", value=data['uvindex']['data'][0]['desc'])
            embed.add_field(name="Update time", value=datetime.fromisoformat(data['temperature']['recordTime'].removesuffix('Z')).strftime('%Y-%m-%d %H:%M:%S'))
            embed.set_footer(text="Data provided by the Hong Kong Observatory", icon_url="attachment://hko_trade_mark.png")
            await interaction.response.send_message(file=file, embed=embed)
        else:
            await interaction.response.send_message('Failed to get the weather data.')

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        embed = embedComp.cuz_embed("***My Embed***", "Test", None, None)
        await interaction.response.send_message(embed=embed)    

async def setup(hat):
    hat.tree.add_command(HKOBS(name="hkobs", description="Weather Info From HKOBS API"))