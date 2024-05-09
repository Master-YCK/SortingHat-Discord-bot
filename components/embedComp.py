import discord

def cuz_embed (tile, des, col, dt):
    
    if col == None:
        col = discord.Color.random()
    elif dt == None:
        dt = ''

    embed = discord.Embed(
        title=f"{tile}",
        description=f"{des}",
        color=col,
        timestamp=dt,
    )
    return embed