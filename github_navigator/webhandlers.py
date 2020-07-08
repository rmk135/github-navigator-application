"""GitHub Navigator application - web request handlers."""

from aiohttp import web
import jinja2

from .search import GithubSearch


async def navigator(request: web.Request, *, template_env: jinja2.Environment, github_search: GithubSearch):
    """Navigator request handler."""
    search_term = request.query.get('search_term')
    limit = request.query.get('limit', 5)

    repositories = await github_search.search_repositories(search_term, limit)

    template = template_env.get_template('navigator.html')
    rendered_template = await template.render_async(
        search_term=search_term,
        results=repositories,
    )

    return web.Response(body=rendered_template, content_type='text/html', charset='utf-8')
