"""Website application module."""

from typing import List

from aiohttp import web


def create_app(routes: List[web.RouteDef]) -> web.Application:
    """Create web application."""
    app = web.Application()
    app.add_routes(routes)
    return app
