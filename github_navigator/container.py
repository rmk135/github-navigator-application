"""Github Navigator application - DI container."""

from sanic import Sanic
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dependency_injector import containers, providers

from . import searcher, webhandlers


class GithubNavigator(containers.DeclarativeContainer):
    """Application components container."""

    config = providers.Configuration('config', default={
            'webapp': {
                'templates_dir': 'github_navigator/templates/',
                'host': '0.0.0.0',
                'port': 80,
                'debug': False,
            },
            'github': {
                'request_timeout': 10.0,
            },
        },
    )

    github_searcher = providers.Factory(
        searcher.GithubSearcher,
        auth_token=config.github.auth_token,
        request_timeout=config.github.request_timeout,
    )

    webapp = providers.Factory(Sanic, __name__)

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

    navigator_webhandler = providers.Callable(
        webhandlers.navigator,
        template_env=template_env,
        github_searcher_factory=github_searcher.provider,
    )
