from lib2to3.pgen2 import token
import re, asyncio, random
from aiohttp import content_disposition_filename
from discord.ext import commands
from discord.ext import tasks

channel_id = 904610663614255114
token = 'ODcyMTIzNjI4MjU3NDI3NTM3.YibQLA.T88U5C-7h-3uCIWd-gmt4-Q7DaY'
spam_id = 
starboard_id = 904610636070277140

with open('data/pokemon.txt', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary.txt','r') as file:
    legendary_list = file.read()
with open('data/mythical.txt','r') as file:
    mythical_list = file.read()
with open('data/level.txt','r') as file:
    to_level = file.readline()
with open('data/ultra beast.txt','r',) as file:
    ultrabeast_list = file.read()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0
ultrabeast = 0

owner_ping = '<@872123628257427537>'
poketwo = 716390085896962058
bot = commands.Bot(command_prefix="!")
intervals = [2.5, 3, 3.1, 3.2, 3.3, 3.5]
poketwo_prefix = '.'

def solve(message):
    hint = []
    for i in range(15,len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^'+hint_replaced+'$', pokemon_list, re.MULTILINE)
    return solution

@tasks.loop(seconds=random.choice(intervals))
async def spam():
    spam = bot.get_channel(int(spam_id))
    await spam.send(f'{random.randint(1, 100000000000)}')
    
@spam.before_loop
async def before_spam():
    await bot.wait_until_ready()
spam.start()

@bot.event
async def on_ready():
    print(f'Logged into account: {bot.user.name}')

@bot.event
async def on_message(message):
    star = bot.get_channel(int(starboard_id))
    channel = bot.get_channel(int(channel_id))
    if message.channel.id == int(channel_id):
        if message.author.id == poketwo:
            if message.embeds:
                embed_title = message.embeds[0].title
                if 'wild pokémon has appeared!' in embed_title:
                    spam.cancel()
                    await asyncio.sleep(1.5)
                    await channel.send(f'{poketwo_prefix}h')
                elif "Congratulations" in embed_title:
                    embed_content = message.embeds[0].description
                    if 'now level' in embed_content:
                        spam.cancel()
                        split = embed_content.split(' ')
                        a = embed_content.count(' ')
                        level = int(split[a].replace('!', ''))
                        if level == 100:
                            await channel.send(f"{poketwo_prefix}s {to_level}")
                            with open('data/level.txt', 'r') as fi:
                                data = fi.read().splitlines(True)
                            with open('data/level.txt', 'w') as fo:
                                fo.writelines(data[1:])
                            spam.start()
                        else:
                            spam.start()
            else:
                content = message.content
                if 'The pokémon is ' in content:
                    if not len(solve(content)):
                        print('Pokemon not found.')
                    else:
                        for i in solve(content):
                            await asyncio.sleep(0.5)
                            await channel.send(f'{poketwo_prefix}c {i}')
                    spam.start()
                elif 'Congratulations' in content:
                    global shiny
                    global legendary
                    global num_pokemon
                    global mythical
                    global ultrabeast
                    num_pokemon += 1
                    split = content.split(' ')
                    pokemon = split[7].replace('!','')
                    if 'These colors seem unusual...' in content:
                        shiny += 1
                        print(f'A shiny Pokémon was caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny}| Ultra Beast: {ultrabeast} | Legendary: {legendary} | Mythical: {mythical}')
                        await star.send(f'A shiny :sparkles: {pokemon} was caught')
                    elif re.findall('^'+pokemon+'$', legendary_list, re.MULTILINE):
                        legendary += 1
                        print(f'A legendary Pokémon was caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Ultra Beast: {ultrabeast} | Legendary: {legendary} | Mythical: {mythical}')
                        await star.send(f'{pokemon}: was caught')   
                    elif re.findall('^'+pokemon+'$', mythical_list, re.MULTILINE):
                        mythical += 1
                        print(f'A mythical Pokémon was caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Ultra Beast: {ultrabeast} | Legendary: {legendary} | Mythical: {mythical}')
                        await star.send(f'{pokemon}: was caught') 
                    elif re.findall('^'+pokemon+'$', ultrabeast_list, re.MULTILINE):
                        ultrabeast += 1
                        print(f'A ultra Pokémon was caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Ultra Beast: {ultrabeast} | Legendary: {legendary} | Mythical: {mythical}')
                        await star.send(f'{pokemon}: was caught')   
                    else:
                        print(f'Total Pokémon Caught: {num_pokemon}')  
                elif 'human' in content:
                    await channel.send(f'{owner_ping} Captcha detected! Solve it for me and send hint when youre done')
                    spam.cancel()
                    print('Captcha detected; autocatcher paused.  Verify the captcha and help the bot restart by sending a hint.')
                    #input()
                    await asyncio.sleep(2)
                    await channel.send(f'{poketwo_prefix}h')
    if not message.author.bot:
        await bot.process_commands(message)       
    if message.channel.id == int(channel_id):
        if message.author.id == poketwo:
            if 'These colors seem unusual...' in message.content:
                await message.add_reaction('\U00002B50')
                await channel.send('NICE')
            elif 'The pokémon is' in message.content:
                await asyncio.sleep(0.8)
                await message.delete()
        if 'Hello' in message.content:
                await message.add_reaction('\U0001F60E')
                await channel.send('Im here')
        if 'Nice Bot' in message.content:
            await channel.send('Thank you :) ')
        if message.author == bot.user:                 
            if f'{poketwo_prefix}h' in message.content:
                await message.delete()
            elif f'{poketwo_prefix}c' in message.content:
                await message.delete()
                
@bot.command()
async def bal(ctx):
    print('sent bal')
    await asyncio.sleep(1)
    await ctx.send(f'{poketwo_prefix}bal')

@bot.command()
async def catchrate(ctx):
    print('sent catch rate')
    await asyncio.sleep(1)
    await ctx.send(f'the catch rate is depend on your spawns time ')

@bot.command()
async def total(ctx):
    print('sent total')
    await asyncio.sleep(1)
    await ctx.send(f'Total caught: {num_pokemon}')

@bot.command()
async def rarecaught(ctx):
    print('sent rare caught')
    await asyncio.sleep(1)
    await ctx.send(f'Shiny: {shiny} | Ultra Beast: {ultrabeast} | Legendary: {legendary} | Mythical: {mythical}') 

@bot.command()
async def quest(ctx):
    print('sent quest')
    await asyncio.sleep(1)
    await ctx.send(f'{poketwo_prefix}q')

@bot.command()
async def startrading(ctx):
    print('TRADING!')
    await ctx.send(f'{poketwo_prefix}t {owner_ping}')

@bot.command()
async def control(ctx, *,args ):
    print('CONTROLLING THE BOT FROM DISTANCES')
    await ctx.send( args )

@bot.command()
async def commands(ctx):
    print('SENT HELP LIST')
    await ctx.send(':stars:``` Hello ``` [check if the bot alive in catching channel]  \n:desktop:Commands list: ```\n              !bal \n              !total \n              !rarecaught \n              !quest \n              !startrading ```\n :video_game:Control args command: ```!control (args)``` \n          [ Ex: ```!control .t x ]```')

print(f'Pokétwo Autocatcher \nCode by Harry\nEvent Log:')
bot.run(f"{token}")
