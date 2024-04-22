# Import the defulat function
import os

# Import the dotenv 
from dotenv import load_dotenv

#load you .env config for the API token
load_dotenv()

# Get the API token from the .env file.
DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
# Setup the message channel ID of you own server
WELCOME_CHANNEL = 1185848222321754144