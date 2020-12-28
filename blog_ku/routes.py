from flask import render_template, url_for, flash, redirect, request
from blog_ku import app, bcrypt, db
from blog_ku.forms import Registrasi_F, Update_Account_F, Loginadmin_F, InfoDesa_F, Kades_F, AdminDesa_F, Umum_F, Penduduk_F, SaranaPenunjang_F, AnggaranDesa_F, PengurusBumdes_F, AdminBumdes_F, UnitUsaha_F, KeuanganBumdes_F, Gambar_F, Gambar2_F
from blog_ku.models import User, InfoDesa, Kades, AdminDesa, Umum, Penduduk, SaranaPenunjang, AnggaranDesa, PengurusBumdes, AdminBumdes, UnitUsaha, KeuanganBumdes, Gambar, Gambar2
from flask_login import login_user, current_user, logout_user, login_required
import os, secrets, schedule
from PIL import Image
from flask_admin.contrib.sqla import ModelView 


# r_info=schedule.every(2).seconds.do(informasi)
# r_info=schedule.every(2).seconds.do(informasi)

@app.route("/")

@app.route("/home")
def home():
	infos = InfoDesa.query.all()
	gambars = Gambar.query.all()
	gambar = Gambar2.query.all()
	penduduks = Penduduk.query.all()
	admindesas = AdminDesa.query.all()
	return render_template("index.html", title='Home', infos=infos, gambars=gambars, gambar=gambar, penduduks=penduduks, admindesas=admindesas)

@app.route("/sejarah")
def sejarah():
	kadess = Kades.query.all()
	return render_template("sejarah.html", title='Sejarah', kadess=kadess)

@app.route("/informasi")
def informasi():
	kadess = Kades.query.all()
	umums = Umum.query.all()
	saranapenunjangs = SaranaPenunjang.query.all()
	anggarandesas = AnggaranDesa.query.all()
	pengurusbumdess = PengurusBumdes.query.all()
	adminbumdess = AdminBumdes.query.all()
	unitusahas = UnitUsaha.query.all()
	keuangans = KeuanganBumdes.query.all()
	return render_template("more_info.html", title='Profile Desa', kadess=kadess, umums=umums, saranapenunjangs=saranapenunjangs, anggarandesas=anggarandesas, pengurusbumdess=pengurusbumdess, adminbumdess=adminbumdess, unitusahas=unitusahas, keuangans=keuangans)

# ====================================ADMIN ADMIN ADMIN ADMIN====================================

@app.route("/registrasi/admin", methods=['GET', 'POST'])
def registrasi():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Registrasi_F()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Akun {form.username.data} berhasil ditambahkan!', 'success')
		return redirect(url_for('login_admin'))
	return render_template("adminku/registrasi.html", title="Registrasi", form=form)


@app.route("/login/admin", methods=['GET','POST'])
def login_admin():
	if current_user.is_authenticated:
		return redirect(url_for('dasboard'))
	form = Loginadmin_F()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('dasboard'))
		else:
			flash('Login gagal...!, periksa username dan password','danger')   
	return render_template("adminku/login_admin.html", title="Login Admin", form=form)

@app.route("/logoutt")
def logoutt():
	logout_user()
	return redirect(url_for('login_admin'))

@app.route("/dasboard")
@login_required
def dasboard():
	users = User.query.all()
	return render_template("adminku/index_admin.html", title='Index_admin', users=users)

# ==============================DATA USER ADMIN==================================
@app.route("/data/user")
@login_required
def data_user():
	user = User.query.all()
	return render_template("adminku/user.html", title='Data User', user=user)

@app.route("/delete/user<id>", methods=['GET'])
@login_required
def delete_user(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('data_user'))
# =============================INFORMASI DESA====================================

@app.route("/info")
@login_required
def info():
	infos = InfoDesa.query.all()
	return render_template("adminku/info.html", title='Informasi Desa', infos=infos)

@app.route("/delete/info/<id>", methods=['GET'])
@login_required
def delete_info(id):
	info = InfoDesa.query.get(id)
	db.session.delete(info)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('info'))

