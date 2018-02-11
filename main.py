import os
import sys
import logging


usagestring = """Usage:\npython3 main.py clientcode (loglevel)\nwhere clientcode
is the discord bot clientcode, and\nloglevel is a valid log level
(default is WARNING)."""


def findLogLevel(logleveltofind):
    loglevels = {"debug": logging.DEBUG,
                 "info": logging.INFO,
                 "warning": logging.WARNING,
                 "error": logging.ERROR,
                 "critical": logging.CRITICAL}
    if logleveltofind.lower() in loglevels:
        return loglevels[logleveltofind.lower()]
    else:
        return None


def startFromEnviron():
    if os.environ.get("clientcode") is None:
        sys.exit("Error, discord client code not set. Set your "
                 "environ, or:\n{}".format(usagestring))
    elif os.environ.get("client_id") is None:
        sys.exit("Error, reddit client_id not set. Set your "
                 "environ, or:\n{}".format(usagestring))
    elif os.environ.get("client_secret") is None:
        sys.exit("Error, reddit client_secret not set. Set your "
                 "environ, or:\n{}".format(usagestring))
    elif os.environ.get("loglevel") is None:
        leveltoPass = logging.WARNING
    else:
        leveltoPass = findLogLevel(os.environ.get("loglevel"))

    import DaveBOT.core as bot
    if leveltoPass is None:
        botclient = bot.Dave(os.environ.get("clientcode"))
    else:
        botclient = bot.Dave(os.environ.get("clientcode"), leveltoPass)
    botclient.discout()


def startWithoneArg(sysargs):
    onearg = sysargs[1]
    if findLogLevel(onearg) is None:
        # Arg is not log level, so clientcode.
        import DaveBOT.core as bot
        botclient = bot.Dave(onearg)
        botclient.discout()
    else:
        # Arg is log level, so try environ for clientcode.
        if os.environ.get("clientcode") is None:
            sys.exit("Error, discord client code not set. Set your "
                     "environ, or:\n{}".format(usagestring))
        else:
            import DaveBOT.core as bot
            botclient = bot.Dave(clientcode, findLogLevel(onearg))
            botclient.discout()

def startWithClientAndLog(sysargs):
    clientcode = sysargs[1]
    leveltoPass = findLogLevel(sysargs[2])
    import DaveBOT.core as bot
    botclient = bot.Dave(clientcode, leveltoPass)
    botclient.discout()


def main():
    args = sys.argv
    numberofargs = len(args)
    if numberofargs == 1:
        startFromEnviron()
    elif numberofargs == 2:
        startWithClientArg(args)
    elif numberofargs == 3:
        startWithClientAndLog(args)
    else:
        sys.exit("Usage:\npython3 main.py clientcode loglevel\nwhere "
                 "clientcode is the discord bot clientcode, and\n"
                 "loglevel is a valid log level (default is INFO).\n")


if __name__ == "__main__":
    main()
