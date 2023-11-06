from modules.shared import emit_socketio_event, report_error
import asyncio, threading, queue
from twitchio.ext import commands
from time import sleep

# Define the bot's token, prefix, and initial channels
bot_token = 'ACCESS_TOKEN'
bot_prefix = '?'
initial_channels = ['...']

# Create a bot instance
bot = commands.Bot(
    token=bot_token,
    prefix=bot_prefix,
    initial_channels=initial_channels
)

def start_bot():
    asyncio.run(bot.start())

def initiate_tbot_connection():
    try:
        # Define the function to run the bot in a separate thread
        def run_bot_in_thread():
            # Create a new event loop for the thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_bot())

        # Start the bot in a separate thread
        thread = threading.Thread(target=run_bot_in_thread)
        thread.daemon = True
        thread.start()
        return thread
    except Exception as e:
        report_error("tbot_thread_error")
        return None


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
