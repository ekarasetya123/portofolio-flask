import os
import json
from app import create_app, db
from models import User, Profile, Skill, Project

def seed_database():
    """Seed database with data from DATA INPUT"""
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Create admin user if not exists
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'ekaprasetyaa007@gmail.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin')  # Change this in production!

        if not User.query.filter_by(username=admin_username).first():
            admin = User(
                username=admin_username,
                email=admin_email,
                is_admin=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            print(f'Admin user "{admin_username}" created.')
        else:
            print(f'Admin user "{admin_username}" already exists.')

        # Create profile if not exists
        if not Profile.query.first():
            profile = Profile(
                nama_lengkap='Eka Prasetya Wardana',
                nim='301250023',
                kelas='',  # tidak dipakai
                dosen_pengampu='',  # tidak dipakai
                headline='Backend Developer | Python & Flask Enthusiast',
                about='''Saya Eka Prasetya Wardana, mahasiswa Teknik Informatika di Universitas Bale Bandung (UNIBBA) angkatan 2025. Saya tertarik pada pengembangan web, khususnya membangun aplikasi backend menggunakan Python dan Flask.
Ketertarikan ini bermula dari mata kuliah Pengantar Pemrograman, di mana saya belajar dari dasar-dasar logika pemrograman hingga membangun aplikasi web yang fungsional dan terhubung dengan database.
Saya senang mengeksplorasi cara kerja sistem di balik layar — mulai dari routing, pengolahan data, hingga menyusun antarmuka yang rapi menggunakan template engine. Website portofolio ini sendiri adalah salah satu hasil belajar saya dalam menerapkan konsep CRUD, autentikasi, dan pengelolaan database secara nyata.''',
                foto_profil='profile.jpg'  # gunakan foto yang sudah diupload user (crop persegi disarankan)
            )
            # Set pendidikan as JSON
            pendidikan_list = [
                {
                    "institusi": "Universitas Bale Bandung (UNIBBA)",
                    "jurusan": "Teknik Informatika",
                    "tahun": "2025 - sekarang"
                }
            ]
            profile.set_pendidikan_list(pendidikan_list)
            db.session.add(profile)
            print('Profile created.')
        else:
            print('Profile already exists.')

        # Create skills if not exist
        skills_data = [
            {"name": "Python", "category": "Bahasa Pemrograman", "level": 80},
            {"name": "Flask", "category": "Framework", "level": 70},
            {"name": "HTML5", "category": "Bahasa Markup", "level": 85},
            {"name": "CSS3", "category": "Styling", "level": 75},
            {"name": "JavaScript", "category": "Bahasa Pemrograman", "level": 60},
            {"name": "SQL / SQLite", "category": "Database", "level": 65},
            {"name": "Git & GitHub", "category": "Version Control", "level": 70},
            {"name": "Logika & Algoritma", "category": "Fundamental", "level": 80}
        ]

        for skill_data in skills_data:
            if not Skill.query.filter_by(name=skill_data['name']).first():
                skill = Skill(
                    name=skill_data['name'],
                    category=skill_data['category'],
                    level=skill_data['level']
                )
                db.session.add(skill)
                print(f'Skill "{skill_data["name"]}" created.')
            else:
                print(f'Skill "{skill_data["name"]}" already exists.')

        # Create projects if not exist
        projects_data = [
            {
                "judul": "KalkulatorPro — Aplikasi Web Kalkulator Canggih",
                "deskripsi_singkat": "Kalkulator web dengan operasi aritmatika, logika, konversi bilangan, dan riwayat perhitungan.",
                "deskripsi_lengkap": '''Aplikasi web kalkulator berbasis Python Flask dengan tampilan modern.
Mendukung operasi aritmatika (tambah, kurang, kali, bagi, pangkat, akar, modulus, floor division),
operator logika (AND, OR, NOT, XOR, NAND, NOR) lengkap dengan tabel kebenaran, serta transformasi bilangan: konversi basis (desimal/biner/oktal/heksadesimal), konversi suhu, konversi mata uang, faktorial, dan deret Fibonacci. Dilengkapi dark/light mode dan riwayat perhitungan.''',
                "teknologi": "Python, Flask, HTML, CSS, JavaScript, Jinja2",
                "github_link": "https://github.com/ekarasetya123/kalkulator-eka",
                "live_link": "",
                "gambar": "project-kalkulator.jpg"   # screenshot aplikasi kalkulator, siapkan sendiri
            },
            {
                "judul": "Web Portofolio Dinamis (Proyek Ini)",
                "deskripsi_singkat": "Website portofolio pribadi dengan dashboard admin, CRUD proyek, dan sistem pesan kontak.",
                "deskripsi_lengkap": '''Aplikasi web portofolio dinamis dibangun dengan Python Flask,
Flask-SQLAlchemy, dan SQLite. Terdiri dari halaman publik (Home, About, Portofolio, Detail Proyek, Kontak)
dan dashboard admin dengan autentikasi login, manajemen proyek (CRUD), upload gambar, manajemen profil, dan
kotak masuk pesan. Dibangun sebagai capstone project mata kuliah Pengantar Pemrograman.''',
                "teknologi": "Python, Flask, Flask-SQLAlchemy, Flask-Login, SQLite, Jinja2, Bootstrap 5",
                "github_link": "",    # isi setelah repo dibuat
                "live_link": "",      # isi setelah deploy
                "gambar": "project-portofolio.jpg"   # screenshot halaman home portofolio ini
            }
        ]

        for project_data in projects_data:
            if not Project.query.filter_by(judul=project_data['judul']).first():
                project = Project(
                    judul=project_data['judul'],
                    deskripsi_singkat=project_data['deskripsi_singkat'],
                    deskripsi_lengkap=project_data['deskripsi_lengkap'],
                    teknologi=project_data['teknologi'],
                    github_link=project_data['github_link'],
                    live_link=project_data['live_link'],
                    gambar=project_data['gambar']
                )
                db.session.add(project)
                print(f'Project "{project_data["judul"]}" created.')
            else:
                print(f'Project "{project_data["judul"]}" already exists.')

        # Commit all changes
        db.session.commit()
        print('Database seeding completed.')

if __name__ == '__main__':
    seed_database()