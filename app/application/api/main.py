from fastapi import FastAPI

from application.api.messages.handlers import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='A simple kafka + ddd example.',
        debug=True,
    )
    app.include_router(message_router, prefix='/chat')

    return app
