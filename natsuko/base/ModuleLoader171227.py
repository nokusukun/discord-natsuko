import glob
import os
import importlib.util
import asyncio
from os.path import basename
from base.Map import Map
from base import EmbedUtils as embed
from base import SessionManager as SM
from base import LOADER
import traceback
import settings
from pprint import pprint
import colorama
from colorama import Fore, Back, Style
colorama.init()


class ModuleLoader():
    

    def __init__(self):
        self.modules = []
        # Finds all of the python files
        print("{}Disukudo - Natsuko Bot Framework{}".format(Fore.CYAN, Style.RESET_ALL))
        modules = glob.glob("modules/*.py", recursive=True)
        self.clear_remotes(modules)

        for x in modules:
            try:
                print(Style.BRIGHT, end="\r")
                print("{}ModLoader --> {}{}{}".format(Fore.BLUE, Fore.YELLOW, basename(x)[:-3], Fore.GREEN))
                spec = importlib.util.spec_from_file_location(basename(x)[:-3], x)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                loaders = [getattr(mod, x) for x in dir(mod) if type(getattr(mod, x)) == LOADER.CommandLoader]
                print(loaders)
                for i in loaders:
                    print(i.ModuleName)
                    print([x["name"] for x in i.Events])
                self.modules.extend(loaders)
            except:
                print("\t{}Load Failed".format(Fore.RED))
            print(Style.RESET_ALL, end="\r")

        #print(self.modules)


    def reload(self):
        # Finds all of the python files
        self.modules = []
        modules = glob.glob("modules/*.py", recursive=True)
        modules_ret = []
        for x in modules:
            try:
                print(Style.BRIGHT, end="\r")
                print("{}ModLoader --> {}{}{}".format(Fore.BLUE, Fore.YELLOW, basename(x)[:-3], Fore.GREEN))
                spec = importlib.util.spec_from_file_location(basename(x)[:-3], x)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                loaders = [getattr(mod, x) for x in dir(mod) if type(getattr(mod, x)) == LOADER.CommandLoader]
                print(loaders)
                for i in loaders:
                    print(i.ModuleName)
                    print([x["name"] for x in i.Events])
                self.modules.extend(loaders)
            except:
                print("\t{}Load Failed".format(Fore.RED))
            print(Style.RESET_ALL, end="\r")

        return modules_ret


    def load_module(self, path, name):
        try:
            print(Style.BRIGHT, end="\r")
            print("{}ModLoader --> {}{}{}".format(Fore.CYAN, Fore.YELLOW, name, Fore.GREEN))
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            loaders = [getattr(mod, x) for x in dir(mod) if type(getattr(mod, x)) == LOADER.CommandLoader]
            #self.modules.extend(loaders)
            self.modules.append(loaders)
            print(Style.RESET_ALL, end="\r")
            return (loaders.ModuleName,)
        except:
            return (None, "".join(traceback.format_exc()))


    def clear_remotes(self, modlist):
        removal = [x for x in modlist if "remote!" in x]
        for m in removal:
            try:
                os.remove(m)
            except:
                pass


    async def filter(self, event, options):
        if options.event:
            if event.get("guilds") and options.event.guild:
                if options.event.guild.id not in  event["guilds"]:
                    return False

            if event.get("channels") and options.event.channel:
                if options.event.channel.id not in event["channels"]:
                    return False

        if event["type"] != options.cmdtype:
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
                        for x in settings.ROLE:
                            if role in settings.ROLE[x] and max_pow < x:
                                max_pow = x
                    if req_pow > max_pow and options.event.user.id != settings.OWNER:
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
        options = Map(options)
        options.client.embeds = embed.EmbedEngine(options.client)
        options.client.config = lambda x: SM.SessionManager(f"botdata\\{x}")

        for module in self.modules:
            for event in module.Events:
                #print(event["type"])
                fl_res = await self.filter(event, options)
                if not fl_res:
                    continue

                print(f"Check Success, Executing Command.")
                if options.event:
                    if "channel" in options.event:
                        print(f"Source: #{options.event.channel.name}({options.event.channel.id})")
                pprint(event)

                try:
                    print(Style.RESET_ALL, end="\r")
                    await event["function"](options.event, options.client)
                    print(Style.BRIGHT, end="\r")
                except:
                    traceback.print_exc()
                    if event["help"]:
                        print("{}[cmd:{}] !".format(Fore.RED, options.cmdtype))
                        em = embed.err_invalid(event["help"], options.client)
                        await options.event.message.channel.send(embed=em)
                    elif event["error"]:
                        print("{}[cmd:{}] !!".format(Fore.RED, options.cmdtype))
                        em=embed.err_invalid("Command Error!", options.client)
                        await options.event.message.channel.send(embed=em)

        print(Style.RESET_ALL, end="\r")