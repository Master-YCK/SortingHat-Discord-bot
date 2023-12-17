# import discord
# import response
# from discord.ext import commands

# # Discord bot token
# TOKEN = "MTE4NTg1MTUwOTEyNTE2OTIxMg.GVV6un.aaWm2D92FXaEyc1SkY9CATdlUcZhFV62a0_MEE"
# # Setting the bot with accpet the message and response
# intents = discord.Intents.default()
# intents.message_content = True

# client = commands.Bot(command_prefix="./", intents=intents)


# async def send_message(message, user_message, is_private):
#     try:
#         # Get the response before sending
#         response_text = response.handle_response(user_message)
#         await message.author.send(
#             response_text
#         ) if is_private else await message.channel.send(response_text)

#     except Exception as e:
#         print(e)


# @client.event
# async def on_ready():
#     print(f"{client.user} is now running!")


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     username = str(message.author)
#     user_message = str(message.content)
#     channel = str(message.channel)

#     print(f"{username} said: '{user_message}' ({channel})")

#     if user_message.startswith("#"):
#         user_message = user_message[1:]
#         await send_message(message, user_message, is_private=True)
#     else:
#         await send_message(message, user_message, is_private=False)


# client.run(TOKEN)
