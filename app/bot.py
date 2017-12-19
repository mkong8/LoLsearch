import discord
from discord.ext.commands import Bot
from config import TOKEN
import riot


my_bot = Bot(command_prefix="!")

@my_bot.event
async def on_ready():
    print("theGoon is ready...")

@my_bot.command()
async def hello():
    return await my_bot.say("Hello there.")

@my_bot.command()
async def embed():
    embed = discord.Embed(title="Title", description="Description", colour=0x00ff00)
    embed.set_author(name="dog", icon_url="https://vignette.wikia.nocookie.net/leagueoflegends/images/2/2b/Shyvana_OriginalSkin.jpg/revision/latest?cb=20170615200806")
    embed.add_field(name="Field1", value='Hi', inline=False)
    embed.add_field(name="Field2", value='Hi2', inline=True)
    return await my_bot.say(embed=embed)

@my_bot.command()
async def ranked(*, summoner_name: str):
    await my_bot.say("retrieving data...")
    output = get_ranks(summoner_name)
    return await my_bot.say(output)

@my_bot.command(pass_context = True)
async def clear(ctx, number):
    mgs = [] # Empty list to put all the messages in the log
    number = int(number) + 1 # Converting the amount of messages to delete to an integer
    async for x in my_bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await my_bot.delete_messages(mgs)

@my_bot.command()
async def shutdown():
    my_bot.logout()

my_bot.run(TOKEN)