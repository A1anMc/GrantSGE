from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here to avoid circular imports
    from .user import User
    from .grant import Grant
    from .organisation import OrganisationProfile
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 