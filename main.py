import asyncio
import discord
import scraper
from discord.ext import commands
from time import time
import os

TOKEN = os.getenv("BOT_TOKEN")
last = 0

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

@commands.command()
async def mat(ctx, resturang: str | None):
    global last
    if ctx.channel.name != "commands":
        await ctx.send('Kör komandot i #commands')
        return

    if (time() - last) < 40:
        await ctx.send(f"Spamma inte komandot! (vänta {str(int(40 + last - time()))} sekunder)")
        return

    last = time()
    await ctx.send('Hämtar maten idag...')
    msg = await asyncio.gather(asyncio.to_thread(scraper.get_food, resturang), )
    await ctx.send(msg[0])

bot.add_command(mat)
bot.run(TOKEN)
