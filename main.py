from colorama import init
import logging

from configuration.config import settings
import configuration.base

import uvicorn


init()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s:%(name)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')


async def main():
    web_api_config = uvicorn.Config(
        app="web_api:app",
        log_level="debug",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=False,
        use_colors=True,
    )
    web_api_server = uvicorn.Server(web_api_config)

    await web_api_server.serve()


if __name__ == "__main__":
    configuration.base.current_event_loop.run_until_complete(main())
