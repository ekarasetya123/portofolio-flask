from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

# Association table for many-to-many between Profile and Skill
profile_skills = db.Table('profile_skills',
    db.Column('profile_id', db.Integer, db.ForeignKey('profile.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20))
    kelas = db.Column(db.String(20))
    dosen_pengampu = db.Column(db.String(100))
    headline = db.Column(db.String(200))
    about = db.Column(db.Text)
    foto_profil = db.Column(db.String(200), default='default-profile.jpg')
    # Pendidikan sebagai JSON string untuk kesederhanaannya
    # Format: [{"institusi": "...", "jurusan": "...", "tahun": "..."}, ...]
    pendidikan = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with skills (many-to-many)
    skills = db.relationship('Skill', secondary=profile_skills, lazy='subquery',
                            backref=db.backref('profiles', lazy=True))

    def get_pendidikan_list(self):
        if self.pendidikan:
            try:
                return json.loads(self.pendidikan)
            except json.JSONDecodeError:
                return []
        return []

    def set_pendidikan_list(self, pendidikan_list):
        self.pendidikan = json.dumps(pendidikan_list)

    def __repr__(self):
        return f'<Profile {self.nama_lengkap}>'

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    category = db.Column(db.String(50))  # Bahasa Pemrograman, Framework, etc.
    level = db.Column(db.Integer, default=0)  # 0-100 percentage

    def __repr__(self):
        return f'<Skill {self.name}>'

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    deskripsi_singkat = db.Column(db.String(500))
    deskripsi_lengkap = db.Column(db.Text)
    teknologi = db.Column(db.String(500))  # Comma-separated list
    github_link = db.Column(db.String(200))
    live_link = db.Column(db.String(200))
    gambar = db.Column(db.String(200))  # filename
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.judul}>'

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.name}>'