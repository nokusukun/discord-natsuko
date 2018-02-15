from natsuko.base import LOADER
from natsuko.base import ROLES
from dotmap import DotMap
import asyncio
import discord
import requests
import io
from PIL import Image
import numpy as np
import operator


on = LOADER.CommandLoader("val_event", prefix="<3")


on.command("resetcounter")
async def resetcounter(event, client):
    client.store["ship_counter"] = client.store.get("ship_counter", 0)
    client.store["ship_counter"] = 0
    await event.channel.send("I-it's not like I want to reset the counter because of you or anything.")


@on.command("myotp")
async def myotp(event, client):
    userA = event.user
    if len(event.args) > 1:
        userA = event.guild.get_member_named(event.args[1])
    otps = {}
    for member in event.guild.members:
        userB = member
        otps[member.display_name] = int(str(userA.id + userB.id)[-2:]) + int(str(userA.id + userB.id)[5])
    xx = "\n".join(f"{x}: {otps[x]}%" for x in sorted(otps, key=otps.get, reverse=True)[:20])
    await event.channel.send(f"```yaml\n{xx}```")


on.command("ship")
async def ship(event, client):
    """
    **ship** [userA] [userB/MiA Character]
    Ship two members and get a compatibility rating!
    """
    client.store["ship_counter"] = client.store.get("ship_counter", 0)
    client.store["ship_counter"] += 1
    print("Debug.ship_counter ", client.store["ship_counter"])
    userA = None
    userB = None

    if len(event.args) >= 3:
        userA = event.guild.get_member_named(event.args[1])

    if len(event.message.mentions) >= 1 and userA is None:
        userA = event.message.mentions[0]

    if len(event.message.mentions) >= 2:
        userB = event.message.mentions[1]

    if len(event.args) >= 3 and userB is None:
        userB = event.guild.get_member_named(event.args[2])

    if len(event.args) >=3:
        if userB is None:
            ub = event.args[2]
            usr_b_id = sum([ord(z) for z in ub])
            userB = DotMap({"id":int(usr_b_id), "display_name": ub})

    if userA is None or userB is None:
        em = client.embeds.err_invalid(ship.__doc__)
        x = await event.message.channel.send(embed=em)
        await asyncio.sleep(8)
        await event.message.delete()
        return await x.delete()


    compatibility = int(str(userA.id + userB.id)[-2:]) + int(str(userA.id + userB.id)[5])
    a_name = "".join(z for z in userA.display_name.split(" ")[0] if str.isalnum(z))
    b_name = "".join(z for z in userB.display_name.split(" ")[0] if str.isalnum(z))
    ship_name = a_name[:int(len(a_name)/ 2)] + b_name[int(len(b_name)/ 2):]
    await image_gen(userA, userB)
    
    message = f"**{userA.display_name}** and **{userB.display_name}** has been shipped! <:valentineboir:410932014158708736>**SS {ship_name}**<:valentineboi:410931996228059137> has sailed!\n{'Holy mackerel! ' if compatibility > 98 else ''}This ship is **{compatibility}%** compatible.:hearts:"
    with open("return.jpg", "rb") as f:
        await event.message.channel.send(message, file=discord.File(f))
        # await event.message.channel.send(f"```yaml\nDEBUG: ship_compatibility_rating: {compatibility}%\nDEBUG: ship_ship_name: {ship_name}```", file=discord.File(f))
    await event.message.channel.send(f"_{client.store['ship_counter']} people have helped Mio with her research!_")

async def image_gen(a, b):
    a_avi = requests.get(a.avatar_url_as(format="jpg", size=256), stream=True)
    a_avi = io.BytesIO(a_avi.content)
    try:
        b_avi = requests.get(b.avatar_url_as(format="jpg", size=256), stream=True)
        b_avi = io.BytesIO(b_avi.content)
    except:
        b_avi = None
        charmap = { "riko":     "riko.png",
                    "reg":      "reg.png",
                    "nanachi":  "nanachi.png",
                    "bondrewd": "bondrewd.jpg",
                    "ozen":     "ozen.png",
                    "prushka":  "prushka.jpg",
                    "faputa":   "faputa.png",
                    "maru":     "maru.png",
                    "nat":      "nat.jpg",
                    "shiggy":   "shiggy.jpg",
                    "mitty":    "mitty.jpg"}
        for name, src in charmap.items():
            if name in b.display_name.lower():
                b_avi = src
            
        if b_avi is None:
            b_avi = "default.jpg"

    images = [Image.open(x) for x in [a_avi, 'flatboilove.jpg', b_avi]]
    widths, heights = zip(*(i.size for i in images))

    min_shape = sorted([(np.sum(i.size), i.size ) for i in images])
    print(min_shape)
    min_shape = min_shape[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in images) )
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save( 'return.jpg' )  
