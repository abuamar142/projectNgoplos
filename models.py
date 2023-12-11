import pymysql
import config

db = cursor = None

class user:
    def __init__(self, username=None, password=None, role=None):
        self.username = username
        self.password = password
        self.role = role

    
    def openDB(self):
        self.db = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        self.cursor = self.db.cursor() if self.db else None


    def closeDB(self):
        self.db.close()

    def insertDB(self, data):
        self.openDB()
        username, password, role = data

        # Simpan kata sandi langsung ke database tanpa hashing
        sql = "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (username, password, role))
        self.db.commit()
        self.closeDB()

    def check_username(self, username):
        self.openDB()
        sql = "SELECT * FROM user WHERE username = %s"
        self.cursor.execute(sql, (username,))
        akun = self.cursor.fetchone()
        self.closeDB()
        return akun


    def check_username_or_password(self, username, password):
        self.openDB()
        # Bandingkan kata sandi langsung dari input pengguna dengan yang disimpan dalam database
        self.cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))
        akun = self.cursor.fetchone()
        self.closeDB()
        return akun





class Cafe:
    def __init__(self, id=None, foto=None, nama=None, nama_lokasi=None, Link_gmaps=None, deskripsi=None, jam_buka=None, jam_tutup=None, status=None, user_id=None):
        self.id = id
        self.foto = foto
        self.nama = nama
        self.nama_lokasi = nama_lokasi
        self.Link_gmaps = Link_gmaps
        self.deskripsi = deskripsi
        self.jam_buka = jam_buka
        self.jam_tutup = jam_tutup
        self.status = status
        self.user_id = user_id
        self.db = None
        self.cursor = None

    def openDB(self):
        try:
            self.db = pymysql.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME
            )
            self.cursor = self.db.cursor()
        except pymysql.Error as e:
            print("Error connecting to the database:", e)

    def closeDB(self):
        if self.db:
            self.db.close()

    def insertDB(self, foto, nama, nama_lokasi, Link_gmaps, deskripsi, jam_buka, jam_tutup, status):
        try:
            self.openDB()
            sql = "INSERT INTO cafe (foto, nama, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (foto, nama, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi))
            self.db.commit()
            self.closeDB()
            return True
        except pymysql.Error as e:
            print("Error inserting data into cafe table:", e)
            return False

    def get_data(self):
        self.openDB()
        query = """
        SELECT
            cafe.id AS cafe_id,
            cafe.nama AS nama_cafe,
            cafe.nama_lokasi,
            cafe.Link_gmaps,
            cafe.deskripsi,
            cafe.jam_buka,
            cafe.jam_tutup,
            menu.Kategori,
            menu.Nama AS menu_nama,
            menu.Harga
        FROM
            cafe
        LEFT JOIN menu ON cafe.id = menu.cafe_id
        """
        self.cursor.execute(query)
        container = []
        data = self.cursor.fetchall()

        for row in data:
            cafe = {
                'cafe_id': row[0],
                'nama_cafe': row[1],
                'nama_lokasi': row[2],
                'Link_gmaps': row[3],
                'deskripsi': row[4],
                'jam_buka': row[5],
                'jam_tutup': row[6],
                'Kategori': row[7],
                'menu_nama': row[8],
                'Harga': row[9]
            }
            container.append(cafe)

        self.closeDB()
        return container
            
    def get_cafe_by_id(self, cafe_id):
        try:
            self.openDB()
            query = """
                SELECT
                    cafe.id AS cafe_id,
                    cafe.nama AS nama_cafe,
                    cafe.nama_lokasi,
                    cafe.Link_gmaps,
                    cafe.deskripsi,
                    cafe.jam_buka,
                    cafe.jam_tutup,
                    menu.Kategori,
                    menu.Nama AS menu_nama,
                    menu.Harga
                FROM
                    cafe
                LEFT JOIN menu ON cafe.id = menu.cafe_id
                WHERE
                    cafe.id = %s
            """
            self.cursor.execute(query, (cafe_id,))
            data = self.cursor.fetchall()

            if data:
                # Ambil data kafe berdasarkan ID
                cafe_item = {
                    'cafe_id': data[0][0],
                    'nama_cafe': data[0][1],
                    'nama_lokasi': data[0][2],
                    'Link_gmaps': data[0][3],
                    'deskripsi': data[0][4],
                    'jam_buka': data[0][5],
                    'jam_tutup': data[0][6],
                    'Kategori': data[0][7],
                    'menu_nama': data[0][8],
                    'Harga': data[0][9]
                }
                self.closeDB()
                return cafe_item
            else:
                self.closeDB()
                return None
        except pymysql.Error as e:
            print("Error retrieving cafe data:", e)
            return None

            if data:
                # Ambil data kafe berdasarkan ID
                cafe_item = {
                    # Informasi cafe
                    'cafe_id': data[0][0],
                    'nama_cafe': data[0][1],
                    'nama_lokasi': data[0][2],
                    'Link_gmaps': data[0][3],
                    'deskripsi': data[0][4],
                    'jam_buka': data[0][5],
                    'jam_tutup': data[0][6],
                    # ... Informasi lainnya ...

                    # Data menu dari database
                    'menus': []  # Isi ini dengan data menu dari database
                }

                # Ambil data menu dari database berdasarkan cafe_id
                menu_query = "SELECT Nama AS menu_nama, Harga FROM menu WHERE cafe_id = %s"
                self.cursor.execute(menu_query, (cafe_id,))
                menu_data = self.cursor.fetchall()

                for row in menu_data:
                    menu = {
                        'menu_nama': row[0],
                        'Harga': row[1]
                    }
                    cafe_item['menus'].append(menu)

                self.closeDB()
                return cafe_item
            else:
                self.closeDB()
                return None
        except pymysql.Error as e:
            print("Error retrieving cafe data:", e)
            return None

    def search_location(self, location_name):
        try:
            self.openDB()
            query = """
                SELECT
                    cafe.id AS cafe_id,
                    cafe.nama AS nama_cafe,
                    cafe.nama_lokasi,
                    cafe.Link_gmaps,
                    cafe.deskripsi,
                    cafe.jam_buka,
                    cafe.jam_tutup,
                    menu.Kategori,
                    menu.Nama AS menu_nama,
                    menu.Harga
                FROM
                    cafe
                LEFT JOIN menu ON cafe.id = menu.cafe_id
                WHERE
                    cafe.nama_lokasi LIKE %s
            """
            self.cursor.execute(query, ('%' + location_name + '%',))  # Gunakan LIKE untuk pencarian substring
            container = []
            data = self.cursor.fetchall()

            for row in data:
                cafe = {
                    'cafe_id': row[0],
                    'nama_cafe': row[1],
                    'nama_lokasi': row[2],
                    'Link_gmaps': row[3],
                    'deskripsi': row[4],
                    'jam_buka': row[5],
                    'jam_tutup': row[6],
                    'Kategori': row[7],
                    'menu_nama': row[8],
                    'Harga': row[9]
                }
                container.append(cafe)

            self.closeDB()
            return container
        except pymysql.Error as e:
            print("Error retrieving cafe data:", e)
            return None
