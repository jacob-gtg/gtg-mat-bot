import asyncio
import discord
import nordrest_scraper
import provschema_scraper
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

async def cooldown(ctx: discord.ext.commands.Context) -> bool:
    global last
    if ctx.channel.name != "commands":
        await ctx.send("Kör kommandot i #commands istället")
        return True

    if (time() - last) < COOLDOWN:
        await ctx.send(f"Spamma inte komandot! (vänta {str(int(COOLDOWN + last - time()))} sekunder)")
        return True

    last = time()
    return False

@commands.command()
async def mat(ctx, resturang: str | None):
    if await cooldown(ctx): return

    msg = await asyncio.gather(asyncio.to_thread(nordrest_scraper.get_food, resturang, False), )
    await ctx.send(msg[0])


@commands.command()
async def meny(ctx, resturang: str | None):
    if await cooldown(ctx): return

    msg = await asyncio.gather(asyncio.to_thread(nordrest_scraper.get_food, resturang, True), )
    await ctx.send(msg[0])

@commands.command()
async def prov(ctx):
    if await cooldown(ctx): return

    msg = await asyncio.gather(asyncio.to_thread(provschema_scraper.get_prov))
    await ctx.send(msg[0])

@commands.command()
async def help(ctx):
    if await cooldown(ctx): return
    await ctx.send(HELP)

bot.add_command(mat)
bot.add_command(meny)
bot.add_command(prov)
bot.add_command(help)
bot.run(TOKEN)
