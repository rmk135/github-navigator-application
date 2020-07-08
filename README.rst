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

Setup
-----

.. code-block:: bash

    pip install -r requirements.txt
    cp ./config.yml-sample ./config.yml

Insert your GitHub auth token to `config.yml`.

Run
---
.. code-block:: bash

    python -m githubnavigator
    open http://127.0.0.1:8080/
