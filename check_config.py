from app import create_app
app = create_app()
print(app.config.get('SQLALCHEMY_DATABASE_URI'))
