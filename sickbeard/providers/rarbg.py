# coding=utf-8
# Author: Dustyn Gibson <miigotu@gmail.com>
#
# This file is part of Medusa.
#
# Medusa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Medusa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Medusa. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import traceback
import datetime
import time

from sickbeard import logger, tvcache
from sickbeard.indexers.indexer_config import INDEXER_TVDB

from sickrage.helper.common import convert_size, try_int
from sickrage.providers.torrent.TorrentProvider import TorrentProvider


class RarbgProvider(TorrentProvider):  # pylint: disable=too-many-instance-attributes

    def __init__(self):

        # Provider Init
        TorrentProvider.__init__(self, 'Rarbg')

        # Credentials
        self.public = True
        self.token = None
        self.token_expires = None

        # URLs
        self.url = 'https://rarbg.com'  # Spec: https://torrentapi.org/apidocs_v2.txt
        self.urls = {
            'api': 'http://torrentapi.org/pubapi_v2.php',
        }

        # Proper Strings
        self.proper_strings = ['{{PROPER|REPACK}}']

        # Miscellaneous Options
        self.ranked = None
        self.sorting = None

        # Torrent Stats
        self.minseed = None
        self.minleech = None

        # Cache
        self.cache = tvcache.TVCache(self, min_time=10)  # only poll RARBG every 10 minutes max

    def search(self, search_strings, age=0, ep_obj=None):  # pylint: disable=too-many-branches, too-many-locals, too-many-statements
        """
        RARBG search and parsing

        :param search_string: A dict with mode (key) and the search value (value)
        :param age: Not used
        :param ep_obj: Not used
        :returns: A list of search results (structure)
        """
        results = []
        if not self.login():
            return results

        # Search Params
        search_params = {
            'app_id': 'sickrage2',
            'category': 'tv',
            'min_seeders': try_int(self.minseed),
            'min_leechers': try_int(self.minleech),
            'limit': 100,
            'format': 'json_extended',
            'ranked': try_int(self.ranked),
            'token': self.token,
        }

        if ep_obj is not None:
            ep_indexerid = ep_obj.show.indexerid
            ep_indexer = ep_obj.show.indexer
        else:
            ep_indexerid = None
            ep_indexer = None

        for mode in search_strings:
            items = []
            logger.log('Search mode: {0}'.format(mode), logger.DEBUG)

            if mode == 'RSS':
                search_params['sort'] = 'last'
                search_params['mode'] = 'list'
                search_params.pop('search_string', None)
                search_params.pop('search_tvdb', None)
            else:
                search_params['sort'] = self.sorting if self.sorting else 'seeders'
                search_params['mode'] = 'search'

                if ep_indexer == INDEXER_TVDB and ep_indexerid:
                    search_params['search_tvdb'] = ep_indexerid
                else:
                    search_params.pop('search_tvdb', None)

            for search_string in search_strings[mode]:

                if mode != 'RSS':
                    search_params['search_string'] = search_string
                    logger.log('Search string: {0}'.format(search_string),
                               logger.DEBUG)

                # Check if token is still valid before search
                if not self.login():
                    continue

                # Maximum requests allowed are 1req/2sec
                # Changing to 5 because of server clock desync
                time.sleep(5)

                data = self.get_url(self.urls['api'], params=search_params, returns='json')
                if not isinstance(data, dict):
                    logger.log('No data returned from provider', logger.DEBUG)
                    continue

                error = data.get('error')
                error_code = data.get('error_code')
                # Don't log when {'error':'No results found','error_code':20}
                # List of errors: https://github.com/rarbg/torrentapi/issues/1#issuecomment-114763312
                if error:
                    if error_code == 5:
                        # 5 = Too many requests per second
                        logger.log('{0}. Error code: {1}'.format(error, error_code), logger.INFO)
                    elif error_code not in (14, 20):
                        # 14 = Cant find thetvdb in database. Are you sure this thetvdb exists?
                        # 20 = No results found
                        logger.log('{0}. Error code: {1}'.format(error, error_code), logger.WARNING)
                    continue

                torrent_results = data.get('torrent_results')
                if not torrent_results:
                    logger.log('Data returned from provider does not contain any torrents', logger.DEBUG)
                    continue

                for item in torrent_results:
                    try:
                        title = item.pop('title')
                        download_url = item.pop('download')
                        if not all([title, download_url]):
                            continue

                        seeders = item.pop('seeders')
                        leechers = item.pop('leechers')

                        # Filter unseeded torrent
                        if seeders < min(self.minseed, 1):
                            if mode != 'RSS':
                                logger.log("Discarding torrent because it doesn't meet the "
                                           " minimum seeders: {0}. Seeders: {1}".format
                                           (title, seeders), logger.DEBUG)
                            continue

                        torrent_size = item.pop('size', -1)
                        size = convert_size(torrent_size) or -1

                        item = {
                            'title': title,
                            'link': download_url,
                            'size': size,
                            'seeders': seeders,
                            'leechers': leechers,
                            'pubdate': None,
                            'hash': None
                        }
                        if mode != 'RSS':
                            logger.log('Found result: {0} with {1} seeders and {2} leechers'.format
                                       (title, seeders, leechers), logger.DEBUG)

                        items.append(item)
                    except (AttributeError, TypeError, KeyError, ValueError, IndexError):
                        logger.log('Failed parsing provider. Traceback: {0!r}'.format
                                   (traceback.format_exc()), logger.ERROR)
                        continue

            results += items

        return results

    def login(self):
        if self.token and self.token_expires and datetime.datetime.now() < self.token_expires:
            return True

        login_params = {
            'get_token': 'get_token',
            'format': 'json',
            'app_id': 'sickrage2',
        }

        response = self.get_url(self.urls['api'], params=login_params, returns='json')
        if not response:
            logger.log('Unable to connect to provider', logger.WARNING)
            return False

        self.token = response.get('token')
        self.token_expires = datetime.datetime.now() + datetime.timedelta(minutes=14) if self.token else None
        return self.token is not None


provider = RarbgProvider()
