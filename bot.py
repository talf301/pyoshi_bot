import os

import discord
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
pYoshiPattern = r"\bpYoshi\b"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = None
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(guild)
    pyoshi = get(guild.roles, name="pYoshis")

    for member in guild.members:
        dname = member.nick if member.nick else member.name
        # check if they're named pYoshi and aren't a pYoshi
        match = re.search(pYoshiPattern, dname)
        if match:
            if pyoshi not in member.roles:
                await member.add_roles(pyoshi)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f'{member.name} is now a pYoshi, as of ', current_time)
        else:
            if pyoshi in member.roles:
                await member.remove_roles(pyoshi)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f'{member.name} is no longer a pYoshi, as of ', current_time)


@client.event
async def on_member_update(before, after):
    # Becoming a pyoshi
    bname = before.nick if before.nick else before.name
    aname = after.nick if after.nick else after.name
    beforeMatchmatch = re.search(pYoshiPattern, bname)
    afterMatchmatch = re.search(pYoshiPattern, aname)

    if not beforeMatchmatch and afterMatchmatch:
        await after.add_roles(get(after.guild.roles, name="pYoshis"))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{after.name} is now a pYoshi, as of ', current_time)
    # Becoming a human
    elif beforeMatchmatch and not afterMatchmatch:
        await after.remove_roles(get(after.guild.roles, name="pYoshis"))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{after.name} is no longer a pYoshi, as of ', current_time)

client.run(TOKEN)