@app.route("/create/info", methods=['GET','POST'])
@login_required
def create_info():
	form=InfoDesa_F()
	if form.validate_on_submit():
		info = InfoDesa(title=form.title.data, konten=form.konten.data, ttd=form.ttd.data)
		db.session.add(info)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('info'))
	return render_template("adminku/create_info.html", title='Create Data Info', form=form, legend='Data Indo')

@app.route("/data/info/<int:info_id>/update", methods=['GET','POST'])
@login_required
def update_info(info_id):
	info = InfoDesa.query.get(info_id)
	form=InfoDesa_F()
	if form.validate_on_submit():
		info.title=form.title.data
		info.konten=form.konten.data
		info.ttd=form.ttd.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('info', info_id=info.id))
	elif request.method == "GET":
		form.title.data=info.title
		form.konten.data=info.konten
		form.ttd.data=info.ttd
	return render_template ('adminku/create_info.html', title="Update", form=form, legend='Update Data Info')

# ========================================KEPALA DESA========================================
@app.route("/kades")
@login_required
def kades():
	kadess = Kades.query.all()
	return render_template("adminku/kades.html", title='Kepala Desa', kadess=kadess)

@app.route("/delete/kades/<id>", methods=['GET'])
@login_required
def delete_kades(id):
	kades = Kades.query.get(id)
	db.session.delete(kades)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('kades'))

@app.route("/create/kades", methods=['GET','POST'])
@login_required
def create_kades():
	form=Kades_F()
	if form.validate_on_submit():
		kades = Kades(nama=form.nama.data, masa_jabatan=form.masa_jabatan.data, no_hp=form.no_hp.data)
		db.session.add(kades)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('kades'))
	return render_template("adminku/create_kades.html", title='Create Data Kepala Desa', form=form, legend='Data Kades')

@app.route("/data/kades/<int:kades_id>/update", methods=['GET','POST'])
@login_required
def update_kades(kades_id):
	kades = Kades.query.get(kades_id)
	form=Kades_F()
	if form.validate_on_submit():
		kades.nama=form.nama.data
		kades.masa_jabatan=form.masa_jabatan.data
		kades.no_hp=form.no_hp.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('kades', kades_id=kades.id))
	elif request.method == "GET":
		form.nama.data=kades.nama
		form.masa_jabatan.data=kades.masa_jabatan
		form.no_hp.data=kades.no_hp
	return render_template ('adminku/create_kades.html', title="Update", form=form, legend='Update Data Susunan Keapala Desa')

# ========================================ADMINISTRASI DESA========================================
@app.route("/administrasi/desa")
@login_required
def administrasidesa():
	admindesas = AdminDesa.query.all()
	return render_template("adminku/admindesa.html", title='Administrasi Desa', admindesas=admindesas)

@app.route("/delete/administrasi/desa/<id>", methods=['GET'])
@login_required
def delete_admindesa(id):
	admindesa = AdminDesa.query.get(id)
	db.session.delete(admindesa)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('administrasidesa'))

@app.route("/create/administrasi/desa", methods=['GET','POST'])
@login_required
def create_admindesa():
	form=AdminDesa_F()
	if form.validate_on_submit():
		admindesa = AdminDesa(alamat=form.alamat.data, no_hp=form.no_hp.data, email=form.email.data)
		db.session.add(admindesa)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('administrasidesa'))
	return render_template("adminku/create_admindesa.html", title='Create Data Administrasi Desa', form=form, legend='Data Administrasi Desa')

@app.route("/data/administrasi/desa/<int:admindesa_id>/update", methods=['GET','POST'])
@login_required
def update_admindesa(admindesa_id):
	admindesa = AdminDesa.query.get(admindesa_id)
	form=AdminDesa_F()
	if form.validate_on_submit():
		admindesa.alamat=form.alamat.data
		admindesa.no_hp=form.no_hp.data
		admindesa.email=form.email.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('administrasidesa', admindesa_id=admindesa.id))
	elif request.method == "GET":
		form.alamat.data=admindesa.alamat
		form.no_hp.data=admindesa.no_hp
		form.email.data=admindesa.email
	return render_template ('adminku/create_admindesa.html', title="Update", form=form, legend='Update Data Administrasi Desa')

