from natsuko.base.COMMANDS import cmdtype
from natsuko.base import ROLES
import asyncio
import os

class CommandLoader():
    #ModuleName = "Generic"

    def __init__(self, name = "Generic", **kwargs):
        self.ModuleName = name
        self.Events = []
        self.overrides = kwargs.get("overrides")
        self.defaults = kwargs.get("defaults")
        self.prefix = kwargs.get("prefix", "!")

    def command(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                
                data = {"type"   : "Command", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}

                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)
                print(f"\t Load Command: {name} @ {f}\n\t\tPermissions: {data['roles']}")

            return f
        return deco


    def message(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                
                data = {"type"   : "Message", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def mention(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                
                data = {"type"   : "Mention", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def typing(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "Typing", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def delete(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                
                data = {"type"   : "Delete", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def edit(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                
                data = {"type"   : "Edit", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def ready(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                
                data = {"type"   : "Ready", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None,
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def reactadd(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "ReactAdd", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def reactremove(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "ReactRemove", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def reactclear(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "ReactClear", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def channeladd(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "ChannelAdd", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def channelremove(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "ChannelRemove", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def memberjoin(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "MemberJoin", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def memberleave(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "MemberLeave", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def memberupdate(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "MemberUpdate", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def ban(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "MemberBan", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def unban(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "MemberUnban", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def botjoin(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "BotJoin", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def guildenable(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "GuildEnable", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def guilddisable(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "GuildDisable", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco

    def guildchange(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "GuildChange", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def roleadd(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "RoleAdd",
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def roleremove(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "RoleRemove", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def pinsupdate(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "PinsUpdate", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def emojichange(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                # New
                data = {"type"   : "EmojiUpdate", 
                        "roles"  : None,
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco


    def voicechange(self, name, **options):

        def deco(f):
            if not asyncio.iscoroutinefunction(f):
                print('{0.__name__} command must be a coroutine'.format(f))

            else:
                data = {"type"   : "EmojiUpdate", 
                        "roles"  : ROLES.EVERYONE if "roles" not in options else options["roles"],
                        "error"  : True if "show_error" not in options else options["show_error"],
                        "filter" : None if "filter" not in options else options["filter"],
                        "name"   : name,
                        "channels": options.get("channels"),
                        "guilds" : options.get("guilds"),
                        "function": f,
                        "help"   : f.__doc__, "source": self.ModuleName}
                if self.defaults:
                    data.update({x: self.defaults[x] for x in [x for x in self.defaults.keys() if x in data.keys()] if data.get(x) is None})
                
                if self.overrides:
                    data.update(self.overrides)

                self.Events.append(data)

            return f
        return deco