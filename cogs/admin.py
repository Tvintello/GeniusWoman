from discord.ext import commands
import discord


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(AdminCog(bot))
