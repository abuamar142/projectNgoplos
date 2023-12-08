from flask import Flask, render_template, request, redirect, url_for, flash,session
from models import user
import hashlib

app = Flask(__name__)
app.secret_key = 'mauygqw56287w6w7' 


        
@app.route('/welcome_register')
def welcome_register():
    return render_template('after_register.html')

@app.route('/login_failed')
def login_failed():
    return render_template('login_failed.html')

@app.route('/')
def index():
    return render_template('Home.html')



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('home.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Melakukan hashing pada password sebelum disimpan
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        data = (username, hashed_password, role)
        model = user()
        model.insertDB(data)

        # Setelah pendaftaran sukses, simpan username ke dalam sesi
        session['username'] = username
        
        return redirect(url_for('welcome_register'))


@app.route('/cafe_login')
def cafe_login():
    return render_template('Cafe.html')

@app.route('/loginn', methods=['GET', 'POST'])
def loginn():
    if 'username' in session:
        username = session['username']
        return render_template('cafe.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_instance = user(username, password) 

        if user_instance.authenticate():
            session['username'] = username
            return redirect(url_for('loginn'))
        return render_template('login_failed.html')

    return render_template('Home.html')




@app.route('/cafe_noLogin')
def cafe_noLogin():
    return render_template('Cafe copy.html')

@app.route('/rekomendasi')
def contact():
    return render_template('rekomendasi.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





