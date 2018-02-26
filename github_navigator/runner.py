"""Github Navigator application - runner."""


def run_web(application):
    """Run web application."""
    webapp = application.webapp()
    webapp.add_route(application.navigator_webhandler, 'navigator/')
    webapp.run(host=application.config.webapp.host(),
               port=application.config.webapp.port(),
               debug=application.config.webapp.debug())
