import discord
import requests
from time import time

USER_AGENT = "gtg-mat-bot-(jacob.borstell@gtg.se)"
HEADERS = {"User-Agent": USER_AGENT}

GLOBAL_CACHE_TTL = 60 * 10

def error(msg):
    embed = discord.Embed(
        title="Fel",
        color=discord.Color.blue(),
    )
    embed.add_field(name=msg, value="", inline=False)
    return embed

class CachedEndpoint:
    def __init__(self, url):
        self.url: str = url
        self.last_request_timestamp: float = 0.0
        self.response: requests.Response | None = None

    def clear(self):
        self.response = None
        self.last_request_timestamp = 0

    def request(self):
        if (time() > (self.last_request_timestamp + GLOBAL_CACHE_TTL)
            or self.response is None):

            self.response = requests.get(self.url, headers=HEADERS)
            self.last_request_timestamp = time()

        return self.response
