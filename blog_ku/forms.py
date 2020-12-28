from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog_ku.models import User, InfoDesa, Kades, AdminDesa, Umum, Penduduk, SaranaPenunjang, AnggaranDesa, PengurusBumdes, AdminBumdes, UnitUsaha, KeuanganBumdes, Gambar, Gambar2
from flask_login import current_user 
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField

class Registrasi_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	konfirmasi_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField ('Daftar')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')
			
	def validate_password(self, password):
		user = User.query.filter_by(password=password.data).first()
		if user:
			raise ValidationError('Password yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

class Loginadmin_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField ('Password', validators=[DataRequired()])
	remember= BooleanField('Remember Me')
	submit = SubmitField ('Login')

class Update_Account_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	foto = FileField('Update Foto Profil', validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data). first()
			if user:
				raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

	def validate_emial(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data). first()
			if user:
				raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')


class InfoDesa_F(FlaskForm):
	title =StringField('Title', validators=[DataRequired()])
	konten = CKEditorField('Konten', validators=[DataRequired()])
	title =StringField('Title', validators=[DataRequired()])
	ttd =StringField('Tanda Tangan', validators=[DataRequired()])
	submit=SubmitField('Save')

class Kades_F(FlaskForm):
	nama = StringField('Nama', validators=[DataRequired()])
	masa_jabatan = TextAreaField('Masa Jabatan', validators=[DataRequired()])
	no_hp = StringField('No Telpon', validators=[DataRequired()])
	submit=SubmitField('Save')

class AdminDesa_F(FlaskForm):
	alamat = TextAreaField('Alamat Kantor Desa', validators=[DataRequired()])
	no_hp = StringField('No Telpon', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	submit = SubmitField('Save')

class Umum_F(FlaskForm):
	luas_desa = StringField('Luas Desa', validators=[DataRequired()])
	jumlah_dusun = StringField('Jumlah Dusun', validators=[DataRequired()])
	utara = StringField('Batas Utara', validators=[DataRequired()])
	selatan = StringField('Batas Selatan', validators=[DataRequired()])
	barat = StringField('Batas Barat', validators=[DataRequired()])
	timur = StringField('Batas Timur', validators=[DataRequired()])
	jarak_dari_kec = StringField('Jarak Dari Kecamatan', validators=[DataRequired()])
	jarak_dari_kab = StringField('Jarak Dari Kabupaten', validators=[DataRequired()])
	jarak_dari_prov = StringField('Jarak Dari Provinsi', validators=[DataRequired()])
	submit = SubmitField('Save')

class Penduduk_F(FlaskForm):
	jumlah_l = StringField('Jumlah Laki-laki', validators=[DataRequired()])
	jumlah_p = StringField('Jumlah Perempuan', validators=[DataRequired()])
	total = StringField('Total', validators=[DataRequired()])
	kk = StringField('Jumlah KK', validators=[DataRequired()])
	tahun = StringField('Tahun', validators=[DataRequired()])
	submit = SubmitField('Save')

class SaranaPenunjang_F(FlaskForm):
	paud = TextAreaField('PAUD', validators=[DataRequired()])
	tk = TextAreaField('TK', validators=[DataRequired()])
	sd = TextAreaField('SD', validators=[DataRequired()])
	smp = TextAreaField('SMP/MTS', validators=[DataRequired()])
	sma = TextAreaField('SMA/SMK/MA', validators=[DataRequired()])
	tpa = TextAreaField('Pesantren/Balai Pengajian', validators=[DataRequired()])
	puskesmas = TextAreaField('Puskesmas', validators=[DataRequired()])
	posyandu = TextAreaField('Posyandu', validators=[DataRequired()])
	submit = SubmitField('Save')

class AnggaranDesa_F(FlaskForm):
	tahun = StringField('Tahun', validators=[DataRequired()])
	add = StringField('ADD', validators=[DataRequired()])
	dd = StringField('DD', validators=[DataRequired()])
	submit = SubmitField('Save')

class PengurusBumdes_F(FlaskForm):
	nama_pengurus = StringField('Nama', validators=[DataRequired()])
	masa_jabatan_pengurus = TextAreaField('Masa Jabatan', validators=[DataRequired()])
	no_hp_pengurus = StringField('No Telpon', validators=[DataRequired()])
	submit=SubmitField('Save')

class AdminBumdes_F(FlaskForm):
	nama_bumdes = StringField('Nama BUMDES', validators=[DataRequired()])
	alamat_bumdes = TextAreaField('Alamat Kantor BUMDES', validators=[DataRequired()])
	no_hp_bumdes = StringField('No Telpon BUMDES', validators=[DataRequired()])
	email_bumdes = StringField('Email BUMDES', validators=[DataRequired()])
	submit = SubmitField('Save')

class UnitUsaha_F(FlaskForm):
	nama_unit_usaha = StringField('Nama Unit Usaha', validators=[DataRequired()])
	submit = SubmitField('Save')

class KeuanganBumdes_F(FlaskForm):
	penyertaan_modal = StringField('Penyertaan Modal', validators=[DataRequired()])
	penambahan_modal = StringField('Penambahan Modal', validators=[DataRequired()])
	submit = SubmitField('Save')

class Gambar_F(FlaskForm):
	foto_struktur = FileField('Update Foto Struktur Pemerintahan', validators=[FileAllowed(['jpg','png'])])
	foto_organisasi = FileField('Update Foto Organisasi Desa', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Save')

class Gambar2_F(FlaskForm):
	foto_organisasi = FileField('Update Foto Organisasi Desa', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Save')