from flask import Flask, render_template, request, redirect, url_for, flash,session
from models import user,Cafe
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'mauygqw56287w6w7' 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

admin_username = 'admin'
admin_password = 'admin123'

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
        data = (username, password, role)
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
        if session['role'] == 'admin':
            return redirect(url_for('all_cafes'))  
        elif session['role'] == 'pemilik_cafe':
            if 'user_id' in session:
                user_id = session['user_id']
                return redirect(url_for('get_cafe_and_menu_by_user_id', user_id=user_id))
            else:
                return render_template('home_login_failed.html')  # or redirect somewhere else
        else:
            return render_template('home_login_failed.html')
    flash('Harap Login dulu', 'danger')
    return redirect(url_for('login'))

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_instance = user()
        result = user_instance.check_username_or_password(username, password) 

        if result is None:
            if username == admin_username and password == admin_password: 
                session['loggedin'] = True
                session['username'] = username
                session['role'] = 'admin'
                return redirect(url_for('loggeddin'))
            else:
                flash('Login Gagal, Cek Username atau Password Anda', 'danger')
                return redirect(url_for('login_failed'))
        else:
            session['loggedin'] = True
            session['user_id'] = result[0]
            session['username'] = result[2]
            session['role'] = result[3]

            if result[3] == 'pemilik_cafe':
                return redirect(url_for('get_cafe_and_menu_by_user_id', user_id=result[0]))
            else:
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
                status = 'Buka' 
                if cafe.insertDB(filename, nama_cafe, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi):
                    flash('Cafe information successfully uploaded')
                else:
                    flash('Failed to upload cafe information')
    return render_template('after_recomendasi.html')

@app.route('/search', methods=['GET', 'POST'])
def search_location():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cafe_instance = Cafe()
        locations = cafe_instance.search_location(search_query) 
        return render_template('search_results_login.html', locations=locations, query=search_query)
    return render_template('cafe.html')

@app.route('/search_nologin', methods=['GET', 'POST'])
def search_location_nologin():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cafe_instance = Cafe()
        locations = cafe_instance.search_location(search_query) 
        return render_template('search_results_nologin.html', locations=locations, query=search_query)
    return render_template('cafe_copy.html')

@app.route('/cafe/<int:user_id>')
def get_cafe_and_menu_by_user_id(user_id):
    if 'user_id' not in session:
        session['user_id'] = user_id
    cafe_instance = Cafe()
    cafes = cafe_instance.get_cafe_by_user_id(user_id)
    if cafes:
        cafe_id = cafes[0]['cafe_id']
        print(cafe_id)
        menu = cafe_instance.get_menu_by_cafe_id(cafe_id)
        cafe_count = cafe_instance.count_cafes_by_user_id(user_id)
        food_menu_count = cafe_instance.count_food_menus_by_cafe_id(cafe_id)
        drink_menu_count = cafe_instance.count_drink_menus_by_cafe_id(cafe_id)
        return render_template('index.html', cafes=cafes, menu=menu, cafe_count=cafe_count, food_menu_count=food_menu_count, drink_menu_count=drink_menu_count)
    else:
        return "No cafes found for this user."

@app.route('/add_cafe_owner', methods=['GET', 'POST'])
def add_cafe_owner():
    if request.method == 'GET':
        return render_template('owener_add_cafe.html')
    if request.method == 'POST':
        nama = request.form['nama']
        nama_lokasi = request.form['nama_lokasi']
        Link_gmaps = request.form['Link_gmaps']
        deskripsi = request.form['deskripsi']
        jam_buka = request.form['jam_buka']
        jam_tutup = request.form['jam_tutup']
        status = request.form['status']
        fasilitas = request.form['fasilitas']  
        user_id = session.get('user_id')  
        cafe_instance = Cafe()
        success = cafe_instance.insertDB(nama, nama_lokasi, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, user_id, fasilitas)
        if success:
            return "Data cafe berhasil ditambahkan!"
        else:
            return "Gagal menambahkan data cafe."


@app.route('/edit_cafe')
def edit_cafe():
    user_id = session.get('user_id')
    if user_id:
        cafe_instance = Cafe()
        cafes = cafe_instance.get_cafe_by_user_id(user_id)
        if cafes:
            return render_template('owener_edit_cafe.html', all_cafes=cafes)
        else:
            return "No cafes found for this user."
    else:
        return "User ID not found in session."

