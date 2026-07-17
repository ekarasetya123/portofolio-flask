from app import create_app, db
from models import Project

app = create_app()
with app.app_context():
    # Find project by id=3
    proj = Project.query.get(3)
    if proj:
        print(f"Deleting project: {proj.judul} (ID={proj.id})")
        db.session.delete(proj)
        db.session.commit()
        print("Project deleted.")
    else:
        print("Project with id=3 not found.")
