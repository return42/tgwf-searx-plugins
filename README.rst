.. SPDX-License-Identifier: AGPL-3.0-or-later

==============================
Only show green hosted results
==============================

A `SearXNG plugin <https://docs.searxng.org/dev/plugins.html>`__ to check if a
domain is part of the `Green WEB <https://www.thegreenwebfoundation.org/>`__.

Installation
============

**USE WITH CARE**

Its recommended to install (and regularly update) `The Green Domains dataset
<https://github.com/thegreenwebfoundation/admin-portal/blob/master/docs/working-with-greenweb-datasets.md>`__
otherwise the plugin uses the API what sends a lot of requests from the SearXNG
instance to the Green WEB foundation and slows down the SearXNG instance
massively.

Change to the environment in which the plugin is to be installed::

     $ sudo utils/searxng.sh instance cmd python -m \
         pip install git+https://github.com/return42/tgwf-searx-plugins


Development
===========

This project is managed by `hatch <https://hatch.pypa.io>`_, for development
tasks you should install ``hatch``:

.. code:: sh

    $ pipx install hatch

Format and *lint* your code before commit:

.. code:: sh

    $ hatch run fix
    $ hatch run check

To enter the development environment use ``shell``:

.. code:: sh

   $ hatch shell

To get a developer installation in a SearXNG developer environment:

.. code:: sh

   $ git clone git@github.com:return42/tgwf-searx-plugins.git
   $ ./manage pyenv.cmd python -m \
         pip install -e tgwf-searx-plugins

To register the plugin in SearXNG add ``only_show_green_results.SXNGPlugin`` to
the ``plugins:``:

.. code:: yaml

    plugins:
      # ...
      only_show_green_results.SXNGPlugin:
        active: false