# ========================================UMUM========================================
@app.route("/umum")
@login_required
def umum():
	umums = Umum.query.all()
	return render_template("adminku/umum.html", title='Umum', umums=umums)

@app.route("/delete/umum/<id>", methods=['GET'])
@login_required
def delete_umum(id):
	umum = Umum.query.get(id)
	db.session.delete(umum)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('umum'))

@app.route("/create/umum", methods=['GET','POST'])
@login_required
def create_umum():
	form=Umum_F()
	if form.validate_on_submit():
		umum = Umum(luas_desa=form.luas_desa.data, jumlah_dusun=form.jumlah_dusun.data, utara=form.utara.data, selatan=form.selatan.data, barat=form.barat.data, timur=form.timur.data, jarak_dari_kec=form.jarak_dari_kec.data, jarak_dari_kab=form.jarak_dari_kab.data, jarak_dari_prov=form.jarak_dari_prov.data)
		db.session.add(umum)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('umum'))
	return render_template("adminku/create_umum.html", title='Create Data Umum', form=form, legend='Data Umum')

@app.route("/data/umum/<int:umum_id>/update", methods=['GET','POST'])
@login_required
def update_umum(umum_id):
	umum = Umum.query.get(umum_id)
	form=Umum_F()
	if form.validate_on_submit():
		umum.luas_desa=form.luas_desa.data
		umum.jumlah_dusun=form.jumlah_dusun.data
		umum.utara=form.utara.data
		umum.selatan=form.selatan.data
		umum.barat=form.barat.data
		umum.timur=form.timur.data
		umum.jarak_dari_kec=form.jarak_dari_kec.data
		umum.jarak_dari_kab=form.jarak_dari_kab.data
		umum.jarak_dari_prov=form.jarak_dari_prov.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('umum', umum_id=umum.id))
	elif request.method == "GET":
		form.luas_desa.data=umum.luas_desa
		form.jumlah_dusun.data=umum.jumlah_dusun
		form.utara.data=umum.utara
		form.selatan.data=umum.selatan
		form.barat.data=umum.barat
		form.timur.data=umum.timur
		form.jarak_dari_kec.data=umum.jarak_dari_kec
		form.jarak_dari_kab.data=umum.jarak_dari_kab
		form.jarak_dari_prov.data=umum.jarak_dari_prov
	return render_template ('adminku/create_umum.html', title="Update", form=form, legend='Update Data Umum')

# ========================================PENDUDUK========================================
@app.route("/penduduk/desa")
@login_required
def penduduk():
	penduduks = Penduduk.query.all()
	return render_template("adminku/penduduk.html", title='Penduduk', penduduks=penduduks)

@app.route("/delete/penduduk/<id>", methods=['GET'])
@login_required
def delete_penduduk(id):
	penduduk = Penduduk.query.get(id)
	db.session.delete(penduduk)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('penduduk'))

@app.route("/create/penduduk", methods=['GET','POST'])
@login_required
def create_penduduk():
	form=Penduduk_F()
	if form.validate_on_submit():
		penduduk = Penduduk(jumlah_l=form.jumlah_l.data, jumlah_p=form.jumlah_p.data, total=form.total.data, kk=form.kk.data, tahun=form.tahun.data)
		db.session.add(penduduk)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('penduduk'))
	return render_template("adminku/create_penduduk.html", title='Create Data Penduduk', form=form, legend='Data Penduduk')

@app.route("/data/penduduk/<int:penduduk_id>/update", methods=['GET','POST'])
@login_required
def update_penduduk(penduduk_id):
	penduduk = Penduduk.query.get(penduduk_id)
	form=Penduduk_F()
	if form.validate_on_submit():
		penduduk.jumlah_l=form.jumlah_l.data
		penduduk.jumlah_p=form.jumlah_p.data
		penduduk.total=form.total.data
		penduduk.kk=form.kk.data
		penduduk.tahun=form.tahun.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('penduduk', penduduk_id=penduduk.id))
	elif request.method == "GET":
		form.jumlah_l.data=penduduk.jumlah_l
		form.jumlah_p.data=penduduk.jumlah_p
		form.total.data=penduduk.total
		form.kk.data=penduduk.kk
		form.tahun.data=penduduk.tahun
	return render_template ('adminku/create_penduduk.html', tittle="Update", form=form, legend='Update Data Penduduk')

