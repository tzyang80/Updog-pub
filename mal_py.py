"""
Haosen Li
This file contains The Mal_Py class.
"""
import requests
import json
import time
import re


class Mal_Py:
    """
    This class contains functions for accessing MAL API.
    """
    def __init__(self, file_dir, nsfw='false'):
        """
        Initializes a mal_py object from a file directory
        containing a .json file with the MAL API token information.
        """
        with open(file_dir, 'r') as f:
            self._token = json.load(f)
        self._headers = {'Authorization': f'Bearer '
                                          f'{self._token["access_token"]}'}
        self._nsfw = nsfw

    def search(self, s_type, query, limit, offset=0):
        """
        Takes in a str for anime or manga, a str name, an int
        return limit, and an optional offset(default=0).
        Returns a list of dictionary containing basic
        information on the anime/manga.
        """
        s_type = self._type_sort(s_type)
        url = f'https://api.myanimelist.net/v2/{s_type}?q={query}&' \
              f'limit={limit}&offset={str(offset)}&nsfw={self._nsfw}'
        return self._format_dict(self._get_response(url))

    def details(self, s_type, s_id):
        """
        Takes in a str for anime or manga, and an anime/manga id.
        Returns a dictionary containing the details of the
        anime/manga from the given id.
        """
        s_type = self._type_sort(s_type)
        base_url = f'https://myanimelist.net/{s_type}/'
        url = f'https://api.myanimelist.net/v2/{s_type}/{str(s_id)}?' \
              f'fields=title,main_picture,synopsis,mean,rank,' \
              f'popularity,media_type,status,genres,' \
              f'num_episodes,start_season,rating,studios'

        info = self._get_response(url)
        info['mal_url'] = base_url + str(info['id'])
        return info

    def ranking(self, s_type, ranking_type, limit=10):
        """
        Takes in a str for anime or manga, a str ranking type,
        and an optional int limit. Returns a list of dictionary
        containing the ranked list of anime/manga.

        ===== Possible Ranking Types =====

        Anime:
        "all", "airing", "upcoming", "tv", "ova", "movie",
        "special", "bypopularity", "favorite"

        Manga:
        "all", "manga", "oneshots", "doujin", "lightnovels",
        "novels", "manwha", "manhua", "bypopularity", "favorite"
        """
        s_type = self._type_sort(s_type)
        url = f'https://api.myanimelist.net/v2/{s_type}/ranking?' \
              f'ranking_type={ranking_type}&limit={str(limit)}&nsfw={self._nsfw}'
        return self._format_dict(self._get_response(url))

    def seasonal_anime(self, season=None, year=None,
                       sort_by='score', offset=0, limit=10):
        """
        Takes in an str season/month(default=current), an int
        year(default=current), a sorting method(default="score"),
        an offset(default=0), and an int limit(default=10).
        Returns a list of dictionaries containing the anime info.
        """
        if sort_by == 'users':
            sort_by = 'anime_num_list_users'
        else:
            sort_by = 'anime_score'

        if season is None and year is None:
            season, year = self._get_time()
        season = self._season_sort(season)
        url = f'https://api.myanimelist.net/v2/anime/season/' \
              f'{str(year)}/{season}?limit={str(limit)}&' \
              f'offset={str(offset)}&sort={sort_by}&nsfw={self._nsfw}'

        return self._format_dict(self._get_response(url))

    def set_nsfw(self, set_nsfw):
        """
        Takes in a str "true" or "false". Sets the nsfw settings.
        """
        self._nsfw = set_nsfw

    def user_list(self, s_type, username, status='all',
                  sort_by='list_score', limit=5, offset=0):
        """
        Takes in a str for anime or manga, a str MAL username,
        a str status(default="all"), a str sorting method(default="list_score")
        an int limit(default=5), and an int offset(default=0). Returns a list of
        dictionary containing the anime/manga info. Returns an empty
        list if there are no results.
        """
        if status != 'all':
            status = f'={status}'
        else:
            status = ''
        s_type = self._type_sort(s_type)
        url = f'https://api.myanimelist.net/v2/users/{username}/' \
              f'{s_type}list?fields=list_status&status{status}&' \
              f'sort={sort_by  }&limit={str(limit)}&offset={str(offset)}'
        return self._format_dict(self._get_response(url))

    def get_user_url(self, username, status=7, order=4, order2=0):
        """
        Takes in a str MAL username, optional ints for status, order,
        and order2. Returns a str url for the given user. Defaults to
        all anime, sorted by score.
        """
        url = f'https://myanimelist.net/animelist/{username}?' \
              f'status={str(status)}&order={str(order)}&order2={str(order2)}'
        return url

    def get_user_url_help(self):
        """
        Prints out a help message for get_user_url.
        """
        print('Here are the known responses...')
        print()
        print('status int values:')
        print('1 is currently watching')
        print('2 is completed')
        print('3 is on hold')
        print('4 is dropped')
        print('5 is none')
        print('6 is plan to watch')
        print('7 is all anime')
        print()
        print('order int values:')
        print('1 is title(asc)')
        print('2 is finish date(desc)')
        print('3 is start date(desc)')
        print('4 is score(desc)')
        print('5 is last updated(desc)')
        print('6 is type(asc)')
        print('...')
        print()
        print('order2 int values:')
        print('0 is none')
        print('1 is title(asc)')
        print('2 is finish date(desc)')
        print('3 is start date(desc)')
        print('4 is none')
        print('5 is last updated(desc)')
        print('6 is type(asc)')
        print('...')

    def _get_response(self, url):
        """
        Takes in a str url.
        Returns the response as a dictionary.
        """
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def _format_dict(self, data):
        """
        Takes in a dictionary returned by the MAL API.
        Returns a list of dictionaries.
        """
        result = []
        nodes = data['data']
        for node in nodes:
            result.append(node['node'])
        return result

    def _get_time(self):
        """
        Returns a tuple of month and year.
        """
        date = time.ctime(time.time()).split()
        return date[1], date[-1]

    def _season_sort(self, season):
        """
        Takes in a str for season/month.
        Returns the proper str used in the url.
        """
        season = re.sub(r'\W+', '', season.lower())
        seasons = {'winter': {'winter', 'win', 'wi', 'january', 'jan',
                              'february', 'feb', 'march', 'mar',},
                   'spring': {'spring', 'spr', 'sp', 'april', 'apr',
                              'may', 'june', 'jun'},
                   'summer': {'summer', 'sum', 'su', 'july', 'jul',
                              'august', 'aug', 'september', 'sep'},
                   'fall': {'fall', 'fal', 'fa', 'october', 'oct',
                            'november', 'nov', 'december', 'dec'}}
        for name, abbrev in seasons.items():
            if season in abbrev:
                return name

    def _type_sort(self, s_type):
        """
        Takes in a str for anime or manga.
        Returns the proper str used in the url.
        """
        s_type = re.sub(r'\W+', '', s_type.lower())
        if s_type.startswith('a'):
            return 'anime'
        elif s_type.startswith('m'):
            return 'manga'
        return None