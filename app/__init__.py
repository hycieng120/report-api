from flask import Flask

def create_app():
    app = Flask(__name__)

    # 載入 API Blueprint
    from app.api.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app