# ========================================SARANA PENUNJANG========================================
@app.route("/sarana/penunjang")
@login_required
def saranapenunjang():
	saranapenunjangs = SaranaPenunjang.query.all()
	return render_template("adminku/saranapenunjang.html", title='Sarana Penunjang', saranapenunjangs=saranapenunjangs)

@app.route("/delete/sarana/penunjang/<id>", methods=['GET'])
@login_required
def delete_saranapenunjang(id):
	saranapenunjang = SaranaPenunjang.query.get(id)
	db.session.delete(saranapenunjang)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('saranapenunjang'))

@app.route("/create/sarana/penunjang/desa", methods=['GET','POST'])
@login_required
def create_saranapenunjang():
	form=SaranaPenunjang_F()
	if form.validate_on_submit():
		saranapenunjang = SaranaPenunjang(paud=form.paud.data, tk=form.tk.data, sd=form.sd.data, smp=form.smp.data, sma=form.sma.data, tpa=form.tpa.data, puskesmas=form.puskesmas.data, posyandu=form.posyandu.data)
		db.session.add(saranapenunjang)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('saranapenunjang'))
	return render_template("adminku/create_saranapenunjang.html", title='Create Data Sarana Penunjang', form=form, legend='Data Sarana Penunjang')

@app.route("/data/sarana/penunjang/<int:saranapenunjang_id>/update", methods=['GET','POST'])
@login_required
def update_saranapenunjang(saranapenunjang_id):
	saranapenunjang = SaranaPenunjang.query.get(saranapenunjang_id)
	form=SaranaPenunjang_F()
	if form.validate_on_submit():
		saranapenunjang.paud=form.paud.data
		saranapenunjang.tk=form.tk.data
		saranapenunjang.sd=form.sd.data
		saranapenunjang.smp=form.smp.data
		saranapenunjang.sma=form.sma.data
		saranapenunjang.tpa=form.tpa.data
		saranapenunjang.puskesmas=form.puskesmas.data
		saranapenunjang.posyandu=form.posyandu.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('saranapenunjang', saranapenunjang_id=saranapenunjang.id))
	elif request.method == "GET":
		form.paud.data=saranapenunjang.paud
		form.tk.data=saranapenunjang.tk
		form.sd.data=saranapenunjang.sd
		form.smp.data=saranapenunjang.smp
		form.sma.data=saranapenunjang.sma
		form.tpa.data=saranapenunjang.tpa
		form.puskesmas.data=saranapenunjang.puskesmas
		form.posyandu.data=saranapenunjang.posyandu
	return render_template ('adminku/create_saranapenunjang.html', title="Update", form=form, legend='Update Data Sarana Penunjang')

# ========================================ANGGARAN DESA========================================
@app.route("/anggaran/desa")
@login_required
def anggarandesa():
	anggarandesas = AnggaranDesa.query.all()
	return render_template("adminku/anggarandesa.html", title='Anggaran Desa', anggarandesas=anggarandesas)

@app.route("/delete/anggarandesa/<id>", methods=['GET'])
@login_required
def delete_anggarandesa(id):
	anggarandesa = AnggaranDesa.query.get(id)
	db.session.delete(anggarandesa)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('anggarandesa'))

@app.route("/create/anggarandesa", methods=['GET','POST'])
@login_required
def create_anggarandesa():
	form=AnggaranDesa_F()
	if form.validate_on_submit():
		anggarandesa = AnggaranDesa(tahun=form.tahun.data, add=form.add.data, dd=form.dd.data)
		db.session.add(anggarandesa)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('anggarandesa'))
	return render_template("adminku/create_anggarandesa.html", title='Create Data Anggaran Desa', form=form, legend='Data Anggaran Desa')

