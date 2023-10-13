from app import create_app
from app.database import get_db,close_db
from app.models import User

# add a admin user
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db_session = get_db()
        admin = User(name='Kunal Sharma', email='kunal.ucet@gmail.com', password='admin', admin=True)
        db_session.add(admin)
        db_session.commit()
        print(f'Admin user created: {admin.name}')
        close_db()
