"""Return json with game info."""
import requests
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

# pp = pprint.PrettyPrinter()
# pp.pprint(get_game_info('so pogo'))


def get_output(ign):
    info = get_game_info(ign)

    if 'status' in info:
        return "{} is not currently in a game.".format(ign)