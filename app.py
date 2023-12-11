from flask import Flask, render_template, request, redirect, url_for, flash,session
from models import user,Cafe
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'mauygqw56287w6w7' 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home_login')
def home_login():
    return render_template('home_login.html')
       
@app.route('/welcome_register')
def welcome_register():
    return render_template('after_register.html')

@app.route('/login_failed')
def login_failed():
    return render_template('login_failed.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username') 
        password = request.form.get('password')
        role = request.form.get('role')
        # Menggunakan kata sandi langsung tanpa hashing
        data = (username, password, role)
        # Cek username atau email
        user_instance = user()
        result = user_instance.check_username_or_password(username, password)
        if result is None:
            model = user()
            model.insertDB(data)
            flash('Registrasi Berhasil', 'success')
        else:
            flash('Username atau email sudah ada', 'danger')
            return render_template('registrasi_failed.html')
    return render_template('after_register.html')

@app.route('/loggeddin')
def loggeddin():
    if 'loggedin' in session:
        return render_template('home_login_failed.html')
    flash('Harap Login dulu', 'danger')
    return redirect(url_for('login'))

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_instance = user()
        result = user_instance.check_username(username)

        if result is None:
            flash('Login Gagal, Cek Username Anda', 'danger')
            return redirect(url_for('login_failed'))
        elif result[2] != password: 
            flash('Login gagal, Cek Password Anda', 'danger')
            return redirect(url_for('login_failed'))
        else:
            session['loggedin'] = True
            session['username'] = result[2]
            session['role'] = result[3]
            return redirect(url_for('loggeddin'))
    return render_template('home.html')

@app.route('/cafe_login')
def cafe_login():
    cafe_instance = Cafe() 
    cafe_data = cafe_instance.get_data()  
    return render_template('cafe.html', cafe_data=cafe_data)

@app.route('/cafe_detail/<int:cafe_id>')
def cafe_detail(cafe_id):
    cafe_instance = Cafe()
    cafe_detail = cafe_instance.get_cafe_by_id(cafe_id)
    return render_template('cafe_detail_copy.html', cafe_detail=cafe_detail)

@app.route('/cafe_detail_nologin/<int:cafe_id>')
def cafe_detail_nologin(cafe_id):
    cafe_instance = Cafe()
    cafe_detail = cafe_instance.get_cafe_by_id(cafe_id)
    return render_template('cafe_detail_copy_nologin.html', cafe_detail=cafe_detail)

@app.route('/cafe_noLogin')
def cafe_noLogin():
    cafe_instance = Cafe() 
    cafe_data = cafe_instance.get_data()  
    return render_template('cafe_copy.html', cafe_data=cafe_data)

@app.route('/dashboard')
def dashboard():
    jumlah_tempat = 9
    return render_template('dashboard.html', jumlah_tempat=jumlah_tempat)

@app.route('/add_cafe')
def add_cafe():
    return render_template('add_cafe.html')

@app.route('/cafe_owner')
def cafe_owner():
    cafe_count = 10
    owner_count = 10
    return render_template('cafe_owner.html', cafe_count=cafe_count, owner_count=owner_count)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/rekomendasi', methods=["POST", "GET"])
def rekomendasi():
    return render_template('rekomendasi.html')

@app.route("/upload_basic_info", methods=["POST"])
def upload_basic_info():
    if request.method == 'POST':
        cafe = Cafe()
        nama_cafe = request.form['cafe_nama']
        nama_lokasi = request.form['nama_lokasi']
        link_gmaps = request.form['link_gmaps']
        if cafe.insertBasicInfo(nama_cafe, nama_lokasi, link_gmaps):
            session['message'] = 'Informasi dasar cafe berhasil diunggah'
            return render_template('after_recomendasi.html')
        else:
            flash('Gagal mengunggah informasi dasar cafe')
    return redirect(url_for('rekomendasi'))

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        cafe = Cafe()
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                nama_cafe = request.form['cafe_nama']
                Link_gmaps = request.form['link_gmaps']
                deskripsi = request.form['deskripsi']
                jam_buka = request.form['jam_buka']
                jam_tutup = request.form['jam_tutup']
                nama_lokasi =  request.form['nama_lokasi']
                status = 'Buka'  # Ganti status sesuai dengan kebutuhan
                if cafe.insertDB(filename, nama_cafe, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi):
                    flash('Cafe information successfully uploaded')
                else:
                    flash('Failed to upload cafe information')
    return render_template('after_recomendasi.html')

@app.route('/search', methods=['GET', 'POST'])
def search_location():
    if request.method == 'POST':
        search_query = request.form['search_query']
        # Ganti ini dengan fungsi pencarian yang sesuai dalam class Cafe Anda
        cafe_instance = Cafe()
        locations = cafe_instance.search_location(search_query) 
        return render_template('search_results_login.html', locations=locations, query=search_query)
    return render_template('cafe.html')

@app.route('/search_nologin', methods=['GET', 'POST'])
def search_location_nologin():
    if request.method == 'POST':
        search_query = request.form['search_query']
        # Ganti ini dengan fungsi pencarian yang sesuai dalam class Cafe Anda
        cafe_instance = Cafe()
        locations = cafe_instance.search_location(search_query) 
        return render_template('search_results_nologin.html', locations=locations, query=search_query)
    return render_template('cafe_copy.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
