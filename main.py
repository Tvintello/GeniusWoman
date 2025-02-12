import discord
import dotenv
import os
from config import PREFIX, EN_RU_KEYBOARD_DICT, RUS_LETTERS, GAME_MODE
from scripts.general import GeneralFunctions
import wavelink


dotenv.load_dotenv()
TOKEN = str(os.getenv("TOKEN"))


def run():
    bot = discord.Bot(intents=discord.Intents.all(), prefix=PREFIX)
    funcs = GeneralFunctions(bot)
    messages = []

    async def connect_nodes():
        """Connect to our Lavalink nodes."""
        await bot.wait_until_ready()  # wait until the bot is ready

        nodes = [
            wavelink.Node(
                identifier="Node1",  # This identifier must be unique for all the nodes you are going to use
                uri="http://127.0.0.1:443",
                # Protocol (http/s) is required, port must be 443 as it is the one lavalink uses
                password="youshallnotpass"
            )
        ]

        await wavelink.Pool.connect(nodes=nodes, client=bot)  # Connect our nodes

    async def verify_alien(message: discord.Message) -> bool:
        text = message.content
        return not any([s in text for s in RUS_LETTERS]) and not text.startswith(PREFIX + "en") \
            and message.author in GAME_MODE

    @bot.event
    async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
        # Everytime a node is successfully connected, we
        # will print a message letting it know.
        print(f"Node with ID {payload.session_id} has connected")
        print(f"Resumed session: {payload.resumed}")

    @bot.event
    async def on_ready():
        await connect_nodes()  # connect to the server

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


