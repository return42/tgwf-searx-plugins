# SPDX-License-Identifier: AGPL-3.0-or-later
"""Only show green hosted results.  Example of a *custom*
SearXNG plugin."""

from __future__ import annotations

import typing

from flask_babel import gettext
from searx.extended_types import SXNG_Request
from searx.plugins import Plugin, PluginInfo
from searx.result_types import Result

from .greencheck import GreenCheck

if typing.TYPE_CHECKING:
    from searx.plugins import PluginCfg
    from searx.search import SearchWithPlugins


__version__ = "0.5.0"

GC = GreenCheck()


class SXNGPlugin(Plugin):
    """Plugin converts strings to different hash digests.  The results are
    displayed in area for the "answers".
    """

    id = "only_show_green_results"

    def __init__(self, plg_cfg: "PluginCfg") -> None:
        super().__init__(plg_cfg)

        self.info = PluginInfo(
            id=self.id,
            name=gettext("Only show green hosted results"),
            description=gettext(
                "Any results not being hosted on green infrastructure will be filtered"
            ),
            preference_section="general",
        )

    def on_result(
        # pylint: disable=unused-argument
        self,
        request: SXNG_Request,
        search: "SearchWithPlugins",
        result: Result,
    ) -> bool:
        """Return a true or false value, based on whether the domain is marked
        as a one running on green energy.
        """
        if not result.url:
            return True
        return GC.check_url(result.url)
