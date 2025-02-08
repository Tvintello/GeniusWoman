from discord.ext import commands
import discord
from config import GAME_MODE, EN_RU_DICTIONARY


class UserCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(description="Turns on game mode to help people communicate with each other")
    async def turn_on_game_mode(self, ctx: discord.commands.context.ApplicationContext, user: discord.Member):
        user_name = "".join([EN_RU_DICTIONARY[s] for s in user.name])
        if user in GAME_MODE:
            user_name = user_name + "а" if not user_name[-1] in ("а", "е", "и", "о", "у", "ю", "й", "я") else user_name
            await ctx.respond(f"Игровой режим у {user_name} уже включен")
        else:
            GAME_MODE.append(user)
            await ctx.respond(f"Включен игровой режим {user_name}")


def setup(bot):
    bot.add_cog(UserCog(bot))
