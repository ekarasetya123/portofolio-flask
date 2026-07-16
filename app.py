import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from datetime import datetime
import secrets
import json

# Import local modules
from config import Config
from models import db, User, Profile, Skill, Project, Message
from forms import LoginForm, ProjectForm, EditProjectForm, ProfileForm, SkillForm, MessageForm, DeleteForm

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Create tables and default data
    with app.app_context():
        db.create_all()
        # Create default profile if not exists
        if not Profile.query.first():
            profile = Profile(nama_lengkap='Nama Anda', headline='Judul Tagline', about='Tentang saya...')
            db.session.add(profile)
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin')
            db.session.add(admin)
        db.session.commit()

    # Context processor supaya {{ now() }} bisa dipakai di semua template
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    
    # Helper function to save uploaded file
    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_fn)
        form_picture.save(picture_path)
        return picture_fn

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Public routes
    @app.route('/')
    def index():
        profile = Profile.query.first()
        projects = Project.query.order_by(Project.created_at.desc()).limit(6).all()
        skills = Skill.query.order_by(Skill.level.desc()).limit(6).all()
        return render_template('index.html', profile=profile, projects=projects, skills=skills)

    @app.route('/about')
    def about():
        profile = Profile.query.first()
        skills = Skill.query.order_by(Skill.level.desc()).all()
        return render_template('about.html', profile=profile, skills=skills)

    @app.route('/portfolio')
    def portfolio():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('portfolio.html', projects=projects)

    @app.route('/project/<int:project_id>')
    def project_detail(project_id):
        project = Project.query.get_or_404(project_id)
        return render_template('project_detail.html', project=project)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = MessageForm()
        if form.validate_on_submit():
            message = Message(
                name=form.name.data,
                email=form.email.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            flash('Pesan Anda telah terkirim! Saya akan membalas secepatnya.', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form, profile=Profile.query.first())

    # Admin routes - Login/Logout
    @app.route('/dashboard/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                flash('Login berhasil!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login gagal. Periksa username dan password Anda.', 'danger')
        return render_template('dashboard/login.html', form=form)

    @app.route('/dashboard/logout')
    @login_required
    def logout():
        logout_user()
        flash('Anda telah logout.', 'info')
        return redirect(url_for('index'))

    # Dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if not current_user.is_admin:
            abort(403)
        total_projects = Project.query.count()
        total_messages = Message.query.count()
        unread_messages = Message.query.filter_by(is_read=False).count()
        total_skills = Skill.query.count()
        return render_template('dashboard/index.html',
                               total_projects=total_projects,
                               total_messages=total_messages,
                               unread_messages=unread_messages,
                               total_skills=total_skills)

    # Project CRUD
    @app.route('/dashboard/projects')
    @login_required
    def admin_projects():
        if not current_user.is_admin:
            abort(403)
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('dashboard/projects.html', projects=projects)

    @app.route('/dashboard/project/add', methods=['GET', 'POST'])
    @login_required
    def add_project():
        if not current_user.is_admin:
            abort(403)
        form = ProjectForm()
        if form.validate_on_submit():
            # Save image
            if form.gambar.data:
                picture_file = save_picture(form.gambar.data)
            else:
                picture_file = 'default-project.jpg'
            project = Project(
                judul=form.judul.data,
                deskripsi_singkat=form.deskripsi_singkat.data,
                deskripsi_lengkap=form.deskripsi_lengkap.data,
                teknologi=form.teknologi.data,
                github_link=form.github_link.data,
                live_link=form.live_link.data,
                gambar=picture_file
            )
            db.session.add(project)
            db.session.commit()
            flash('Proyek berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_projects'))
        return render_template('dashboard/add_project.html', form=form, title='Tambah Proyek')

    @app.route('/dashboard/project/edit/<int:project_id>', methods=['GET', 'POST'])
    @login_required
    def edit_project(project_id):
        if not current_user.is_admin:
            abort(403)
        project = Project.query.get_or_404(project_id)
        form = EditProjectForm()
        if form.validate_on_submit():
            project.judul = form.judul.data
            project.deskripsi_singkat = form.deskripsi_singkat.data
            project.deskripsi_lengkap = form.deskripsi_lengkap.data
            project.teknologi = form.teknologi.data
            project.github_link = form.github_link.data
            project.live_link = form.live_link.data
            if form.gambar.data:
                # Delete old image if not default
                if project.gambar != 'default-project.jpg':
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], project.gambar)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                picture_file = save_picture(form.gambar.data)
                project.gambar = picture_file
            project.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Proyek berhasil diperbarui!', 'success')
            return redirect(url_for('admin_projects'))
        elif request.method == 'GET':
            form.judul.data = project.judul
            form.deskripsi_singkat.data = project.deskripsi_singkat
            form.deskripsi_lengkap.data = project.deskripsi_lengkap
            form.teknologi.data = project.teknologi
            form.github_link.data = project.github_link
            form.live_link.data = project.live_link
        return render_template('dashboard/edit_project.html', form=form, title='Edit Proyek', project=project)

    @app.route('/dashboard/project/delete/<int:project_id>', methods=['POST'])
    @login_required
    def delete_project(project_id):
        if not current_user.is_admin:
            abort(403)
        project = Project.query.get_or_404(project_id)
        # Delete image if not default
        if project.gambar != 'default-project.jpg':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], project.gambar)
            if os.path.exists(image_path):
                os.remove(image_path)
        db.session.delete(project)
        db.session.commit()
        flash('Proyek berhasil dihapus!', 'success')
        return redirect(url_for('admin_projects'))

    # Profile management
    @app.route('/dashboard/profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        if not current_user.is_admin:
            abort(403)
        profile = Profile.query.first()
        if not profile:
            profile = Profile()
            db.session.add(profile)
        form = ProfileForm()
        if form.validate_on_submit():
            profile.nama_lengkap = form.nama_lengkap.data
            profile.nim = form.nim.data
            profile.kelas = form.kelas.data
            profile.dosen_pengampu = form.dosen_pengampu.data
            profile.headline = form.headline.data
            profile.about = form.about.data
            if form.foto_profil.data:
                # Delete old photo if not default
                if profile.foto_profil != 'default-profile.jpg':
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], profile.foto_profil)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                picture_file = save_picture(form.foto_profil.data)
                profile.foto_profil = picture_file
            # Handle pendidikan from textarea
            pendidikan_str = request.form.get('pendidikan', '[]')
            try:
                pendidikan_list = json.loads(pendidikan_str)
                if not isinstance(pendidikan_list, list):
                    raise ValueError
                profile.set_pendidikan_list(pendidikan_list)
            except Exception:
                flash('Format pendidikan tidak valid. Menggunakan data sebelumnya.', 'warning')
            profile.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Profil berhasil diperbarui!', 'success')
            return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
            form.nama_lengkap.data = profile.nama_lengkap
            form.nim.data = profile.nim
            form.kelas.data = profile.kelas
            form.dosen_pengampu.data = profile.dosen_pengampu
            form.headline.data = profile.headline
            form.about.data = profile.about
        return render_template('dashboard/profile.html', form=form, title='Edit Profil', pendidikan_json=json.dumps(profile.get_pendidikan_list()), profile=profile)

    # Skill management
    @app.route('/dashboard/skills')
    @login_required
    def admin_skills():
        if not current_user.is_admin:
            abort(403)
        skills = Skill.query.order_by(Skill.level.desc()).all()
        return render_template('dashboard/skills.html', skills=skills)

    @app.route('/dashboard/skill/add', methods=['GET', 'POST'])
    @login_required
    def add_skill():
        if not current_user.is_admin:
            abort(403)
        form = SkillForm()
        if form.validate_on_submit():
            # Validate proficiency is between 0 and 100
            try:
                proficiency = int(form.level.data)
                if proficiency < 0 or proficiency > 100:
                    flash('Tingkat kepahiran harus antara 0 dan 100.', 'danger')
                    return render_template('dashboard/add_skill.html', form=form, title='Tambah Skill')
            except ValueError:
                flash('Tingkat kepahiran harus berupa angka.', 'danger')
                return render_template('dashboard/add_skill.html', form=form, title='Tambah Skill')
            skill = Skill(
                name=form.nama.data,
                category=form.kategori.data,
                level=proficiency
            )
            db.session.add(skill)
            db.session.commit()
            flash('Skill berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_skills'))
        return render_template('dashboard/add_skill.html', form=form, title='Tambah Skill')

    @app.route('/dashboard/skill/edit/<int:skill_id>', methods=['GET', 'POST'])
    @login_required
    def edit_skill(skill_id):
        if not current_user.is_admin:
            abort(403)
        skill = Skill.query.get_or_404(skill_id)
        form = SkillForm()
        if form.validate_on_submit():
            try:
                proficiency = int(form.level.data)
                if proficiency < 0 or proficiency > 100:
                    flash('Tingkat kepahiran harus antara 0 dan 100.', 'danger')
                    return render_template('dashboard/edit_skill.html', form=form, title='Edit Skill', skill=skill)
            except ValueError:
                flash('Tingkat kepahiran harus berupa angka.', 'danger')
                return render_template('dashboard/edit_skill.html', form=form, title='Edit Skill', skill=skill)
            skill.name = form.nama.data
            skill.category = form.kategori.data
            skill.level = proficiency
            db.session.commit()
            flash('Skill berhasil diperbarui!', 'success')
            return redirect(url_for('admin_skills'))
        elif request.method == 'GET':
            form.nama.data = skill.name
            form.kategori.data = skill.category
            form.level.data = str(skill.level)
        return render_template('dashboard/edit_skill.html', form=form, title='Edit Skill', skill=skill)

    @app.route('/dashboard/skill/delete/<int:skill_id>', methods=['POST'])
    @login_required
    def delete_skill(skill_id):
        if not current_user.is_admin:
            abort(403)
        skill = Skill.query.get_or_404(skill_id)
        db.session.delete(skill)
        db.session.commit()
        flash('Skill berhasil dihapus!', 'success')
        return redirect(url_for('admin_skills'))

    # Message inbox
    @app.route('/dashboard/messages')
    @login_required
    def admin_messages():
        if not current_user.is_admin:
            abort(403)
        messages = Message.query.order_by(Message.created_at.desc()).all()
        return render_template('dashboard/messages.html', messages=messages)

    @app.route('/dashboard/message/<int:message_id>/read', methods=['POST'])
    @login_required
    def mark_as_read(message_id):
        if not current_user.is_admin:
            abort(403)
        message = Message.query.get_or_404(message_id)
        message.is_read = True
        db.session.commit()
        flash('Pesan ditandai sebagai sudah dibaca.', 'success')
        return redirect(url_for('admin_messages'))

    @app.route('/dashboard/message/delete/<int:message_id>', methods=['POST'])
    @login_required
    def delete_message(message_id):
        if not current_user.is_admin:
            abort(403)
        message = Message.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        flash('Pesan berhasil dihapus!', 'success')
        return redirect(url_for('admin_messages'))

    # Serve uploaded files
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # CLI command to create database and admin user
    @app.cli.command('init-db')
    def init_db():
        """Initialize the database and create admin user."""
        db.create_all()
        # Create default profile if not exists
        if not Profile.query.first():
            profile = Profile(nama_lengkap='Nama Anda', headline='Judul Tagline', about='Tentang saya...')
            db.session.add(profile)
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin')
            db.session.add(admin)
        db.session.commit()
        print('Database initialized with sample data.')

    return app

# Flask instance for Vercel, Gunicorn, etc.
app = create_app()

# For running the app directly (e.g., during development)
if __name__ == '__main__':
    app.run(debug=True)