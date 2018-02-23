import glob
import os
import importlib.util
import asyncio
from os.path import basename
from natsuko.base.Map import Map
from natsuko.base import EmbedUtils as embed
from natsuko.base import SessionManager as SM
from natsuko.base import LOADER
import traceback
from pprint import pprint
from dotmap import DotMap
import colorama
from colorama import Fore, Back, Style
colorama.init()


class ModuleManager():

    def __init__(self, natsuko):
        self.natsuko = natsuko


    def load_module(self, path, name):
        try:
            print(Style.BRIGHT, end="\r")
            print("{}ModLoader --> {}{}{}".format(Fore.CYAN, Fore.YELLOW, name, Fore.GREEN))
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            loaders = [getattr(mod, x) for x in dir(mod) if type(getattr(mod, x)) == LOADER.CommandLoader]
            #self.modules.extend(loaders)
            self.natsuko.modules.append(loaders)
            print(Style.RESET_ALL, end="\r")
            return (loaders.ModuleName,)
        except:
            return (None, "".join(traceback.format_exc()))


    async def filter(self, event, options, module):
        if options.event:
            if event.get("guilds") and options.event.guild:
                if options.event.guild.id not in  event["guilds"]:
                    return False

            if event.get("channels") and options.event.channel:
                if options.event.channel.id not in event["channels"]:
                    return False

        if event["type"] != options.cmdtype:
            return False

        if options.event.message and options.cmdtype == "Command":
            if not options.event.message.content.startswith(module.prefix):
                return False

        if event["type"] == "Command":
            #print(event)
            if event["name"] != options.command:
                return False

            if event["roles"]:
                max_pow = 1
                req_pow = event["roles"]
                if req_pow != 1:
                    for role in [x.name for x in options.event.user.roles]:
                        for x in self.natsuko.roles:
                            if role in self.natsuko.roles[x] and max_pow < x:
                                max_pow = x
                    if req_pow > max_pow and options.event.user.id not in self.natsuko.owners:
                        em = embed.failed("You don't have enough permissions for that.", options.client)
                        msg = await options.event.message.channel.send(embed=em)
                        await asyncio.sleep(10)
                        await msg.delete()
                        return False

        if event["filter"]:
            if not event["filter"](options.event):
                return False

        return True


    async def execute(self, **options):
        #print(f"Event: {options['']}")
        options = DotMap(options)
        options.client.embeds = embed.EmbedEngine(options.client)
        options.client.config = lambda x: SM.SessionManager(os.path.join("botdata", x))
        options.client.store = self.natsuko.bot_store

        for module in list(self.natsuko.modules.values()):
            for event in module.Events:
                print(event)
                fl_res = await self.filter(event, options, module)
                if not fl_res:
                    continue
                print("Running!")
                #print(f"Check Success, Executing Command.")
                if options.event and options.cmdtype != "Message":
                    if options.event.channel is not None:
                        try:
                            print(f"Source: #{options.event.channel.name}({options.event.channel.id})")
                        except:
                            print(f"Source: #unknown({options.event.channel.id})")
                    #pprint(event)

                try:
                    print(Style.RESET_ALL, end="\r")
                    asyncio.ensure_future(event["function"](options.event, options.client))
                    print(Style.BRIGHT, end="\r")
                except:
                    traceback.print_exc()
                    if event["help"]:
                        print("{}[cmd:{}] !".format(Fore.RED, options.cmdtype))
                        em = options.client.embeds.err_invalid(event["help"])
                        await options.event.message.channel.send(embed=em)
                    elif event["error"]:
                        print("{}[cmd:{}] !!".format(Fore.RED, options.cmdtype))
                        em= options.client.embeds.err_invalid("Command Error!")
                        await options.event.message.channel.send(embed=em)

        print(Style.RESET_ALL, end="\r")