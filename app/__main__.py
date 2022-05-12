from api.flask.factory import create_app
from app.bus.bus import MessageBus
from app.db.sql import SQLAlchemyAdapter

if __name__ == '__main__':
    create_app(MessageBus(SQLAlchemyAdapter())).run()
