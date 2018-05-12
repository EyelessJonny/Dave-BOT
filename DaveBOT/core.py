import datetime
import logging
import logging.handlers
import platform
import queue
import signal
import sys

import discord
from discord.ext import commands


class Dave:
    """Main class for Bot."""
    def __init__(self, code, loglevel, redid, redsc, wk):
        self.client = commands.Bot(command_prefix="!")
        self.inittime = datetime.datetime.utcnow()
        self.code = code
        self.cogs = []
        if (redid and redsc):
            # Enable reddit cog.
            self.client.rid = redid
            self.client.rsc = redsc
            self.cogs.append("DaveBOT.cogs.reddit")
        if wk:
            # Enable weather cog.
            self.client.wk = wk
            self.cogs.append("DaveBOT.cogs.weather")
        # enable meme & rss cogs
        self.cogs.append("DaveBOT.cogs.memes")
        self.cogs.append("DaveBOT.cogs.rss")
        self.loadcogs()
        self.setupLogging(loglevel)
        self.host_is_Linux = True if ("Linux" in platform.system()) else False
        signal.signal(signal.SIGTERM, self.sigterm)

    def loadcogs(self):
        """Load discord.py cogs."""
        for cog in self.cogs:
            try:
                self.client.load_extension(cog)
            except Exception as e:
                self.logger.critical("Failed load {}, exception {}".format(cog,
                                                                           e))

    def setupLogging(self, loglev):
        """Sets up logging"""
        # Setup queue and queue handler:
        que = queue.Queue(-1)
        queue_handler = logging.handlers.QueueHandler(que)
        queue_handler.setLevel(loglev)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(queue_handler)
        # Setup listener:
        streamhandle = logging.StreamHandler()
        streamhandle.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
            " [in %(pathname)s:%(lineno)d]"))
        streamhandle.setLevel(loglev)
        listener = logging.handlers.QueueListener(que, streamhandle)
        listener.start()
        self.logger.warning("Logging is setup in core.py")

    def sigterm(self, signal, frame):
        """Response to sigterm."""
        self.client.logout()
        self.logger.critical("SIGTERM recieved, ending.")
        sys.exit("SIGTERM recieved, ending.")

    async def uptimeFunc(self):
        """Returns formatted host uptime."""
        if self.host_is_Linux:
            from datetime import timedelta
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = str(timedelta(seconds=uptime_seconds))
            return uptime_string
        else:
            self.logger.warning("Host is not linux, uptimeFunc not supported.")
            return "incomp host."

    def discout(self):
        """Discord functions and client running."""
        @self.client.event
        async def on_ready():
            """Outputs on successful launch."""
            self.logger.warning("Login Successful")
            self.logger.warning("Name : {}" .format(self.client.user.name))
            self.logger.warning("ID : {}" .format(self.client.user.id))
            self.logger.info("Successful self.client launch.")
            await self.client.change_presence(game=discord.Game(name="for !help", type=3))

        @self.client.command(pass_context=True)
        async def dave(ctx):
            """Provides data about Dave and the system it's running on."""
            self.logger.info("!dave called.")
            await self.client.send_typing(ctx.message.channel)
            if self.host_is_Linux:
                e = discord.Embed(title="Dave-BOT",
                                  type="rich",
                                  description="Info on dave & it's host.",
                                  url="https://github.com/DaveInc/Dave-BOT",
                                  colour=0xFFDFAA,
                                  timestamp=datetime.datetime.utcnow())
                e.set_thumbnail(url="https://theeu.uk/dave.jpg")
                delta_uptime = datetime.datetime.utcnow() - self.inittime
                hours, remainder = divmod(int(delta_uptime.total_seconds()),
                                          3600)
                minutes, seconds = divmod(remainder, 60)
                days, hours = divmod(hours, 24)
                botuptime = "{}d, {}h, {}m, {}s.".format(days,
                                                         hours,
                                                         minutes,
                                                         seconds)
                e.add_field(name="Bot Uptime", value=botuptime, inline=True)
                e.add_field(name="Host Uptime", value=await self.uptimeFunc(),
                            inline=True)
                e.add_field(name="Python V", value=platform.python_version(),
                            inline=True)
                e.add_field(name="Python Compiler",
                            value=platform.python_compiler(),
                            inline=True)
                lindist = platform.linux_distribution()
                lindists = "{};v{}".format(lindist[0], lindist[1])
                e.add_field(name="Distro", value=lindists, inline=True)
                await self.client.say(embed=e)
            else:
                self.logger.warning("Host not linux, !dave is not supported.")
                await self.client.say("Host !=linux; feature coming soon.\n")

        self.client.run(str(self.code))


if __name__ == "__main__":
    raise sys.exit("This is an import file, please do not run directly.")
