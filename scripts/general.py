import discord
from discord.ext import commands


class GeneralFunctions:
    def __init__(self, bot: commands.Bot):
        self.timers = {}
        self.bad_counter = {}
        self.bot = bot

