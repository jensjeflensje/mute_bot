import os
from datetime import datetime

import discord
from discord.ext import commands, voice_recv

MAX_VIOLATIONS = 20
MAX_VOICE_POWER = 115
VIOLATION_TIMEOUT = 2 # seconds
BOT_TOKEN = os.environ["BOT_TOKEN"]

# TODO: This is probably not the opus path on your computer, unless you're also using macos.. :)
discord.opus.load_opus("/opt/homebrew/opt/opus/lib/libopus.dylib")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class Testing(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.violations: dict[int, list[datetime]] = {}

    def voice_callback(self, user: discord.Member, data: voice_recv.VoiceData):
        ext_data = data.packet.extension_data.get(
            voice_recv.ExtensionID.audio_power
        )
        if not ext_data:
            return

        # calculate the voice power to make it an int from 0 to 127
        value = int.from_bytes(ext_data, "big")
        power = 127 - (value & 127)

        user_violations = self.violations.get(user.id, [])
        if power > MAX_VOICE_POWER:
            user_violations.append(datetime.now())
            user_violations = list(
                filter(
                    # probably not the most efficient way to do this :P
                    lambda v: (datetime.now() - v).total_seconds() < VIOLATION_TIMEOUT, user_violations
                )
            )
            self.violations[user.id] = user_violations
            if len(user_violations) > MAX_VIOLATIONS:
                # if the user made more violations than MAX_VIOLATIONS in the last VIOLATION_TIMEOUT
                # then mute them
                # this MAX_VIOLATIONS is just a random number that you can tweak
                self.client.loop.create_task(user.edit(mute=True))

    @commands.command()
    async def mutebot(self, ctx):
        # join the user's channel and start recording audio
        vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
        vc.listen(voice_recv.BasicSink(self.voice_callback))

        # also unmute the user that executed this command, for good measure
        await ctx.author.edit(mute=False)

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def die(self, ctx):
        ctx.voice_client.stop()
        await ctx.bot.close()

@bot.event
async def on_ready():
    print('Logged in as {0.id}/{0}'.format(bot.user))
    print('------')

@bot.event
async def setup_hook():
    await bot.add_cog(Testing(bot))

bot.run(BOT_TOKEN)
