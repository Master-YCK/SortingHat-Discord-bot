# SoritngHat Discord Bot

In the hallowed halls of the world of digital magic, the SortingHat Discord bot spreads its wings and proves the transformative power of the Internet. Born from the art of Python and the magic of discord.py, this bot casts spells and incantations to light the way for virtual conversations within the shimmering confines of the Discord server.

## Table of Contents

- [Environment](#environment)

- [How to Use](#installation)

- [Feature](#Feature)

## Environment

The SortingHat-Discord Bot is built using discord.py 2.3.2 and Python 3.12.0. The chat ai part uses Hugging Face's Tramsfomer package and the google gemme 2b float-16 model.

## Installation

1. If you can't use pip on your computer command line, please download python 3.12.0 first.
	<https://www.python.org/downloads/>

2. Step 1: to run this bot on your own computer, server or any device, you need the required pip installation package, the required pip package requirement.txt file has been created in the project.

	```bash
	pip  install  requirements.txt
	```
	
3. Step 2: Create an ```.env``` file in the code directory and enter access to the Hugging Face LLM and your Discord Bot API access with create ```DISCORD_API_TOKEN``` and ```HF_TOKEN``` variable in the ```.env``` file ( Data type should be String ).

	```bash
	# Discord bot token
	DISCORD_API_TOKEN = 'You Token Here'
	# Hugging Face Access Token
	HF_TOKEN = 'You Token Here'
	```
	
4. Step 3: Change the ```WELCOME_CHANNEL``` variable in the ```setting.py``` code file to the ID of your personal server welcome channel ( Data type should be Int ).

	```bash
	# Setup the welcome message channel ID of you own server
	WELCOME_CHANNEL  =  You Discord server channel ID
	```
	If you can't find your Discord Server Welcome Channel ID, turn on "Developer Mode" in Settings, 			 then right-click on the Welcome Channel and you can copy the channel ID.

5. Step 4:  After completing the above runtime environment settings, you just need to run the ```main.py``` file.

## Feature

Examples and instructions on how to use your project.

## License

Information about the license for your project.

SortingHat Discord Bot