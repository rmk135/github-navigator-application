"""Github Navigator application - entrypoint."""

from github_navigator import ConfigLoader, GithubNavigator, run_web


if __name__ == '__main__':
    config_loader = ConfigLoader('config.yml')
    application = GithubNavigator(config=config_loader.load())
    run_web(application)
