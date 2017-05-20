import requests
import ast

def get_request(url, keys):
	request = requests.get(url, params = keys)
	return request

# regex for valid summoner name: '^[0-9\\p{L} _\\.]+$'

#PROGRAM

key = 'RGAPI-3989dd96-5f18-464f-bf05-865ca78dd8ee'
keys = {'api_key': key}
url = 'https://na.api.pvp.net/'

summoner_name = input('Summoner Name: ')
summoner_name = summoner_name.replace(' ', '') #get rid of white space


region = 'na'
summoner_url = url + 'api/lol/na/v1.4/summoner/by-name/{name}'.format(name = summoner_name)

summoner_req = get_request(summoner_url, keys)
summoner_id = summoner_req.json()[summoner_name]['id']

game_url = url + 'observer-mode/rest/consumer/getSpectatorGameInfo/NA1/{id}'.format(id = summoner_id)
game_req = get_request(game_url, keys)

# print json to text
#f = open('ingame.txt', 'w')
#print(game_req.json(), file=f)

# gather all participating summoner names
names_list = []
id_list = []
rank_list = []
for i, summoner in enumerate(game_req.json()['participants']):
	names_list.append(summoner['summonerName'])
	id_list.append(summoner['summonerId'])
	rank_url = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/{id}'.format(id = summoner['summonerId'])
	rank_req = get_request(rank_url, keys)
	if not rank_req.json():
		rank_list.append('UNRANKED')
	else:
	    rank_list.append((str(rank_req.json()[0]['tier']), str(rank_req.json()[0]['rank'])))



print('__SUMMONER NAME__\t\t__RANK__')
#for name, rank in zip(names_list, rank_list):


	