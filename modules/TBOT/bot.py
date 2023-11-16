from modules.shared import emit_socketio_event, report_error
import asyncio, threading, queue
from twitchio.ext import commands
from time import sleep

# Define the bot's token, prefix, and initial channels
bot_token = '5d22t69yjjq4gjbb9y6u2oknh0wgmo'
bot_prefix = '?'
initial_channels = ['izitto']

# Create a bot instance
bot = commands.Bot(
    token=bot_token,
    prefix=bot_prefix,
    initial_channels=initial_channels
)

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=bot_token, prefix=bot_prefix, initial_channels=[initial_channels[0]])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()


def initiate_tbot_connection():
    try:
        def run(send_queue):
            sleep(5)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete('''start bot''')

        thread = threading.Thread(target=run, args=(send,))
        thread.daemon = True
        thread.start()
        return thread
    except Exception as e:
        report_error("tbot_thread_error")
        return None
