import discord
import requests
import datetime
from datetime import datetime
from components import embedComp
from discord import app_commands

hkobs_logo = (
    "https://www.weather.gov.hk/en/abouthko/logoexplain/images/HKOLogo-color-symbol.png"
)

weather_warning_sign = {
    "WTS": "https://upload.wikimedia.org/wikipedia/commons/2/24/Thunderstorm_Warning.png",
    "WRAINA": "https://upload.wikimedia.org/wikipedia/commons/8/83/Amber_Rainstorm_Signal.png",
    "WRAINR": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Red_Rainstorm_Signal.png",
    "WRAINB": "https://upload.wikimedia.org/wikipedia/commons/c/c0/Black_Rainstorm_Signal.png",
    "TC1": "https://upload.wikimedia.org/wikipedia/commons/a/a9/No._01_Standby_Signal.png",
    "TC3": "https://upload.wikimedia.org/wikipedia/commons/7/7b/No._03_Strong_Wind_Signal.png",
    "TC8NW": "https://upload.wikimedia.org/wikipedia/commons/1/17/No._8_Northwest_Gale_or_Storm_Signal.png",
    "TC8SW": "https://upload.wikimedia.org/wikipedia/commons/c/c7/No._8_Southwest_Gale_or_Storm_Signal.png",
    "TC8NE": "https://upload.wikimedia.org/wikipedia/commons/4/49/No._8_Northeast_Gale_or_Storm_Signal.png",
    "TC8SE": "https://upload.wikimedia.org/wikipedia/commons/0/04/No._8_Southeast_Gale_or_Storm_Signal.png",
    "TC9": "https://upload.wikimedia.org/wikipedia/commons/7/7a/No._09_Increasing_Gale_or_Storm_Signal.png",
    "TC10": "https://upload.wikimedia.org/wikipedia/commons/3/3d/No._10_Hurricane_Signal.png",
}

def_text_lang = "tc"


def replace_null(data):
    # Replace the null value with a string
    for key, value in data.items():
        if value == "":
            data[key] = "N/A"
    return data


def get_weather(dataType, lang):
    # Get the weather data from the HKO API
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={dataType}&lang={lang}"
    try:
        response = requests.get(url)
        # Load the JSON response
        data = response.json()
        # Access specific data from the JSON response
        # print(f"API JSON DATA: {json.dumps(data, indent=4)}")
        return data
    except requests.exceptions.RequestException as e:
        print("Error Info:", e)


def place_name():
    enData = replace_null(get_weather("rhrread", "en"))
    cnData = replace_null(get_weather("rhrread", "tc"))
    placeList = []
    for i in range(len(enData["temperature"]["data"])):
        placeList.append(
            discord.app_commands.Choice(
                name=f"{enData['temperature']['data'][i]['place']}({cnData['temperature']['data'][i]['place']})",
                value=i,
            )
        )
    return placeList[0:25]


last_warnsum_data = None  # Store the last fetched data


async def check_warnsum_periodically():
    global last_warnsum_data
    new_data = get_weather("warnsum", def_text_lang)
    if new_data:
        if last_warnsum_data != new_data:
            last_warnsum_data = new_data
            print("New weather warning summary data received.")
            return new_data
        else:
            print("No new weather warning summary data.")
    return None

class HKOBS(app_commands.Group):
    # Set the text language for the command
    @app_commands.command(
        name="setlang",
        description="Set the text language for the command (English, Traditional Chinese, Simplified Chinese)",
    )
    @app_commands.describe(lang="Choose the language")
    @app_commands.choices(
        lang=[
            discord.app_commands.Choice(name="English", value="en"),
            discord.app_commands.Choice(name="繁體中文", value="tc"),
            discord.app_commands.Choice(name="简体中文", value="sc"),
        ]
    )
    async def setlang(
        self, interaction: discord.Interaction, lang: discord.app_commands.Choice[str]
    ):
        def_text_lang = lang.value
        await interaction.response.send_message(
            f"The default language set to {lang.name}"
        )
        print(f"HKOBS default language set to {def_text_lang}/{lang.name}")

    # The commands checking the weather information
    @app_commands.command(name="flw", description="本港地區天氣預報(Weather Forecast)")
    async def flw(self, interaction: discord.Interaction):
        # Get the forecast data
        data = replace_null(get_weather("flw", f"{def_text_lang}"))
        if data:
            embed = embedComp.cuz_embed(
                "***Weather forecast for Hong Kong***", "", 0x004A87, datetime.now()
            )
            embed.add_field(
                name="Overview", value=data["generalSituation"], inline=False
            )
            if data["tcInfo"] != "N/A":
                embed.add_field(
                    name="Tropical Cyclone Information", value=data["tcInfo"]
                )
            if data["fireDangerWarning"] != "N/A":
                embed.add_field(
                    name="Fire Hazard Warning Information",
                    value=data["fireDangerWarning"],
                )
            embed.add_field(name="Outlook", value=data["outlook"])
            embed.add_field(name="Forecast", value=data["forecastDesc"])
            embed.add_field(name="Forecast period", value=data["forecastPeriod"])
            embed.add_field(
                name="Update time",
                value=datetime.fromisoformat(
                    data["updateTime"].removesuffix("Z")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            )
            embed.set_footer(
                text="Data provided by the Hong Kong Observatory", icon_url=hkobs_logo
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Failed to get the weather data.")

    # Get the weather information for today
    @app_commands.command(name="today", description="今日天氣概況(Weather Today)")
    @app_commands.describe(place="Choose the place")
    @app_commands.choices(place=place_name())
    async def today(
        self, interaction: discord.Interaction, place: discord.app_commands.Choice[int]
    ):
        # Get the today data
        data = replace_null(get_weather("rhrread", f"{def_text_lang}"))
        if data:
            embed = embedComp.cuz_embed(
                f"***Today's weather in {data['temperature']['data'][place.value]['place']}***",
                "",
                0x004A87,
                datetime.now(),
            )
            embed.add_field(
                name="Place", value=data["temperature"]["data"][place.value]["place"]
            )
            embed.add_field(
                name="Temperature",
                value=f"{data['temperature']['data'][place.value]['value']}°",
            )
            embed.add_field(
                name="Humidity", value=f"{data['humidity']['data'][0]['value']}%"
            )

            if data["uvindex"] != "N/A":
                embed.add_field(
                    name="UV Index", value=data["uvindex"]["data"][0]["value"]
                )
                embed.add_field(
                    name="UV Index Desc", value=data["uvindex"]["data"][0]["desc"]
                )

            embed.add_field(
                name="Update time",
                value=datetime.fromisoformat(
                    data["temperature"]["recordTime"].removesuffix("Z")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            )
            embed.set_footer(
                text="Data provided by the Hong Kong Observatory", icon_url=hkobs_logo
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Failed to get the weather data.")

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        embed = embedComp.cuz_embed(
            "***Rain Warning Test***", "Amber Rainstorm Signal", None, None
        )
        embed.set_thumbnail(url=rain_warning_sign["WRAINA"])
        embed.add_field(name="Warning Type", value="Amber Rainstorm Signal")
        await interaction.response.send_message(embed=embed)


async def setup(hat):
    hat.tree.add_command(HKOBS(name="hkobs", description="Weather Info From HKOBS API"))
