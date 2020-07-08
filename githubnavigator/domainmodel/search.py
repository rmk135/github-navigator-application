"""GitHub Navigator application - search component."""

import asyncio
import json
from typing import Optional

import aiohttp
import async_timeout


class GithubSearch:
    """GitHub search performs search on Github."""

    API_URL = 'https://api.github.com/'
    DEFAULT_LIMIT = 5

    def __init__(
            self, *,
            auth_token: Optional[str],
            request_timeout: Optional[int] = DEFAULT_LIMIT,
    ) -> None:
        """Initialize search."""
        self._auth_token = auth_token
        self._request_timeout = request_timeout

    async def search_repositories(self, search_term, limit):
        """Search repositories."""
        if not search_term:
            return []

        headers = {}
        if self._auth_token:
            headers['authorization'] = f'token {self._auth_token}'

        async with aiohttp.ClientSession(headers=headers) as session:
            repositories = await self._make_search(session, search_term, limit)

            latest_commits = await asyncio.gather(
                *[
                    self._get_latest_commit(session, repository, search_term)
                    for repository in repositories
                ]
            )

            return list(zip(repositories, latest_commits))

    async def _make_search(self, session, search_term, limit):
        url = f'{self.API_URL}search/repositories'
        params = {
            'q': f'{search_term} in:name',
            'sort': 'updated',
            'order': 'desc',
            'page': 1,
            'per_page': limit,
        }
        async with async_timeout.timeout(self._request_timeout):
            async with session.get(url, params=params) as response:
                response = await response.text()
                response_data = json.loads(response)
                return response_data['items']

    async def _get_latest_commit(self, session, repository, search_term):
        url = repository['commits_url'].replace('{/sha}', '')
        params = {
            'q': f'{search_term} in:name',
            'sort': 'updated',
            'order': 'desc',
            'page': 1,
            'per_page': 1,
        }
        async with async_timeout.timeout(self._request_timeout):
            async with session.get(url, params=params) as response:
                response = await response.text()
                response_data = json.loads(response)
                return response_data[0]
