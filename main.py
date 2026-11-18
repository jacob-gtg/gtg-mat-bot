import asyncio
import discord
import scraper
from discord.ext import commands
from time import time
import os

TOKEN = os.getenv("BOT_TOKEN")
last = 0

COOLDOWN = 20
HELP = """GTG matbot
`?mat <resturang>`: visa maten på en viss resturang
`?meny <resturang>`: visa veckans meny för en resturang
`?hemsida <resturang>`: skicka en länk till hemsidan av en resturang (WORK IN PROGRESS)
`?help`: visa hjälp

`<resturang>` kan vara `träffpunkten`, `höjden`, `balansen`, `backyard` eller lämnas tomt för träffpunkten
"""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Okänt kommando. Använd `{bot.command_prefix}help` för att se tillgänliga kommandon.")
    else:
        raise error

async def prep(ctx):
    global last
    if ctx.channel.name != "commands":
        await ctx.send('Kör komandot i #commands')
        return

    if (time() - last) < COOLDOWN:
        await ctx.send(f"Spamma inte komandot! (vänta {str(int(COOLDOWN + last - time()))} sekunder)")
        return

    last = time()

@commands.command()
async def mat(ctx, resturang: str | None):
    await prep(ctx)

    await ctx.send('Hämtar maten idag...')
    msg = await asyncio.gather(asyncio.to_thread(scraper.get_food, resturang, False),)
    await ctx.send(msg[0])


@commands.command()
async def meny(ctx, resturang: str | None):
    await prep(ctx)

    await ctx.send('Hämtar menyn för veckan...')
    msg = await asyncio.gather(asyncio.to_thread(scraper.get_food, resturang, True),)
    await ctx.send(msg[0])

@commands.command()
async def help(ctx):
    await prep(ctx)
    await ctx.send(HELP)

bot.add_command(mat)
bot.add_command(meny)
bot.add_command(help)
bot.run(TOKEN)
