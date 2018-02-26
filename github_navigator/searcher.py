"""GitHub Navigator application - searcher component."""

import asyncio
import json

import aiohttp
import async_timeout


class GithubSearcher:
    """GitHub searcher."""

    API_URL = 'https://api.github.com/'

    def __init__(self, search_term, limit, *, auth_token, request_timeout):
        """Initializer."""
        self._search_term = search_term
        self._limit = limit
        self._auth_token = auth_token
        self._request_timeout = request_timeout

    async def get_search_results(self):
        """Return search results."""
        headers = {'authorization': f'token {self._auth_token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            repositories = await self._make_search(session)

            latest_commits = await asyncio.gather(
                *(self._get_lastest_commit(session, repository)
                  for repository in repositories))

            return zip(repositories, latest_commits)

    async def _make_search(self, session):
        url = f'{self.API_URL}search/repositories'
        params = {'q': f'{self._search_term} in:name',
                  'sort': 'updated',
                  'order': 'desc',
                  'page': 1,
                  'per_page': self._limit}
        async with async_timeout.timeout(self._request_timeout):
            async with session.get(url, params=params) as response:
                response = await response.text()
                response_data = json.loads(response)
                return response_data['items']

    async def _get_lastest_commit(self, session, repository):
        url = repository['commits_url'].replace('{/sha}', '')
        params = {'q': f'{self._search_term} in:name',
                  'sort': 'updated',
                  'order': 'desc',
                  'page': 1,
                  'per_page': 1}
        async with async_timeout.timeout(self._request_timeout):
            async with session.get(url, params=params) as response:
                response = await response.text()
                response_data = json.loads(response)
                return response_data[0]