@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    if request.method == 'GET':
        return render_template('owener_add_menu.html')

    elif request.method == 'POST':
        cafe_id = request.form['cafe_id']
        category = request.form['category']
        menu_name = request.form['menu_name']
        price = request.form['price']
        cafe_instance = Cafe()
        success = cafe_instance.add_menu(cafe_id, category, menu_name, price)
        if success:
            flash("Menu added successfully")
        else:
            flash("Failed to add menu")
        return redirect(url_for('add_menu', cafe_id=cafe_id))


@app.route('/delete_cafe_owner', methods=['POST'])
def delete_cafe_owner():
    if 'user_id' in session:
        user_id = session['user_id']
        user_instance = Cafe()
        success = user_instance.delete_cafe_owner_by_user_id(user_id)
        if success:
            flash(f"Data cafe owner dengan user_id {user_id} berhasil dihapus.", 'success')
            return redirect(url_for('get_cafe_and_menu_by_user_id', user_id=user_id))
        else:
            flash(f"Gagal menghapus data cafe owner dengan user_id {user_id}.", 'error')
            return redirect(url_for('get_cafe_and_menu_by_user_id', user_id=user_id)) 
    else:
        print(f"user_id: {user_id}")  
        return render_template('index.html', user_id=user_id)

@app.route('/all_cafes')
def all_cafes():
    cafe_instance = Cafe()
    all_cafes = cafe_instance.get_all_data()
    print(all_cafes)  
    return render_template('admin_recomendasi_cafe.html', all_cafes=all_cafes)

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        try:
            cafe_id = request.form['id']
            nama = request.form['nama']
            link_gmaps = request.form['Link_gmaps']
            deskripsi = request.form['deskripsi']
            jam_buka = request.form['jam_buka']
            jam_tutup = request.form['jam_tutup']
            status = request.form['status']
            nama_lokasi = request.form['nama_lokasi']
            rekomendasi_user = request.form['rekomendasi_user']
            user_id = request.form['user_id']
            fasilitas = request.form['fasilitas']

            cafe_instance = Cafe()
            updated = cafe_instance.update_cafe(
                cafe_id, nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas
            )
            if updated:
                flash("Data Updated Successfully")
                return redirect(url_for('all_cafes'))
            else:
                flash("Failed to update data")
                return redirect(url_for('all_cafes'))

        except Exception as e:
            print("An error occurred during update:", str(e))
            flash("Failed to update data")
            return redirect(url_for('all_cafes'))

@app.route('/tambah_cafe', methods=['GET', 'POST'])
def tambah_cafe():
    if request.method == 'GET':
        return redirect(url_for('all_cafes'))
    elif request.method == 'POST':
        nama = request.form['nama']
        link_gmaps = request.form['Link_gmaps']
        deskripsi = request.form['deskripsi']
        jam_buka = request.form['jam_buka']
        jam_tutup = request.form['jam_tutup']
        status = request.form['status']
        nama_lokasi = request.form['nama_lokasi']
        rekomendasi_user = request.form['rekomendasi_user']
        user_id = request.form.get('user_id')
        fasilitas = request.form['fasilitas']
        cafe_model = Cafe()
        inserted = cafe_model.insert_cafe(
            nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas
        )
        if inserted:
            flash("Data Cafe Ditambahkan")
            return redirect(url_for('tambah_cafe'))
        else:
            flash("Gagal Menambahkan Data Cafe")
            return redirect(url_for('tambah_cafe'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cafe_instance = Cafe()
    if cafe_instance.delete_cafe_by_id(id_data):
        flash("Record Has Been Deleted Successfully", "success")
    else:
        flash("Failed to delete record", "danger")
    return redirect(url_for('all_cafes'))


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == 'POST':
        user_model = user()
        deleted = user_model.delete_user(user_id)
        if deleted:
            flash('Pengguna berhasil dihapus', 'success')  
        else:
            flash('Gagal menghapus pengguna', 'error')  
        return redirect(url_for('get_all_users'))
    else:
        return redirect(url_for('get_all_users',user_id=user_id))

@app.route('/users', methods=['GET'])
def get_all_users():
    user_model = user()
    all_users = user_model.get_all_users()
    if all_users:
        return render_template('admin_kelola_pengguna.html', users=all_users)
    else:
        flash('Tidak ada data pengguna', 'info') 
        return render_template('admin_kelola_pengguna.html', users=[])


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

