"""Application module."""

from aiohttp import web
import jinja2
from dependency_injector import containers, providers

from . import search, handlers, webapp


class Application(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()

    github_search = providers.Factory(
        search.GithubSearch,
        auth_token=config.github.auth_token,
        request_timeout=config.github.request_timeout,
    )

    template_loader = providers.Factory(
        jinja2.FileSystemLoader,
        searchpath=config.webapp.templates_dir,
    )

    template_env = providers.Singleton(
        jinja2.Environment,
        loader=providers.Factory(
            jinja2.FileSystemLoader,
            searchpath=config.webapp.templates_dir,
        ),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        enable_async=True,
    )

    navigator_handler = providers.Coroutine(
        handlers.navigator,
        template_env=template_env,
        github_search=github_search,
        default_search_term=config.search.default_term,
        default_search_limit=config.search.default_limit,
    )

    web_app = providers.Factory(
        webapp.create_app,
        routes=providers.List(
            providers.Factory(web.get, '/', navigator_handler.provider),
        ),
    )

    run = providers.Callable(
        web.run_app,
        app=web_app,
        port=config.webapp.port,
        host=config.webapp.host,
    )
