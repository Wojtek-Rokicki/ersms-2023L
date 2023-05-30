import uvicorn

from ersms_test.settings import get_config


def run() -> None:
    config = get_config()
    uvicorn.run('ersms_test.api.app:app',
                host=config.HOST,
                port=config.PORT,
                log_level=config.LOG_LEVEL,
                log_config=config.LOGGING_CONFIG,
                loop="asyncio",
                reload=config.DEBUG,
                workers=config.WORKERS)


if __name__ == '__main__':
    run()

