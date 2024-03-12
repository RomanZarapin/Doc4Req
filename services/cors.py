import aiohttp_cors
import os


def setup_cors(app):
    available_hosts = os.getenv('ALLOWED_CORS_HOST', '*')
    options = {}
    for host in available_hosts.split(','):
        options[host] = aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(
        app,
        defaults=options
    )

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)
