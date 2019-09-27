import random
import discord
import urllib.request
from urllib.request import Request, urlopen
from PIL import Image
#project files
from pokedex import Pokedex

#constants
NUM = 0
NAME = 1
TYPE = 2
TOTAL = 3
HP = 4
ATTACK = 5
DEFENSE = 6
SPATCK = 7
SPDEF = 8
SPEED = 9



client = discord.Client()
TOKEN = "" #must put in your own token!
pokedex = Pokedex()



#run the discored bot
def run():
    client.run(TOKEN)



#display a message when ready
@client.event
async def on_ready():
    print("Bot ready!")
    await client.change_presence(activity=discord.Game(name="Pokemon Red"))



#send a message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Who's That Pokemon?":
        #get the index of the pokemon we want
        index = random.randint(0, 925)
        msg = getPokemon(index)
        
        #send the pokemon
        channel = message.channel
        await sendIcon(index, message)
        await channel.send(msg)



# Integer, Message -> void
#send image
async def sendIcon(index, message):
    request = Request(pokedex.images[index], headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request)
    
    image = Image.open(response).convert('RGB')
    image.save('img.jpg')

    await message.channel.send(file=discord.File('img.jpg')) 

#Integer -> String
#get a random pokemon  
def getPokemon(index):
      
    headers = pokedex.headers

    pokeNum = pokedex.info[NUM][index]
    pokeName = pokedex.info[NAME][index]
    pokeType = pokedex.info[TYPE][index]
    pokeTotal = pokedex.info[TOTAL][index]
    pokeHP = pokedex.info[HP][index]
    pokeAtt = pokedex.info[ATTACK][index]
    pokeDef = pokedex.info[DEFENSE][index]
    pokeSpAtk = pokedex.info[SPATCK][index]
    pokeSpDef = pokedex.info[SPDEF][index]
    pokeSpeed = pokedex.info[SPEED][index]
    
    msg = ""
    msg = msg + headers[NAME] + ": " + pokeName + "\n"
    msg = msg + headers[NUM] + ": " + pokeNum + "\n"
    msg = msg + headers[TYPE] + ": " + pokeType + "\n"
    msg = msg + headers[HP] + ": " + pokeHP + "\n"
    msg = msg + headers[ATTACK] + ": " + pokeAtt + "\n"
    msg = msg + headers[DEFENSE] + ": " + pokeDef + "\n"
    msg = msg + headers[SPATCK] + ": " + pokeSpAtk + "\n"
    msg = msg + headers[SPDEF] + ": " + pokeSpDef + "\n"
    msg = msg + headers[SPEED] + ": " + pokeSpeed + "\n"
    msg = msg + headers[TOTAL] + ": " + pokeTotal + "\n"

    return msg