@app.route("/data/anggarandesa/<int:anggarandesa_id>/update", methods=['GET','POST'])
@login_required
def update_anggarandesa(angarandesa_id):
	anggarandesa = Anggarandesa.query.get(anggarandesa_id)
	form=AnggaranDesa_F()
	if form.validate_on_submit():
		anggarandesa.tahun=form.tahun.data
		anggarandesa.add=form.add.data
		anggarandesa.dd=form.dd.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('anggarandesa', anggarandesa_id=anggarandesa.id))
	elif request.method == "GET":
		form.tahun.data=anggarandesa.tahun
		form.add.data=anggarandesa.add
		form.dd.data=anggarandesa.dd
	return render_template ('adminku/create_anggarandesa.html', tittle="Update", form=form, legend='Update Data Anggaran Desa')

# ========================================PENGURUS BUMDES========================================
@app.route("/pengurusbumdes")
@login_required
def pengurusbumdes():
	pengurusbumdess = PengurusBumdes.query.all()
	return render_template("adminku/pengurusbumdes.html", title='Pengurus Bumdes', pengurusbumdess=pengurusbumdess)

@app.route("/delete/pengurusbumdes/<id>", methods=['GET'])
@login_required
def delete_pengurusbumdes(id):
	pengurusbumdes = PengurusBumdes.query.get(id)
	db.session.delete(pengurusbumdes)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('pengurusbumdes'))

@app.route("/create/pengurusbumdes", methods=['GET','POST'])
@login_required
def create_pengurusbumdes():
	form=PengurusBumdes_F()
	if form.validate_on_submit():
		pengurusbumdes = PengurusBumdes(nama_pengurus=form.nama_pengurus.data, masa_jabatan_pengurus=form.masa_jabatan_pengurus.data, no_hp_pengurus=form.no_hp_pengurus.data)
		db.session.add(pengurusbumdes)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('pengurusbumdes'))
	return render_template("adminku/create_pengurusbumdes.html", title='Create Data Pengurus Bumdes', form=form, legend='Data Pengurus Bumdes')

@app.route("/data/pengurusbumdes/<int:pengurus_id>/update", methods=['GET','POST'])
@login_required
def update_pengurusbumdes(pengurus_id):
	pengurus = PengurusBumdes.query.get(pengurus_id)
	form=PengurusBumdes_F()
	if form.validate_on_submit():
		pengurus.nama_pengurus=form.nama_pengurus.data
		pengurus.masa_jabatan_pengurus=form.masa_jabatan_pengurus.data
		pengurus.no_hp_pengurus=form.no_hp_pengurus.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('pengurusbumdes', pengurus_id=pengurus.id))
	elif request.method == "GET":
		form.nama_pengurus.data=pengurus.nama_pengurus
		form.masa_jabatan_pengurus.data=pengurus.masa_jabatan_pengurus
		form.no_hp_pengurus.data=pengurus.no_hp_pengurus
	return render_template ('adminku/create_pengurusbumdes.html', title="Update", form=form, legend='Update Data Pengurus Bumdes')

# ========================================ADMINISTRASI BUMDES========================================
@app.route("/administrasi/bumdes")
@login_required
def adminbumdes():
	adminbumdess= AdminBumdes.query.all()
	return render_template("adminku/adminbumdes.html", title='Administrasi Bumdes', adminbumdess=adminbumdess)

@app.route("/delete/administrasi/bumdes/<id>", methods=['GET'])
@login_required
def delete_adminbumdes(id):
	adminbumdes= AdminBumdes.query.get(id)
	db.session.delete(adminbumdes)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('adminbumdes'))

@app.route("/create/administrasi/bumdes", methods=['GET','POST'])
@login_required
def create_adminbumdes():
	form=AdminBumdes_F()
	if form.validate_on_submit():
		adminbumdes = AdminBumdes(nama_bumdes=form.nama_bumdes.data, alamat_bumdes=form.alamat_bumdes.data, no_hp_bumdes=form.no_hp_bumdes.data, email_bumdes=form.email_bumdes.data)
		db.session.add(adminbumdes)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('adminbumdes'))
	return render_template("adminku/create_adminbumdes.html", title='Create Data Administrasi BUMDES', form=form, legend='Data Administrasi BUMDES')

