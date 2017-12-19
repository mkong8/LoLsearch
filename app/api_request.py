import requests
import time
import discord
from discord.ext.commands import Bot
import sys
import re

def get_request(url, keys):
	request = requests.get(url, params = keys)
	return request

# regex for valid summoner name: '^[0-9\\p{L} _\\.]+$'

def get_ranks(orig_summoner_name):

	output = '```'

	
	keys = {'api_key': key}
	url = 'https://na.api.pvp.net/'

	summoner_name = orig_summoner_name.replace(' ', '').lower() #get rid of white space


	region = 'na'
	summoner_url = url + 'api/lol/na/v1.4/summoner/by-name/{name}'.format(name = summoner_name)

	summoner_req = get_request(summoner_url, keys)

	# check if summoner exists
	if 'status' in summoner_req.json():
		output += orig_summoner_name + ' is not an existing summoner.```'

	summoner_id = summoner_req.json()[summoner_name]['id']
	orig_summoner_name = summoner_req.json()[summoner_name]['name']

	game_url = url + 'observer-mode/rest/consumer/getSpectatorGameInfo/NA1/{id}'.format(id = summoner_id)
	game_req = get_request(game_url, keys)

	#check for 404 status if player is not in game
	if 'status' in game_req.json():
		output += orig_summoner_name + ' is not in a game.```'
		return output

	# 10 second interval from API calls
	future = time.time() + 10
	while True:
		if time.time() > future:
			break
	# print json to text
	#f = open('ingame.txt', 'w')
	#print(game_req.json(), file=f)

	# format the column width
	col_width = 19
	output += '___SUMMONER NAME___\t___RANK___\n'

	# gather all participating summoner names/ranks and output
	for i, summoner in enumerate(game_req.json()['participants']):
		if i == 5: output += '\n'
		output += '\n'
		if summoner['summonerId'] == summoner_id:
			output += '* '
			col_width -= 2 #adjust for '* '
		output += summoner['summonerName'].ljust(col_width) + '\t'
		col_width = 19 #adjust back to normal
		rank_url = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/{id}'.format(id = summoner['summonerId'])
		rank_req = get_request(rank_url, keys)
		if not rank_req.json():
			output += 'UNRANKED'
		else:
		    output += str(rank_req.json()[0]['tier']) + ' ' + str(rank_req.json()[0]['rank'])
		    if summoner['summonerId'] == summoner_id:
		    	output += ' *'

	output += '\n' + '_'*33

	return output + '```'


my_bot = Bot(command_prefix="!")

@my_bot.event
async def on_ready():
    print("Client ready to retrieve ranks")

@my_bot.command()
async def hello():
	return await my_bot.say('Hello World!')

@my_bot.command()
async def ranked(*, summoner_name: str):
	await my_bot.say("retrieving data...")
	output = get_ranks(summoner_name)
	return await my_bot.say(output)

@my_bot.command(pass_context = True)
async def clear(ctx, number):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) + 1 #Converting the amount of messages to delete to an integer
    async for x in my_bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await my_bot.delete_messages(mgs)

@my_bot.command()
async def matt():
    return await my_bot.say("What a monkey.")

@my_bot.command()
async def joey():
    return await my_bot.say("He did it.")

@my_bot.command()
async def felix():
    return await my_bot.say("~meow")

my_bot.run("MzE1OTI4MzU3NTA0MDI0NTc2.DAN2uQ.SLmnsOTQf2Bm760HS4DeQAybgF4")

