import glob
import os
import importlib.util
import asyncio
from os.path import basename
from base.Map import Map
from base import EmbedUtils as embed
import traceback
import settings

import colorama
from colorama import Fore, Back, Style
colorama.init()


class ModuleLoader():
    modules = []

    def __init__(self):
        # Finds all of the python files
        print("{}Disukudo - Natsuko Bot Framework{}".format(Fore.CYAN, Style.RESET_ALL))
        modules = glob.glob("modules/*.py", recursive=True)
        self.clear_remotes(modules)

        # Taken from: http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        for x in modules:
            try:
                print(Style.BRIGHT, end="\r")
                print("{}ModLoader --> {}{}{}".format(Fore.BLUE, Fore.YELLOW, basename(x)[:-3], Fore.GREEN))
                spec = importlib.util.spec_from_file_location(basename(x)[:-3], x)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.modules.append(mod)
            except:
                print("\t{}Load Failed".format(Fore.RED))
            print(Style.RESET_ALL, end="\r")


    def reload(self):
        # Finds all of the python files
        self.modules = []
        modules = glob.glob("modules/*.py", recursive=True)
        modules_ret = []
        # Taken from: http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        for x in modules:
            try:
                print(Style.BRIGHT, end="\r")
                print("{}ModLoader --> {}{}{}".format(Fore.MAGENTA, Fore.YELLOW, basename(x)[:-3], Fore.GREEN))
                spec = importlib.util.spec_from_file_location(basename(x)[:-3], x)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.modules.append(mod)
                modules_ret.append("Load OK: {}".format(basename(x)[:-3]))
            except:
                print("\t{}Load Failed".format(Fore.RED))
                modules_ret.append("Load FAIL: {}".format(basename(x)[:-3]))
                traceback.print_exc();
            print(Style.RESET_ALL, end="\r")
        return modules_ret


    def load_module(self, path, name):
        # Taken from: http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        try:
            print(Style.BRIGHT, end="\r")
            print("{}ModLoader --> {}{}{}".format(Fore.CYAN, Fore.YELLOW, name, Fore.GREEN))
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.modules.append(mod)
            print(Style.RESET_ALL, end="\r")
            return (mod.module_name,)
        except:
            return (None, "".join(traceback.format_exc()))

    def clear_remotes(self, modlist):
        removal = [x for x in modlist if "remote!" in x]
        for m in removal:
            try:
                os.remove(m)
            except:
                pass


    async def execute(self, **options):
        options = Map(options)
        options.client.loader = self

        for mod in self.modules:
            # How is this appending
            # I have no idea
            # What was I drinking?!
            commands = getattr(mod.on, options.cmdtype)


        print(Style.BRIGHT, end="\r")

        if options.command is None:
            for func in list(commands.values()):
                try:
                    print(Style.BRIGHT, end="\r")
                    print("{}[cmd:{}] ?> {}".format(Fore.GREEN, options.cmdtype, func.__name__))
                    print(Style.RESET_ALL, end="\r")
                    await func(options.event, options.client)
                    print(Style.BRIGHT, end="\r")
                except:
                    print(traceback.print_exc())
            return

        
        print("{}[cmd:{}] ?> {}".format(Fore.YELLOW, options.cmdtype, options.command))
        
        if options.command in commands:
            print("{}[cmd:{}] OK> {}".format(Fore.GREEN, options.cmdtype, options.event.args))
            #try:
            max_pow = 1
            req_pow = mod.on._role[options.command]
            print(req_pow)
            if req_pow != 1:
                for role in [x.name for x in options.event.user.roles]:
                    for x in settings.ROLE:
                        if role in settings.ROLE[x] and max_pow < x:
                            max_pow = x
                print(max_pow)
                if req_pow > max_pow:
                    em = embed.failed("You don't have enough permissions for that.", options.client)
                    msg = await options.event.message.channel.send(embed=em)
                    await asyncio.sleep(10)
                    await msg.delete()
                    return
                

                # print("user_roles: {0}".format(ascii(user_roles)))
            #except:
            #    pass

            try:
                print(Style.RESET_ALL, end="\r")
                await commands[options.command](options.event, options.client)
                print(Style.BRIGHT, end="\r")
            except:

                try:
                    traceback.print_exc()
                    if commands[options.command].__doc__ is not None:
                        print("{}[cmd:{}] !".format(Fore.RED, options.cmdtype))
                        em = embed.err_invalid(commands[options.command].__doc__, options.client)
                    else:
                        print("{}[cmd:{}] !".format(Fore.RED, options.cmdtype))
                        em = embed.err_invalid(mod.on._help[options.command], options.client)
                    await options.event.message.channel.send(embed=em)
                except:
                    traceback.print_exc()
                    print("{}[cmd:{}] !!".format(Fore.RED, options.cmdtype))
                    em=embed.err_invalid("Generic command Error!", options.client)
                    await options.event.message.channel.send(embed=em)

        print(Style.RESET_ALL, end="\r")
