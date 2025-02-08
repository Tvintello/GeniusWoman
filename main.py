import discord
import dotenv
import os
from config import PREFIX, EN_RU_KEYBOARD_DICT, RUS_LETTERS, GAME_MODE
from scripts.general import GeneralFunctions


dotenv.load_dotenv()
TOKEN = str(os.getenv("TOKEN"))


def run():
    bot = discord.Bot(intents=discord.Intents.all(), prefix=PREFIX)
    funcs = GeneralFunctions(bot)
    messages = []

    async def verify_alien(message: discord.Message) -> bool:
        text = message.content
        return not any([s in text for s in RUS_LETTERS]) and not text.startswith(PREFIX + "en") \
            and message.author in GAME_MODE

    @bot.event
    async def on_connect() -> None:
        bot.load_extension("cogs.admin")
        bot.load_extension("cogs.user")
        await bot.sync_commands()

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if message.author == bot.user:
            return
        if await verify_alien(message):
            await message.channel.send("".join([EN_RU_KEYBOARD_DICT[s] for s in message.content]) +
                                       f" (Перевод слов {message.author.name})")

    bot.run(TOKEN)


if __name__ == '__main__':
    run()


