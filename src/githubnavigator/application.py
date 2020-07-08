"""Application module."""

from aiohttp import web
import jinja2
from dependency_injector import containers, providers

from . import domainmodel, website


class Application(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()

    # Domain model

    github_search = providers.Factory(
        domainmodel.search.GithubSearch,
        auth_token=config.github.auth_token,
        request_timeout=config.github.request_timeout,
    )

    # Website

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
        website.handlers.navigator,
        template_env=template_env,
        github_search=github_search,
        default_search_term=config.search.default_term,
        default_search_limit=config.search.default_limit,
    )

    website_app = providers.Factory(
        website.app.create_webapp,
        routes=providers.List(
            providers.Factory(web.get, '/', navigator_handler.provider),
        ),
    )

    run_website = providers.Callable(
        web.run_app,
        app=website_app,
        port=config.webapp.port,
        host=config.webapp.host,
    )
