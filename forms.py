from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, Optional, EqualTo
from werkzeug.utils import secure_filename
from models import db, Skill, Profile
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    judul = StringField('Judul Proyek', validators=[DataRequired(), Length(max=200)])
    deskripsi_singkat = TextAreaField('Deskripsi Singkat', validators=[DataRequired()])
    deskripsi_lengkap = TextAreaField('Deskripsi Lengkap', validators=[DataRequired()])
    teknologi = StringField('Teknologi (pisahkan dengan koma)', validators=[Optional(), Length(max=500)])
    github_link = StringField('Link GitHub', validators=[Optional(), URL(), Length(max=200)])
    live_link = StringField('Link Live Demo', validators=[Optional(), URL(), Length(max=200)])
    gambar = FileField('Gambar Proyek', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Hanya gambar yang diizinkan!'),
        FileRequired()
    ])
    submit = SubmitField('Simpan')

class EditProjectForm(FlaskForm):
    judul = StringField('Judul Proyek', validators=[DataRequired(), Length(max=200)])
    deskripsi_singkat = TextAreaField('Deskripsi Singkat', validators=[DataRequired()])
    deskripsi_lengkap = TextAreaField('Deskripsi Lengkap', validators=[DataRequired()])
    teknologi = StringField('Teknologi (pisahkan dengan koma)', validators=[Optional(), Length(max=500)])
    github_link = StringField('Link GitHub', validators=[Optional(), URL(), Length(max=200)])
    live_link = StringField('Link Live Demo', validators=[Optional(), URL(), Length(max=200)])
    gambar = FileField('Ganti Gambar Proyek (biarkan kosong jika tidak ingin mengganti)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Hanya gambar yang diizinkan!')
    ])
    submit = SubmitField('Update Proyek')

class ProfileForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired(), Length(max=100)])
    nim = StringField('NIM', validators=[Length(max=20)])
    kelas = StringField('Kelas', validators=[Length(max=20)])
    dosen_pengampu = StringField('Dosen Pengampu', validators=[Length(max=100)])
    headline = StringField('Headline/Tagline', validators=[Length(max=200)])
    about = TextAreaField('Tentang Saya', validators=[DataRequired()])
    foto_profil = FileField('Foto Profil', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Hanya gambar yang diizinkan!')
    ])
    # We'll handle skills separately via a separate form or inline in the template
    submit = SubmitField('Simpan Profil')

class SkillForm(FlaskForm):
    nama = StringField('Nama Skill', validators=[DataRequired(), Length(max=50)])
    kategori = StringField('Kategori', validators=[DataRequired(), Length(max=50)])
    level = StringField('Tingkat Kepahiran (0-100)', validators=[
        DataRequired(),
        # We'll use a custom validator or just rely on the front-end for now, but let's add a basic one
        # For simplicity, we'll use a StringField and validate in the view or use IntegerRange if available
        # Since WTForms doesn't have IntegerRange by default, we'll use a StringField and convert in view.
        # Alternatively, we can use IntegerField with NumberRange if we have WTForms version that supports it.
        # Let's use StringField and convert to int in the view, with a simple validator for digits.
    ])
    submit = SubmitField('Tambah Skill')

class MessageForm(FlaskForm):
    name = StringField('Nama', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    message = TextAreaField('Pesan', validators=[DataRequired()])
    submit = SubmitField('Kirim Pesan')

# We'll also create a form for deleting items (with confirmation) but that can be handled in the route with a simple form.
# Alternatively, we can use a simple form with a CSRF token for deletion.
class DeleteForm(FlaskForm):
    submit = SubmitField('Hapus')