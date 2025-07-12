<p align="center">
	<img src="images/banner.png" alt="SortingHat Discord Bot Banner" style="max-width: 100%; height: auto;">
</p>

# SoritngHat Discord Bot

In the hallowed halls of the world of digital magic, the SortingHat Discord bot spreads its wings and proves the transformative power of the Internet. Born from the art of Python and the magic of discord.py, this bot casts spells and incantations to light the way for virtual conversations within the shimmering confines of the Discord server.

## Table of Contents

- [SoritngHat Discord Bot](#soritnghat-discord-bot)
	- [Table of Contents](#table-of-contents)
	- [Environment](#environment)
	- [Project Setup Guidelines](#project-setup-guidelines)
	- [Feature](#feature)
		- [Current Support Bot Command](#current-support-bot-command)
		- [Bot Function](#bot-function)
	- [Conclusion](#conclusion)

## Environment

The SortingHat-Discord Bot is built using discord.py 2.3.2 and Python 3.12.0. The chat ai part uses Hugging Face's Tramsfomer package and the google gemme 2b float-16 model.

## Project Setup Guidelines

1. **Clone the Repository**
	```bash
	git clone https://github.com/yourusername/SortingHat-Discord-bot.git
	cd SortingHat-Discord-bot
	```

2. **Create a Conda Environment**
	```bash
	conda create -n sortinghat-bot python=3.12
	conda activate sortinghat-bot
	```

3. **Install Dependencies**
	```bash
	pip install -r requirements.txt
	```

4. **Configure Environment Variables**
	- Create a `.env` file in the project root.
	- Add your Discord bot token and other required keys:
	  ```
	  DISCORD_TOKEN=your_discord_token_here
	  OLLAMA_API_URL=your_own_ollama_url
	  ```

5. **Run the Bot**
	```bash
	python bot.py
	```

6. **Optional: Update Model Files**
	- Download or update AI model files as needed for chat features.

Refer to the documentation for advanced configuration and troubleshooting.

## Feature

### Current Support Bot Command 

| Bot Command   | Description                      |
| ------------- | ---------------------------------|
| `./myrole`    | Check you self role in server    |
| `./talk`      | Talk with the bot (Fix response) | 
| `./roll`      | Randomly roll a Die              |
| `./chat`      | ChatGPT function using Gemma 2   |

### Bot Function 

* New member joins the Auto-Distribution Server Membership Group
* Welcome message for new members

## Conclusion

The project is still in the development phase and new features and commands will be added to the robot. Welcome to reference or directly use this warehouse, if you have better comments and ideas are also welcome to leave me a message, if you have encountered difficulties in the use, please feel free to leave a message, I do my best to provide help ～

