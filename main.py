import discord
import response
import datetime
from discord.ext import commands

# Discord bot token
TOKEN = "MTE4NTg1MTUwOTEyNTE2OTIxMg.GVV6un.aaWm2D92FXaEyc1SkY9CATdlUcZhFV62a0_MEE"
# Setting the bot permession
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

welcome_channel = 1185848222321754144 
#1071065748631466024

client = commands.Bot(command_prefix="./", intents=intents)

# Bot start message
def run():
    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")

    #Welcome message and auto assign a user role
    @client.event
    async def on_member_join(member):
        channel = client.get_channel(welcome_channel)
        role = discord.utils.get(member.guild.roles, name = "麻瓜")
        await member.add_roles(role)

        embed = discord.Embed(
            title = f'**Welcome to Hogwarts !**',
            description = f'**{member.mention}** come to the Hogwarts, but he/she is a **{role.name}** !!!',
            color = 0xff55ff,
            timestamp = datetime.datetime.now()
        )

        await channel.send(embed = embed)

    # async def on_member_join(member):
    #     # 发送欢迎消息
    #     await member.send("欢迎加入！请回答以下五个问题，以帮助我们了解你。")

    #     # 提问五个问题
    #     answers = []
    #     for i in range(5):
    #         question = f"问题 {i+1}: "
    #         await member.send(question)
            
    #         def check(msg):
    #             return msg.author == member and msg.channel.type == discord.ChannelType.private

    #         response = await client.wait_for('message', check=check)
    #         answers.append(response.content)

    #     # 根据回答进行身份分组
    #     role_name = get_group_based_on_answers(answers)  # 请自行实现这个函数
    #     role = discord.utils.get(member.guild.roles, name=role_name)

    #     if role:
    #         await member.add_roles(role)
    #         await member.send(f"你已被分配到 {role_name} 组！")

    # def get_group_based_on_answers(answers):
    #     # 这是一个示例函数，根据回答返回身份组的名称
    #     # 请根据你的需求实现具体的逻辑
    #     if answers.count("Yes") >= 3:
    #         return "GroupA"
    #     else:
    #         return "GroupB"

    # Server user rock check (Self check)
    @client.command()
    async def myrole(ctx):
        user = ctx.author
        roles = [role.name for role in user.roles if not role.is_default()]
        if not roles:
            await ctx.send(f"{ctx.author.mention} doesn't have any roles.")
        else:
            await ctx.send(f"{ctx.author.mention} has the following roles: {', '.join(roles)}")

    # Message response
    @client.command()
    async def talk(ctx, *, message):
        response_text = response.handle_response(message)

        if response_text == "Sorry, what 7 you said ar ????":
            image_url = "images\what 7 you said.jpg"
            image_file = discord.File(image_url)
            await ctx.send(f"{ctx.author.mention}, {response_text}", file=image_file)
        else:
            await ctx.send(f"{ctx.author.mention}, {response_text}")

    # Run the bot with you own token
    client.run(TOKEN)

 # run the bot
if __name__ == "__main__":
    run()
