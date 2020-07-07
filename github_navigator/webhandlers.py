"""GitHub Navigator application - web request handlers."""

from aiohttp.web import Response


async def navigator(request, *, template_env, github_searcher_factory):
    """Navigator request handler."""
    search_term = request.query.get('search_term')
    limit = request.query.get('limit', 5)

    github_searcher = github_searcher_factory(search_term, limit=limit)
    results = await github_searcher.get_search_results()

    template = template_env.get_template('navigator.html')
    rendered_template = await template.render_async(
        search_term=search_term,
        results=enumerate(results, 1),
    )

    return Response(body=rendered_template, content_type='text/html', charset='utf-8')
