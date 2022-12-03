import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(threadName)-10s %(name)-15s %(levelname)-5s %(message)s"
)
logging.getLogger("werkzeug").setLevel("WARNING")

env = os.environ

db = SQLAlchemy()


class Me(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return f"<{self.id}: {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

def setup_db(app, db_user, db_pass, db_host, db_name):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
    logger.info(app.config.get("SQLALCHEMY_DATABASE_URI"))
    db.app = app
    db.init_app(app)


def create_app():
    app = Flask(__name__)
    db_user = env.get("db_user", "abdullah")
    db_pass = env.get("db_pass", "abdullah")
    db_host = env.get("db_host", "localhost")
    db_name = env.get("db_name", "abdullah")
    logger.info((db_user, db_pass, db_host, db_name))
    setup_db(app, db_user, db_pass, db_host, db_name)
    try:
        with app.app_context():
            logger.info("dropping all tables 🔁")
            db.drop_all()
            logger.info("dropping done ... ✔")
            logger.info("creating all tables 🔁")
            db.create_all()
            logger.info("creating done ... ✔")

    except Exception as e:
        logger.critical(type(e))
        logger.critical(e)

    # / => index
    @app.route("/", methods=["GET", ])
    def index():
        me = Me(name=f"Abdullah {request.remote_addr}")
        me.save()
        res = db.session.execute(db.select(Me)).scalars()
        data = [{item.id: item.name} for item in res]
        return data, 200

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
