"""Website request handlers module."""

from aiohttp import web
import jinja2

from githubnavigator.search import GithubSearch


async def navigator(
        request: web.Request,
        *,
        template_env: jinja2.Environment,
        github_search: GithubSearch,
        default_search_term: str,
        default_search_limit: int,
) -> web.Response:
    """Navigator request handler."""
    search_term = request.query.get('search_term', default_search_term)
    limit = request.query.get('limit', default_search_limit)

    repositories = await github_search.search_repositories(search_term, limit)

    template = template_env.get_template('navigator.html')
    rendered_template = await template.render_async(
        search_term=search_term,
        limit=limit,
        results=repositories,
    )

    return web.Response(body=rendered_template, content_type='text/html', charset='utf-8')
