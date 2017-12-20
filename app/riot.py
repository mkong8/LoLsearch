"""Return json with game info."""
import requests
import json
from datetime import datetime, timedelta
import pprint
import discord

import config
from config import API_KEY, RIOT


def get_summoner_info(ign):
    """Summoner id needed for spectator API."""
    searchname = ign.strip().replace(' ', '').lower()
    summoner_endpoint = '{}/lol/summoner/v3/summoners/by-name/' \
                        '{}?api_key={}'.format(RIOT, searchname, API_KEY)
    summoner_info = requests.get(summoner_endpoint).json()
    # print(info)
    return summoner_info


def get_game_info(ign):
    """In game info from spectator endpoint."""
    summoner_id = get_summoner_info(ign)['id']
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


def get_history(ign):
    account_id = get_summoner_info(ign)['accountId']
    history_endpoint = '{}/lol/match/v3/matchlists/by-account/' \
                       '{}/recent?api_key={}'.format(RIOT, account_id, API_KEY)
    history_info = requests.get(history_endpoint).json()
    return history_info


def get_match_info(match_id):
    match_endpoint = '{}/lol/match/v3/matches/' \
                       '{}?api_key={}'.format(RIOT, match_id, API_KEY)
    match_info = requests.get(match_endpoint).json()
    return match_info


def get_rank_output(ign):
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
        output += " {} TEAM\n".format(team.upper())
        output += ' ' + '-'*32 + '\n'
        for player in players[team]:
            curr_player = ' '
            line_length = 20 - len(player)
            blank_buffer = ' '*line_length
            if player.lower() == ign.lower():
                curr_player = '*'
            output += '{}{}{}{} {}\n'.format(curr_player, player, blank_buffer,
                                           players[team][player][0],
                                           players[team][player][1])
        output += '\n'
    minutes, seconds = divmod(game_length, 60)
    output += ' Game Time: %02d:%02d' % (minutes, seconds)
    return output + '```'


def get_history_output(ign):
    champion_index = json.loads(open('var/champions.json').read())['data']
    matchlist = get_history(ign)['matches'][0:10]
    output = '```CHAMPION  SCORE     CS      WIN/LOSS\n'
    output += '-'*30 + '\n'
    for match in matchlist:
        line_length = 10
        champion_id = int(match['champion'])
        for champion in champion_index:
            if int(champion_index[champion]['key']) == champion_id:
                # print(champion_index[champion]['name'])
                output += champion
                space_buffer = line_length - len(champion)
                output += ' '*space_buffer
        match_info = get_match_info(match['gameId'])
        for participant in match_info['participants']:
            if int(participant['championId']) == champion_id:
                win = participant['stats']['win']
                kills = participant['stats']['kills']
                deaths = participant['stats']['deaths']
                assists = participant['stats']['assists']
                creepscore = participant['stats']['totalMinionsKilled'] \
                             + participant['stats']['neutralMinionsKilled']
                space_buffer = line_length - len(str(kills))\
                                - len(str(deaths)) - len(str(assists)) - 2
                output += "{}/{}/{}{}".format(kills,
                                              deaths,
                                              assists,
                                              ' '*space_buffer)
                space_buffer = line_length - len(str(creepscore))
                output += "{}{}".format(creepscore, ' '*space_buffer)
                if win:
                    output += 'WIN\n'
                else:
                    output += 'LOSS\n'
    return output + '```'
