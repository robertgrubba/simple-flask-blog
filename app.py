from flask import Flask

from core.core import core_bp

app = Flask(__name__)

app.register_blueprint(core_bp)
