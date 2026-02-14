# app.py
from datetime import datetime

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faca login para acessar o sistema."
login_manager.login_message_category = "warning"

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.clientes import clientes_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(api_bp)

    # Rota raiz -> login
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # Variáveis globais nos templates
    @app.context_processor
    def inject_globals():
        return {
            "empresa_nome": app.config.get("EMPRESA_NOME", ""),
            "empresa_cnpj": app.config.get("EMPRESA_CNPJ", ""),
            "agora": datetime.now(),
        }

    # Importa models (necessário para o Alembic/Flask-Migrate enxergar as tabelas)
    with app.app_context():
        import models.usuario  # noqa: F401
        import models.cliente  # noqa: F401
        _criar_dados_iniciais()

    return app


def _criar_dados_iniciais():
    from models.usuario import Usuario

    if not Usuario.query.filter_by(login="MACIEL").first():
        admin = Usuario(nome="MACIEL PRATES", login="MACIEL", perfil="admin")
        admin.set_senha("m2admin")
        db.session.add(admin)
        db.session.commit()
