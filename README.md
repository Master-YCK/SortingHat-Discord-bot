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
		- [Major Features](#major-features)
			- [1. Real-Time Hong Kong Weather Updates](#1-real-time-hong-kong-weather-updates)
			- [2. AI Chat Powered by Ollama](#2-ai-chat-powered-by-ollama)
			- [3. Basic Utility Features](#3-basic-utility-features)
	- [Conclusion](#conclusion)

## Environment

The SortingHat Discord Bot is developed with discord.py 2.5.2 and Python 3.12.2. For chat AI features, it connects to a self-hosted Ollama server, allowing users to easily select and switch between supported models such as Llama 3 (8B) and others available on Ollama. This flexible setup enables personalized AI chat experiences directly within Discord.

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

### Major Features

#### 1. Real-Time Hong Kong Weather Updates

Get instant weather info for Hong Kong using the Observatory API—current conditions, forecasts, and location-based details, all in Discord.

#### 2. AI Chat Powered by Ollama

Chat with advanced AI models like Llama 3 (8B) via Ollama for smart, natural conversations and Q&A, with easy model switching.

#### 3. Basic Utility Features

- **MBTI Role Assignment:** Assign MBTI personality roles to users for fun and community engagement.
- **Dice Rolling:** Roll a dice with customizable sides for games and random decisions.
- **Greeting:** Say hi to someone in the server with a friendly command.
- **Role Checker:** Check which server roles you or others have.
- **Other Fun Features:** Discover more interactive and interesting commands to enhance your Discord experience.

## Conclusion

The project is currently under active development, and new features and commands will be added regularly. You are welcome to reference or use this repository directly. If you have suggestions or ideas for improvement, please feel free to leave a message. Should you encounter any issues while using the bot, don't hesitate to reach out—I will do my best to assist you.

