GitHub Navigator
================

GitHub Navigator is an example
`Dependency Injector <https://github.com/ets-labs/python-dependency-injector>`_ web application.

Powered By:

- `Python 3.8 <https://www.python.org/>`_
- `Dependency Injector <https://github.com/ets-labs/python-dependency-injector>`_
- `Aiohttp <https://github.com/aio-libs/aiohttp>`_
- `GitHub <https://github.com/>`_ and its awesome `API <https://developer.github.com/v3/>`_
- `Docker <https://www.docker.com/>`_ + `Docker-compose <https://docs.docker.com/compose/>`_

How to run?
-----------

.. code-block:: bash

    docker-compose up

.. note::

   Github has a rate limit. For unauthenticated requests, the rate limit allows for up to 60
   requests per hour. To extend the limit to 5000 requests per hour you need to set personal
   access token.

   It's easy.

   - Follow this `guide <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_ to create a token.
   - Set a token to the ``.env`` file:

   .. code-block:: bash

      GITHUB_TOKEN=<your token>
