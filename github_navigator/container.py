"""Github Navigator application - DI container."""

from aiohttp import web
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dependency_injector import containers, providers

from . import searcher, webhandlers, webapp


class GithubNavigator(containers.DeclarativeContainer):
    """Application components container."""

    config = providers.Configuration()

    github_searcher = providers.Factory(
        searcher.GithubSearcher,
        auth_token=config.github.auth_token,
        request_timeout=config.github.request_timeout,
    )

    template_loader = providers.Singleton(
        FileSystemLoader,
        searchpath=config.webapp.templates_dir,
    )
    template_env = providers.Singleton(
        Environment,
        loader=template_loader,
        autoescape=select_autoescape(['html', 'xml']),
        enable_async=True,
    )

    navigator_webhandler = providers.Coroutine(
        webhandlers.navigator,
        template_env=template_env,
        github_searcher_factory=github_searcher.provider,
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
