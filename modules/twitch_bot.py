'''from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='ACCESS_TOKEN', prefix='?', initial_channels=['...'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_error(self, error, data=None):
        # An event handler to be called when an error occurs inside an event handler...
        # This does not include check errors or command errors...
        print(error)
    
    async def event_command_error(self, ctx, error):
        # This event is called when an error is raised inside a command either from a check or the body of a command...
        # For example, if a user tries to use a command but they don't have permission to do so, you can handle that here...
        # For this example, we will just print the error and continue on...
        print(error)

    async def event_redemption(self, redemption):
        # This is called when a user redeems a reward...
        # You can do anything you want with this, for example, grant the user a role, or send them a DM...
        print(f'{redemption.user.display_name} redeemed {redemption.reward.title}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # We want to ignore these messages or we will end up in a loop...
        if message.echo:
            return

        # Process commands...
        await self.handle_commands(message)

    
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()'''