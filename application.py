"""Github Navigator application - entrypoint."""

from github_navigator import GithubNavigator


if __name__ == '__main__':
    application = GithubNavigator()
    application.config.from_yaml('config.yml')
    application.run_webapp()
