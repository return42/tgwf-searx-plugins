# SPDX-License-Identifier: AGPL-3.0-or-later
"""Only show green hosted results"""

import os
import logging
import sqlite3
import requests

from flask_babel import gettext

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

logger = logging.getLogger(__name__)

name = gettext('Only show green hosted results')
description = gettext('Any results not being hosted on green infrastructure will be filtered')
default_on = False
preference_section = 'general'
allow_api_connections = True
database_name = "url2green.db"
api_server = "https://api.thegreenwebfoundation.org"


class GreenCheck:
    """Implement methods to check if a domain is part of the Green WEB"""

    def __init__(self):
        self.db = True  # pylint: disable=invalid-name

        try:
            self.db = bool(os.stat(database_name))
        except Exception:  # pylint: disable=broad-except
            self.db = False

        if self.db:
            logger.debug(
                "Database found at %s. Using it for lookups instead of the Greencheck API",
                database_name)
            return

        logger.debug("No database found at %s.", database_name)
        if allow_api_connections:
            logger.debug(
                "Falling back to the the Greencheck API, as 'allow_api_connections' is set to %s.",
                allow_api_connections)
        else:
            logger.debug(
                "filtering inactive: no database found at %s and 'allow_api_connections=%s'",
                database_name, allow_api_connections)

    def check_url(self, url=None):
        """Check a url passed in, and return a true or false result, based on whether
        the domain is marked as a one running on green energy."""
        logger.debug(url)

        parsed_domain = urlparse(url).hostname
        ret_val = False

        if parsed_domain:
            logger.debug("Checking %s, parsed from %s", parsed_domain, url)
            if self.db:
                ret_val = self.check_in_db(parsed_domain)
            elif allow_api_connections:
                ret_val = self.check_against_api(parsed_domain)

        return ret_val

    def check_in_db(self, domain=None):  # pylint: disable=no-self-use
        """Checks wether ``domain`` is in the green database

        We basically treat the the sqlite database like an immutable, read-only
        datastructure.  This allows multiple concurrent connections as no state
        is ever being changed - only read with SELECT

        - https://docs.python.org/3.8/library/sqlite3.html#//apple_ref/Function/sqlite3.connect
        - https://sqlite.org/lockingv3.html

        """
        with sqlite3.connect(
                "file:{}?mode=ro".format(database_name),
                uri=True,
                check_same_thread=False
        ) as con:
            cur = con.cursor()
            cur.execute("SELECT green FROM green_presenting WHERE url=? LIMIT 1",
                        [domain])
            res = cur.fetchone()
            logger.debug(res)
            return bool(res)

    def check_against_api(self, domain=None):  # pylint: disable=no-self-use
        """Checks ``domain`` against https://api.thegreenwebfoundation.org API"""
        api_url = "{}/greencheck/{}".format(api_server, domain)
        logger.debug(api_url)
        response = requests.get(api_url).json()
        return bool(response.get("green"))

GC = GreenCheck()

def post_search(request, search):  # pylint: disable=unused-argument
    """Filter searx results."""

    # pylint: disable=protected-access
    green_results = [
        result for result in list(search.result_container._merged_results)
        if GC.check_url(result.get('url'))
    ]
    search.result_container._merged_results = green_results
