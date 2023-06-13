.. SPDX-License-Identifier: AGPL-3.0-or-later

==============================
Only show green hosted results
==============================

A `SearXNG plugin <https://docs.searxng.org/dev/plugins.html>`__ to check if a
domain is part of the `Green WEB <https://www.thegreenwebfoundation.org/>`__.

Its recommended to install (and regularly update) `The Green Domains dataset
<https://github.com/thegreenwebfoundation/admin-portal/blob/master/docs/working-with-greenweb-datasets.md>`__
otherwise the plugin uses the API what sends a lot of requests from the SearXNG
instance to the Green WEB foundation and slows down the SearXNG instance
massively.
