# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Searx plugins from The Green Web Foundation

tgwf-searx-plugins
  All results of searx queries that not hosted on a green infrastructure are
  filtered

"""

from setuptools import setup

GIT_URL='https://github.com/return42/tgwf-searx-plugins'

setup(
    name                = 'tgwf-searx-plugins'
    , version           = '0.3'
    , description       = 'The Green Web Foundation searx plugins'
    , long_description  = __doc__
    , url               =  GIT_URL
    , author            = 'The Green Web Foundation'
    , author_email      = 'chris@productscience.co.uk'
    , project_urls      = {
        "Code"              : GIT_URL
        , "Issue tracker"   : GIT_URL + "/issues"
    }
    , license           = 'GNU Affero General Public License'
    , zip_safe          = False
    , py_modules        = [
        'only_show_green_results'
    ]
    , entry_points      = {
        'searxng.plugins' : [
            'tgwf.green-results = only_show_green_results'
        ]
    }
)
