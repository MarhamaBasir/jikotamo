from datetime import datetime
from blog_ku import db, login_manager, app
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

admin = Admin(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
class User(db.Model, UserMixin):
	id=db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}','{self.image_file}','{self.password}')"


class InfoDesa(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title =db.Column(db.String(100), nullable=False)
	konten = db.Column(db.Text, nullable=False)
	ttd =db.Column(db.String(100), nullable=True)

	def __repr__(self):
		return f"SejarahDesa('{self.title}','{self.konten}','{self.ttd}')"

class Kades(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama =db.Column(db.String(100), nullable=False)
	masa_jabatan = db.Column(db.Text, nullable=False)
	no_hp = db.Column(db.String(30), nullable=True)

	def __repr__(self):
		return f"Kades('{self.nama}','{self.masa_jabatan}','{self.no_hp}')"

class AdminDesa(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	alamat = db.Column(db.Text, nullable=True)
	no_hp = db.Column(db.String(30), nullable=True)
	email = db.Column(db.String(100), nullable=True)

	def __repr__(self):
		return f"AdminDesa('{self.alamat}','{self.no_hp}','{self.email}')"

class Umum(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	luas_desa = db.Column(db.String(30), nullable=True)
	jumlah_dusun = db.Column(db.String(30), nullable=True)
	utara = db.Column(db.String(300), nullable=True)
	selatan = db.Column(db.String(300), nullable=True)
	barat = db.Column(db.String(300), nullable=True)
	timur = db.Column(db.String(300), nullable=True)
	jarak_dari_kec = db.Column(db.String(30), nullable=True)
	jarak_dari_kab = db.Column(db.String(30), nullable=True)
	jarak_dari_prov = db.Column(db.String(30), nullable=True)

	def __repr__(self):
		return f"Umum('{self.luas_desa}','{self.jumlah_dusun}','{self.utara}','{self.selatan}','{self.barat}','{self.timur}','{self.jarak_dari_kec}','{self.jarak_dari_kab}','{self.jarak_dari_prov}')"

class Penduduk(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	jumlah_l = db.Column(db.String(30), nullable=True)
	jumlah_p = db.Column(db.String(30), nullable=True)
	total = db.Column(db.String(30), nullable=True)
	kk = db.Column(db.String(30), nullable=True)
	tahun = db.Column(db.String(10), nullable=True)

	def __repr__(self):
		return f"Penduduk('{self.jumlah_l}','{self.jumlah_p}','{self.total}','{self.kk}','{self.tahun}')"

class SaranaPenunjang(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	paud = db.Column(db.Text, nullable=True)
	tk = db.Column(db.Text, nullable=True)
	sd = db.Column(db.Text, nullable=True)
	smp = db.Column(db.Text, nullable=True)
	sma = db.Column(db.Text, nullable=True)
	tpa = db.Column(db.Text, nullable=True)
	puskesmas = db.Column(db.Text, nullable=True)
	posyandu = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return f"SaranaPenunjang('{self.paud}','{self.tk}','{self.sd}','{self.smp}','{self.sma}','{self.tpa}','{self.puskesmas}','{self.posyandu}')"

class AnggaranDesa(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tahun = db.Column(db.String(30), nullable=True)
	add = db.Column(db.String(30), nullable=True)
	dd = db.Column(db.String(30), nullable=True)

	def __repr__(self):
		return f"Penduduk('{self.tahun}','{self.add}','{self.dd}')"

class PengurusBumdes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama_pengurus = db.Column(db.String(100), nullable=True)
	masa_jabatan_pengurus = db.Column(db.Text, nullable=True)
	no_hp_pengurus = db.Column(db.String(30), nullable=True)

	def __repr__(self):
		return f"PengurusBumdes('{self.nama_pengurus}','{self.masa_jabatan_pengurus}','{self.no_hp_pengurus}')"

class AdminBumdes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama_bumdes = db.Column(db.String(100), nullable=True)
	alamat_bumdes = db.Column(db.Text, nullable=True)
	no_hp_bumdes = db.Column(db.String(30), nullable=True)
	email_bumdes = db.Column(db.String(100), nullable=True)

	def __repr__(self):
		return f"AdminBumdes('{self.nama}','{self.alamat}','{self.no_hp}','{self.email}')"

class UnitUsaha(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama_unit_usaha = db.Column(db.String(100), nullable=True)

	def __repr__(self):
		return f"AdminBumdes('{self.nama}')"

class KeuanganBumdes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	penyertaan_modal = db.Column(db.String(100), nullable=True)
	penambahan_modal = db.Column(db.String(100), nullable=True)

class Gambar(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	foto_struktur = db.Column(db.String(20), nullable=False, default='default.jpg')

	def __repr__(self):
		return f"Gambar('{self.foto_struktur}')"

class Gambar2(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	foto_organisasi = db.Column(db.String(20), nullable=False, default='default.jpg')

	def __repr__(self):
		return f"Gambar('{self.foto_organisasi}')"

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(InfoDesa, db.session))
admin.add_view(ModelView(Kades, db.session))
admin.add_view(ModelView(AdminDesa, db.session))
admin.add_view(ModelView(Umum, db.session))
admin.add_view(ModelView(Penduduk, db.session))
admin.add_view(ModelView(SaranaPenunjang, db.session))
admin.add_view(ModelView(AnggaranDesa, db.session))
admin.add_view(ModelView(PengurusBumdes, db.session))
admin.add_view(ModelView(AdminBumdes, db.session))
admin.add_view(ModelView(UnitUsaha, db.session))
admin.add_view(ModelView(KeuanganBumdes, db.session))
admin.add_view(ModelView(Gambar, db.session))
admin.add_view(ModelView(Gambar2, db.session))