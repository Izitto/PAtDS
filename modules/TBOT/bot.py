from twitchio.ext import commands, eventsub, pubsub
import os

bot = commands.Bot(
    token= '',

    nick = 'izittobot',
    prefix = '!',
    initial_channels = ["izitto"]
)

@bot.event()
async def event_ready():
    print(f'Logged into Twitch | {bot.nick}')
    print(f'Channels: {bot.connected_channels}')

@bot.event()
async def event_message(message):
    print(message.content)



