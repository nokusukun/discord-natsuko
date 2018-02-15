from natsuko.base.ModuleManager import ModuleManager
from natsuko.base import EmbedUtils as embed
from natsuko.base.Map import Map
from natsuko.base import LOADER

from dotmap import DotMap
import requests
import discord

import importlib.util
import traceback
import shelve
import shlex
import os


class NatsukoClient(discord.Client):
    def __init__(self, **kwargs):
        self.bot_name = kwargs.get("bot_name", "Generic Bot")
        self.token = kwargs.get("token", None)
        self.is_bot = kwargs.get("is_bot", True)
        self.owners = kwargs.get("owners", [])
        self.roles = kwargs.get("roles", {})
        self.prefixes = []
        if not self.token:
            raise Exception("Missing token.")
        self.client = discord.Client()
        self.modules = {}
        self.manager = ModuleManager(self)
        self.module_loads = []
        self.bot_store = shelve.open(f"{self.bot_name}.store", writeback=True)


    def run(self):
        self.assign_events()
        print(self.modules)
        self.client.run(self.token, is_bot=self.is_bot)


    def load_module_gist(self, link):
        self.module_loads.append({"type": "gist", "path": link})
        module_link = link
        if "gist.github.com" not in module_link:
            raise Exception("The link is not a gist.github link")
            return

        module_name = module_link.split("/")[-1]
        module_path = "modules/remote!{}.py".format(module_name)
        module_link = module_link.replace("gist.github.com", "gist.githubusercontent.com") + "/raw/"
        module_link = module_link.replace("//raw","/raw")

        with open(module_path, "w") as f:
            data = requests.get(module_link, headers={'Cache-Control': 'no-cache'})
            f.write(data.text)

        load_result = self.load_module_file(module_path)
        return load_result


    def load_module_file(self, path):
        self.module_loads.append({"type": "file", "path": path})
        name = os.path.split(path)[-1].split(".")[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        files_modules = [getattr(mod, x) for x in dir(mod) if type(getattr(mod, x)) == LOADER.CommandLoader]
        for module in files_modules:
            self.load_module(module)


    def load_module(self, module):
        if type(module) == LOADER.CommandLoader:
            self.modules[module.ModuleName] = module


    def assign_events(self):
        self.client.event(self.on_message)
        self.client.event(
            self.event_factory(
                event="on_typing",
                cmdtype="Typing",
                args=["channel", "user", "when"]))
        self.client.event(
            self.event_factory(
                event="on_ready",
                cmdtype="Ready"))
        self.client.event(
            self.event_factory(
                event="on_message_delete",
                cmdtype="Delete",
                args=["message"]))
        self.client.event(
            self.event_factory(
                event="on_message_edit",
                cmdtype="Edit",
                args=["old", "new"]))
        self.client.event(
            self.event_factory(
                event="on_reaction_add",
                cmdtype="ReactAdd",
                args=["reaction", "user"]))
        self.client.event(
            self.event_factory(
                event="on_reaction_remove",
                cmdtype="ReactRemove",
                args=["reaction", "user"]))
        self.client.event(
            self.event_factory(
                event="on_reaction_clear",
                cmdtype="ReactClear",
                args=["message", "reactions"]))
        self.client.event(
            self.event_factory(
                event="on_channel_delete",
                cmdtype="ChannelRemove",
                args=["channel"]))
        self.client.event(
            self.event_factory(
                event="on_member_join",
                cmdtype="MemberJoin",
                args=["user"]))
        self.client.event(
            self.event_factory(
                event="on_member_remove",
                cmdtype="MemberLeave",
                args=["user"]))
        self.client.event(
            self.event_factory(
                event="on_member_update",
                cmdtype="MemberUpdate",
                args=["old", "new"]))
        self.client.event(
            self.event_factory(
                event="on_member_ban",
                cmdtype="MemberBan",
                args=["guild", "user"]))
        self.client.event(
            self.event_factory(
                event="on_member_unban",
                cmdtype="MemberUnban",
                args=["user"]))
        self.client.event(
            self.event_factory(
                event="on_guild_join",
                cmdtype="BotJoin",
                args=["guild"]))
        self.client.event(
            self.event_factory(
                event="on_guild_update",
                cmdtype="GuildChange",
                args=["old", "new"]))
        self.client.event(
            self.event_factory(
                event="on_guild_available",
                cmdtype="GuildEnable",
                args=["guild"]))
        self.client.event(
            self.event_factory(
                event="on_guild_unavailable",
                cmdtype="GuildDisable",
                args=["guild"]))
        self.client.event(
            self.event_factory(
                event="on_guild_role_create",
                cmdtype="RoleAdd",
                args=["role"]))
        self.client.event(
            self.event_factory(
                event="on_guild_role_delete",
                cmdtype="RoleRemove",
                args=["role"]))
        self.client.event(
            self.event_factory(
                event="on_guild_emojis_update",
                cmdtype="EmojiUpdate",
                args=["guild", "old", "new"]))
        self.client.event(
            self.event_factory(
                event="on_voice_state_update",
                cmdtype="VoiceUpdate",
                args=["user", "old", "new"]))
        self.client.event(
            self.event_factory(
                event="on_guild_channel_pins_update",
                cmdtype="PinsUpdate",
                args=["channel", "last_pin"]))

    async def on_message(self, message):
        prefixes = [x.prefix for x in list(self.modules.values())]
        if message.content.startswith("~~diediedie") and message.author.id in self.owners:
            quit()

        event = DotMap({})
        event.message = message
        event.guild = message.guild
        event.user = message.author
        event.channel = message.channel
        print(f"[command]: {message.content}")
        # Execute all of the on_message commands first
        await self.manager.execute(command=None, 
                                cmdtype="Message", 
                                event=event, 
                                client=self.client)

        # Checks if it actually is a command
        command_prefix = [x for x in prefixes if message.content.startswith(x)] 
        if not command_prefix:
            return
        
        try:
            event.args = shlex.split(message.content[len(command_prefix[0]):])
        except:
            event.args = message.content[len(command_prefix[0]):]
        command = message.content.split(" ")[0][len(command_prefix[0]):]
        # Execute any commands
        
        await self.manager.execute( command=command, 
                                    cmdtype="Command", 
                                    event=event, 
                                    client=self.client)


    def event_factory(self, **kwargs):
        print(f"Registering Event: {kwargs}")

        async def event_func(*args):
            event = DotMap({})
            for i, argument in enumerate(kwargs.get("args", [])):
                setattr(event, argument, args[i])
                event.user = getattr(args[i], "author", None) if not event.user else event.user
                event.channel = getattr(args[i], "channel", None) if not event.channel else event.channel
                event.guild = getattr(args[i], "guild", None) if not event.guild else event.guild
            
            # Attach Stores 
            store = DotMap({})
            for attribute, attachable in event.items():
                if "id" in dir(attachable):
                    if str(attachable.id) not in self.bot_store:
                        self.bot_store[str(attachable.id)] = {}
                    store[attribute] = self.bot_store[str(attachable.id)]

            event.store = store
            print("\n\nStore\n", store)
            print("\n\nEvent\n", event)
            await self.manager.execute(
                                command=kwargs.get("command"),
                                cmdtype=kwargs.get("cmdtype"),
                                event=event,
                                client=self.client)

        event_func.__name__ = kwargs["event"]
        return event_func