@app.route("/data/adminbumdes/<int:admin_id>/update", methods=['GET','POST'])
@login_required
def update_adminbumdes(admin_id):
	admin = AdminBumdes.query.get(admin_id)
	form=AdminBumdes_F()
	if form.validate_on_submit():
		admin.nama_bumdes=form.nama_bumdes.data
		admin.alamat_bumdes=form.alamat_bumdes.data
		admin.no_hp_bumdes=form.no_hp_bumdes.data
		admin.email_bumdes=form.email_bumdes.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('adminbumdes', admin_id=admin.id))
	elif request.method == "GET":
		form.nama_bumdes.data=admin.nama_bumdes
		form.alamat_bumdes.data=admin.alamat_bumdes
		form.no_hp_bumdes.data=admin.no_hp_bumdes
		form.email_bumdes.data=admin.email_bumdes
	return render_template ('adminku/create_adminbumdes.html', title="Update", form=form, legend='Update Data Administrasi BUMDES')

# ========================================UNIT USAHA========================================
@app.route("/unit/usaha")
@login_required
def unitusaha():
	unitusahas= UnitUsaha.query.all()
	return render_template("adminku/unitusaha.html", title='Unit Usaha', unitusahas=unitusahas)

@app.route("/delete/unit/usaha/<id>", methods=['GET'])
@login_required
def delete_unitusaha(id):
	unitusaha= UnitUsaha.query.get(id)
	db.session.delete(unitusaha)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('unitusaha'))

@app.route("/create/unit/usaha", methods=['GET','POST'])
@login_required
def create_unitusaha():
	form=UnitUsaha_F()
	if form.validate_on_submit():
		unitusaha = UnitUsaha(nama_unit_usaha=form.nama_unit_usaha.data)
		db.session.add(unitusaha)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('unitusaha'))
	return render_template("adminku/create_unitusaha.html", title='Create Data Unit Usaha', form=form, legend='Unit Usaha')

@app.route("/data/unitusaha/<int:unit_id>/update", methods=['GET','POST'])
@login_required
def update_unitusaha(unit_id):
	unit = UnitUsaha.query.get(unit_id)
	form=UnitUsaha_F()
	if form.validate_on_submit():
		unit.nama_unit_usaha=form.nama_unit_usaha.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('unitusaha',unit_id=unit.id))
	elif request.method == "GET":
		form.nama_unit_usaha.data=unit.nama_unit_usaha
	return render_template ('adminku/create_unitusaha.html', title="Update", form=form, legend='Update Data Unit Usaha')

# ========================================KEUANGAN BUMDES========================================
@app.route("/keuangan/bumdes")
@login_required
def keuanganbumdes():
	keuanganbumdess = KeuanganBumdes.query.all()
	return render_template("adminku/keuanganbumdes.html", title='Keuangan BUMDES', keuanganbumdess=keuanganbumdess)

@app.route("/delete/keuangan/bumdes/<id>", methods=['GET'])
@login_required
def delete_keuanganbumdes(id):
	keuanganbumdes= KeuanganBumdes.query.get(id)
	db.session.delete(keuanganbumdes)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('keuanganbumdes'))

@app.route("/create/keuangan/bumdes", methods=['GET','POST'])
@login_required
def create_keuanganbumdes():
	form=KeuanganBumdes_F()
	if form.validate_on_submit():
		keuanganbumdes = KeuanganBumdes(penyertaan_modal=form.penyertaan_modal.data, penambahan_modal=form.penambahan_modal.data)
		db.session.add(keuanganbumdes)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('keuanganbumdes'))
	return render_template("adminku/create_keuanganbumdes.html", title='Create Data Keuangan BUMDES', form=form, legend='Keuangan BUMDES')

@app.route("/data/keuangan/bumdes/<int:uang_id>/update", methods=['GET','POST'])
@login_required
def update_keuanganbumdes(uang_id):
	uang = KeuanganBumdes.query.get(uang_id)
	form=KeuanganBumdes_F()
	if form.validate_on_submit():
		uang.penyertaan_modal=form.penyertaan_modal.data
		uang.penambahan_modal=form.penambahan_modal.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('keuanganbumdes', uang_id=uang.id))
	elif request.method == "GET":
		form.penyertaan_modal.data=uang.penyertaan_modal
		form.penambahan_modal.data=uang.penambahan_modal
	return render_template ('adminku/create_keuanganbumdes.html', title="Update", form=form, legend='Update Data Keuangan BUMDES')

