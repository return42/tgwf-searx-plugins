# SPDX-License-Identifier: AGPL-3.0-or-later
"""Example of a *custom* SearXNG plugin."""

import logging
import os
import sqlite3
from urllib.parse import urlparse

from searx import network

log = logging.getLogger(__name__)

ALLOW_API_CONNECTIONS = True
DB_NAME = "url2green.db"
API_SERVER = "https://api.thegreenwebfoundation.org"


class GreenCheck:
    """Implement methods to check if a domain is part of the Green WEB"""

    def __init__(self):
        self.db = True  # pylint: disable=invalid-name

        try:
            self.db = bool(os.stat(DB_NAME))
        except Exception:  # pylint: disable=broad-except
            self.db = False

        if self.db:
            log.debug(
                f"Database found at {DB_NAME}. Using it for lookups instead of the Greencheck API"
            )
            return

        log.warning(f"No database found at {DB_NAME}.")
        if ALLOW_API_CONNECTIONS:
            log.warning(
                f"Falling back to the (much slower) Greencheck API, "
                f"as 'ALLOW_API_CONNECTIONS' is set to {ALLOW_API_CONNECTIONS}."
            )
        else:
            log.debug(
                f"filtering inactive: no database found at {DB_NAME}"
                f" and 'ALLOW_API_CONNECTIONS={ALLOW_API_CONNECTIONS}'"
            )

    def check_url(self, url=None):
        """Check a url passed in, and return a true or false result, based on whether
        the domain is marked as a one running on green energy."""
        log.debug(url)

        parsed_domain = urlparse(url).hostname
        ret_val = False

        if parsed_domain:
            log.debug(f"Checking {parsed_domain}, parsed from {url}")
            if self.db:
                ret_val = self.check_in_db(parsed_domain)
            elif ALLOW_API_CONNECTIONS:
                ret_val = self.check_against_api(parsed_domain)

        return ret_val

    def check_in_db(self, domain=None):
        """Checks wether ``domain`` is in the green database

        We basically treat the the sqlite database like an immutable, read-only
        datastructure.  This allows multiple concurrent connections as no state
        is ever being changed - only read with SELECT

        - https://docs.python.org/3.8/library/sqlite3.html#//apple_ref/Function/sqlite3.connect
        - https://sqlite.org/lockingv3.html

        """
        with sqlite3.connect(
            f"file:{DB_NAME}?mode=ro", uri=True, check_same_thread=False
        ) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT green FROM green_presenting WHERE url=? LIMIT 1", [domain]
            )
            res = cur.fetchone()
            log.debug(res)
            return bool(res)

    def check_against_api(self, domain=None):
        """Checks ``domain`` against https://api.thegreenwebfoundation.org API"""
        api_url = f"{API_SERVER}/greencheck/{domain}"
        log.debug(api_url)
        response = network.get(api_url).json()
        return bool(response.get("green"))
