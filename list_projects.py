from app import create_app, db
from models import Project

app = create_app()
with app.app_context():
    projects = Project.query.all()
    print(f"Total projects: {len(projects)}")
    for p in projects:
        print(f"ID: {p.id}, Judul: {p.judul}")
