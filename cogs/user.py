from discord.ext import commands
import discord
from config import GAME_MODE
import typing
import wavelink


class UserCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(description="Turns on game mode to help people communicate with each other")
    async def switch_game_mode(self, ctx: discord.commands.context.ApplicationContext, user: discord.Member):
        if user in GAME_MODE:

            await ctx.respond(f"**Отключила** игровой режим для {user.name}")
        else:
            GAME_MODE.append(user)
            await ctx.respond(f"**Включила** игровой режим для {user.name}")

    @discord.slash_command(description="banger player")
    async def play_song(self, ctx: discord.commands.context.ApplicationContext, search: str):
        # First we may define our voice client,
        # for this, we are going to use typing.cast()
        # function just for the type checker know that
        # `ctx.voice_client` is going to be from type
        # `wavelink.Player`
        vc = typing.cast(wavelink.Player, ctx.voice_client)

        if not vc:  # We firstly check if there is a voice client
            try:
                vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                return await ctx.respond("Я не могу тебе нашептать на ушко, если ты не находишься в голосовом канале)")
            except discord.ClientException:
                await ctx.respond("У меня не получилось подключиться к каналу. Попробуй еще раз вызвать команду!")
                return
        print("CONTINUE1")

        # Now we are going to check if the invoker of the command
        # is in the same voice channel than the voice client, when defined.
        # If not, we return an error message.
        if ctx.author.voice.channel.id != vc.channel.id:
            return await ctx.respond("Ты куда убежал, я вообще-то в другом канале! Как я по твоему "
                                     "тебе скажу что-то, если ты ушел в другую комнату)")
        print("CONTINUE2")

        # Now we search for the song. You can optionally
        # pass the "source" keyword, of type "wavelink.TrackSource"
        song = await wavelink.Playable.search(search)
        print("CONTINUE3")

        if not song:  # In case the song is not found
            return await ctx.respond("Не нашла такой музыки, можно поточнее запрос!")  # we return an error message

        await vc.play(song[0])  # Else, we play it
        await ctx.respond(f"Играет: `{song[0].title}`")  # and return a success message


def setup(bot):
    bot.add_cog(UserCog(bot))
