import asyncio
import discord
import nordrest_scraper
import provschema_scraper
import os
import datetime
from discord.ext import commands
from time import time
from helpers import error

TOKEN = os.getenv("BOT_TOKEN")
last = 0

COOLDOWN = 20
HELP = """GTG utils
`?mat <resturang>`: visa maten på en viss resturang
`?meny <resturang>`: visa veckans meny för en resturang
`?prov`: visa kommande prov
`?help`: visa hjälp
`?idag`: visa maten idag på båda resturanger
`?imorgon`: visa maten imorgon på båda resturanger

`<resturang>` kan vara `träffpunkten`, `höjden` eller lämnas tomt för träffpunkten
"""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)
allowed_mentions = discord.AllowedMentions(everyone = True)


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

    embed = (await asyncio.gather(asyncio.to_thread(nordrest_scraper.get_food, resturang)))[0]
    await ctx.send(embed=embed)


@commands.command()
async def meny(ctx, resturang: str | None):
    if await cooldown(ctx): return

    for i in range(5):
        # Vi använder inte gather här, eftersom cachen är mer effektiv
        embed = (await asyncio.gather(asyncio.to_thread(nordrest_scraper.get_food, resturang, i)))[0]
        await ctx.send(embed=embed)

@commands.command()
async def idag(ctx):
    if await cooldown(ctx): return

    embed = (await asyncio.gather(asyncio.to_thread(nordrest_scraper.get_food, "träffpunkten")))[0]
    await ctx.send(embed=embed)

    embed = (await asyncio.gather(asyncio.to_thread(nordrest_scraper.get_food, "höjden")))[0]
    await ctx.send(embed=embed)

@commands.command()
async def imorgon(ctx):
    if await cooldown(ctx): return

    dag = datetime.datetime.now().isocalendar().weekday  # vi subtraherar inte
    if dag > 4:         
        return error("Imorgon är inte en arbetsdag")

    embed = (await asyncio.gather(asyncio.to_thread(
        nordrest_scraper.get_food, "träffpunkten", dag)))[0]
    await ctx.send(embed=embed)

    embed = (await asyncio.gather(asyncio.to_thread(
        nordrest_scraper.get_food,"höjden", dag)))[0]
    await ctx.send(embed=embed)

@commands.command()
async def prov(ctx):
    if await cooldown(ctx): return

    embed = (await asyncio.gather(asyncio.to_thread(provschema_scraper.get_prov)))[0]
    await ctx.send(embed=embed)


@commands.command()
async def suggest_time(ctx):
    channel = discord.utils.get(ctx.guild.channels, name='dnd-tider')
    if channel is None: return

    now = datetime.datetime.now()

    embed = discord.Embed(
        title="DnD Tidförslag",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name=f"Kan du spela DnD {discord.utils.format_dt(now, style='F')}?",
        value="Reagera med ✅ eller ❌",
        inline=False
    )

    msg: discord.Message = await channel.send(
        embed=embed,
        content="@everyone",
        allowed_mentions=allowed_mentions
    )
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

@commands.command()
async def resistance(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    author = ctx.author
    await author.send("Join the resistance!\nhttps://discord.gg/njz24tQ6Uh")

@commands.command()
async def svartamarknaden(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    author = ctx.author
    await author.send("Berätta inte för någon...\nhttps://svartamarknaden.borstell.dev/")

@commands.command()
async def help(ctx):
    if await cooldown(ctx): return
    await ctx.send(HELP)


bot.add_command(mat)
bot.add_command(meny)
bot.add_command(idag)
bot.add_command(imorgon)

bot.add_command(prov)
bot.add_command(suggest_time)
bot.add_command(help)
bot.add_command(resistance)
bot.add_command(svartamarknaden)

bot.run(TOKEN)

