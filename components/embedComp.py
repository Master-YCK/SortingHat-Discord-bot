import discord

def cuz_embed (tile, des, col, dt):
    embed = discord.Embed(
        title=f"{tile}",
        description=f"{des}",
        color=col,
        timestamp=dt,
    )
    return embed