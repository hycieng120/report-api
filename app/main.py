# app/main.py
from flask import Flask
from app.api.routes import api
from app.models import Base
from app.database import engine

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def home():
        return "Flask API is running!"

    # 把 API Blueprint 掛在 /api
    app.register_blueprint(api, url_prefix="/api")

    # 初始化資料表（正式上線改用 Alembic）
    Base.metadata.create_all(bind=engine)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)