import discord

class EmbedEngine():

    def __init__(self, client):
        self.client = client
        self.bot_name = client.user.name

    def err_invalid(self, string):
        print("MAKE: ERROR self.client")
        em = discord.Embed(title="Invalid Command", description=string)
        em.set_author(name=self.bot_name, icon_url=self.client.user.avatar_url)
        em.colour = discord.Colour.red()
        return em

    def make(self, string, title="Natsuko Framework"):
        em = discord.Embed(title=title, description=string)
        em.set_author(name=self.bot_name, icon_url=self.client.user.avatar_url)
        em.colour = discord.Color.blue()
        return em

    def success(self, string, title="Natsuko Framework"):
        em = discord.Embed(title=title, description=string)
        em.set_author(name=self.bot_name, icon_url=self.client.user.avatar_url)
        em.colour = discord.Colour.green()
        return em

    def failed(self, string, title="Natsuko Framework"):
        em = discord.Embed(title=title, description=string)
        em.set_author(name=self.bot_name, icon_url=self.client.user.avatar_url)
        em.colour = discord.Colour.red()
        return em