# =======================================GAMBAR STRUKTUR KEPEMIMPINAN=========================================
@app.route("/struktur/kepemimpinan")
@login_required
def gambar():
	gambars=Gambar.query.all()
	return render_template("adminku/gambar.html", title='Upload Gambar', gambars=gambars)

@app.route("/delete/struktur/<id>", methods=['GET'])
def delete_gambar(id):
	gambar = Gambar.query.get(id)
	db.session.delete(gambar)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('gambar'))

def simpan_gambar(form_gambar):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_gambar.filename)
	nama_gambar = random_hex + f_ext
	path_gambar = os.path.join(app.root_path, 'static/foto', nama_gambar)
	form_gambar.save(path_gambar)

	output_size =(600,600)
	j = Image.open(form_gambar)
	j.thumbnail(output_size)
	j.save(path_gambar)
	return nama_gambar

@app.route("/create/struktur", methods=['GET','POST'])
@login_required
def create_gambar():
	form=Gambar_F()
	if form.validate_on_submit():
		file_gambar = simpan_gambar(form.foto_struktur.data)
		gambar = Gambar(foto_struktur=file_gambar)
		db.session.add(gambar)
		db.session.commit()
		flash('Data berhasil ditambahkan!','success')
		return redirect(url_for('gambar'))
	return render_template("adminku/create_gambar.html", title='Create Gambar', form=form, legend='Gambar')


@app.route("/data/struktur/<int:gambar_id>/update", methods=['GET','POST'])
@login_required
def update_gambar(gambar_id):
	gambar = Gambar.query.get(gambar_id)
	form=Gambar_F()
	if form.validate_on_submit():
		gambar.foto_struktur=form.foto_struktur.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('gambar', gambar_id=gambar.id))
	elif request.method == "GET":
		form.foto_struktur.data=gambar.foto_struktur
	return render_template ('adminku/create_gambar.html', title="Update", form=form, legend='Update Data Struktur Kepemimpinan')

# =======================================GAMBAR STRUKTUR ORGANISASI=======================================
@app.route("/struktur/organisasi")
@login_required
def gambar2():
	gambar2=Gambar2.query.all()
	return render_template("adminku/gambar2.html", title='Upload Gambar', gambar2=gambar2)

@app.route("/delete/struktur/organisasi/<id>", methods=['GET'])
def delete_gambar2(id):
	gambar = Gambar2.query.get(id)
	db.session.delete(gambar)
	db.session.commit()
	flash('Data berhasil dihapus','success')
	return redirect(url_for('gambar2'))

@app.route("/create/struktur/organisasi", methods=['GET','POST'])
@login_required
def create_gambar2():
	form=Gambar2_F()
	if form.validate_on_submit():
		file_gambar = simpan_gambar(form.foto_organisasi.data)
		gambar = Gambar2(foto_organisasi=file_gambar)
		db.session.add(gambar)
		db.session.commit()
		flash('Data berhasil ditambahkan!','success')
		return redirect(url_for('gambar2'))
	return render_template("adminku/create_gambar2.html", title='Create Gambar', form=form, legend='Gambar2')


@app.route("/data/struktur/organisasi/<int:gambar_id>/update", methods=['GET','POST'])
@login_required
def update_gambar2(gambar_id):
	gambar = Gambar2.query.get(gambar_id)
	form=Gambar2_F()
	if form.validate_on_submit():
		gambar.foto_organisasi=form.foto_organisasi.data
		db.session.commit()
		flash('Data berhasil diubah','success')
		return redirect(url_for('gambar2', gambar_id=gambar.id))
	elif request.method == "GET":
		form.foto_organisasi.data=gambar.foto_organisasi
	return render_template ('adminku/create_gambar2.html', title="Update", form=form, legend='Update Data Struktur Organisasi')