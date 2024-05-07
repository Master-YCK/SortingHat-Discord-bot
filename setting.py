# Import the defulat function
import os

# Import the dotenv 
from dotenv import load_dotenv

#load you .env config for the API token
load_dotenv()

# Get the API token from the .env file.
DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
# Setup the message channel ID of you own server
WELCOME_CHANNEL = 1071065748631466024