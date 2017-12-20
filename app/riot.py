"""Return json with game info."""
import requests
from datetime import datetime, timedelta
import pprint

import config
from config import API_KEY, RIOT


def get_summoner_id(ign):
    """Summoner id needed for spectator API."""
    searchname = ign.strip().replace(' ', '').lower()
    summoner_endpoint = '{}/lol/summoner/v3/summoners/by-name/' \
                        '{}?api_key={}'.format(RIOT, searchname, API_KEY)
    summoner_info = requests.get(summoner_endpoint).json()
    # print(info)
    return summoner_info['id']


def get_game_info(ign):
    """In game info from spectator endpoint."""
    summoner_id = get_summoner_id(ign)
    spectator_endpoint = '{}/lol/spectator/v3/active-games/by-summoner/' \
                         '{}?api_key={}'.format(RIOT, summoner_id, API_KEY)
    game_info = requests.get(spectator_endpoint).json()
    return game_info


def get_rank(summoner_id):
    rank_endpoint = '{}/lol/league/v3/positions/by-summoner/' \
                    '{}?api_key={}'.format(RIOT, summoner_id, API_KEY)
    rank_info = requests.get(rank_endpoint).json()
    for rank_type in rank_info:
        if rank_type['queueType'] == 'RANKED_SOLO_5x5':
            return rank_type['tier'], rank_type['rank']



def get_output(ign):
    game_info = get_game_info(ign)

    if 'status' in game_info:
        return "{} is not currently in a game.".format(ign)

    players = {'blue': {}, 'red': {}}
    game_length = game_info['gameLength']

    for participant in game_info['participants']:
        tier, rank = get_rank(participant['summonerId'])
        name = participant['summonerName']
        if participant['teamId'] == 100:
            players['blue'][name] = (tier, rank)
        else:
            players['red'][name] = (tier, rank)

    # pp = pprint.PrettyPrinter()
    # pp.pprint(players)
    output = '```'
    for team in players:
        output += team.upper() + " TEAM\n"
        output += '-'*32 + '\n'
        for player in players[team]:
            line_length = 20 - len(player)
            print(line_length)
            blank_buffer = ' '*line_length
            output += '{}{}{} {}\n'.format(player, blank_buffer, 
                                           players[team][player][0],
                                           players[team][player][1])
        output += '\n'
    minutes, seconds = divmod(game_length, 60)
    output += 'Game Time: %02d:%02d' % (minutes, seconds)
    output += '```'
    return output

print(get_output('chapanya'))

