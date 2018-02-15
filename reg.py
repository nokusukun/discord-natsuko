import natsuko
from natsuko.base import ROLES

regu = natsuko.NatsukoClient(
			bot_name="Reg", 
			token="MzcyNzQ0MzMwNjYzOTUyNDA0.DNIovQ.We2S0bAnXjP1WoAYjxRAvh5AK6k") #This doesn't work

regu.owners.append(217121568256557056) #That's me!
regu.roles = {
	ROLES.ADMIN:	["Admin", "Owner", "White Whistles"],
	ROLES.MOD:		["Bot People", "Mod", "Black Whistles"],
	ROLES.SPECIAL:	["Cinnamon Bun"],
	ROLES.EVERYONE:	["@everyone"]}

regu.load_module_file("modules\\anime.py")
regu.load_module_file("kigo.py")
regu.load_module_gist("https://gist.github.com/nokusukun/cf02d84f42965189fc9b1186f32f87e5")
regu.run()