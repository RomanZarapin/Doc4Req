from aiohttp import web
from aiohttp.web import json_response, StreamResponse


def init(app):
    prefix = "/api/test"
    app.router.add_post(f"{prefix}/test_endpoint", test_endpoint)


async def test_endpoint(request: web.Request) -> web.Response:
    message = await request.json()
    return json_response(data={"success": True})