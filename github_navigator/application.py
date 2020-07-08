"""Github Navigator application container."""

from aiohttp import web
import jinja2
from dependency_injector import containers, providers

from . import search, webhandlers, webapp


class GithubNavigator(containers.DeclarativeContainer):
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
        loader=template_loader,
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        enable_async=True,
    )

    navigator_webhandler = providers.Coroutine(
        webhandlers.navigator,
        template_env=template_env,
        github_search=github_search,
    )

    webapp = providers.Factory(
        webapp.create_webapp,
        routes=providers.List(
            providers.Factory(web.get, '/navigator', navigator_webhandler.provider),
        ),
    )

    run_webapp = providers.Callable(
        web.run_app,
        app=webapp,
        port=config.webapp.port,
        host=config.webapp.host,
    )
