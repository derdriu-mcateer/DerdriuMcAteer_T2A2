from setup import app

from blueprints.cli_bp import db_commands
from blueprints.courses_bp import courses_bp
from blueprints.educators_bp import educators_bp
from blueprints.users_bp import users_bp
from blueprints.auth_bp import auth_bp
from blueprints.enrolments_bp import enrolments_bp
from blueprints.reviews_bp import reviews_bp
from blueprints.login_bp import login_bp

app.register_blueprint(db_commands)
app.register_blueprint(courses_bp)
app.register_blueprint(educators_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(enrolments_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(login_bp)