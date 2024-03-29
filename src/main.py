from config import app

from blueprints.cli_bp import db_commands
from blueprints.courses_bp import courses_bp
from blueprints.educators_bp import educators_bp
from blueprints.users_bp import users_bp
from blueprints.auth_bp import auth_bp


app.register_blueprint(db_commands)
app.register_blueprint(courses_bp)
app.register_blueprint(educators_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

