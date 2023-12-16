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

    def get_all_users(self):
        try:
            self.openDB()
            query = "SELECT * FROM user"
            self.cursor.execute(query)
            users = self.cursor.fetchall()

            user_list = []
            for user in users:
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'password': user[2],
                    'role': user[3]
                }
                user_list.append(user_data)

            self.closeDB()
            return user_list
        except pymysql.Error as e:
            print("Error fetching all users:", e)
            return None

    def delete_user(self, user_id):
        try:
            self.openDB()
            query = "DELETE FROM user WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            self.db.commit()
            self.closeDB()
            return True
        except pymysql.Error as e:
            print(e)
            print("Error deleting user:", e)
            return False

    

class Cafe:
    def __init__(self, id=None, foto=None, nama=None, nama_lokasi=None, Link_gmaps=None, deskripsi=None, jam_buka=None, jam_tutup=None, status=None, user_id=None, rekomendasi_user=None, fasilitas=None):
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
        self.rekomendasi_user = rekomendasi_user
        self.fasilitas = fasilitas 
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

    def insertDB(self, nama, nama_lokasi, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, user_id, fasilitas):
        try:
            self.openDB()
            sql = "INSERT INTO cafe (nama, nama_lokasi, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, user_id, fasilitas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (nama, nama_lokasi, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, user_id, fasilitas))
            self.db.commit()
            self.closeDB()
            return True
        except pymysql.Error as e:
            print("Error inserting data into cafe table:", e)
            return False

    def get_data(self):
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
                cafe.status,
                cafe.user_id,
                cafe.rekomendasi_user,
                cafe.fasilitas
            FROM
                cafe
            WHERE
                cafe.status = 1 AND cafe.rekomendasi_user = 1 
            """
            self.cursor.execute(query)
            cafe_data = self.cursor.fetchall()

            cafes = {}
            for row in cafe_data:
                cafe_id = row[0]
                if cafe_id not in cafes:
                    cafes[cafe_id] = {
                        'cafe_id': row[0],
                        'nama_cafe': row[1],
                        'nama_lokasi': row[2],
                        'Link_gmaps': row[3],
                        'deskripsi': row[4],
                        'jam_buka': row[5],
                        'jam_tutup': row[6],
                        'status': row[7],
                        'user_id': row[8],
                        'rekomendasi_user': row[9],
                        'fasilitas': row[10],
                        'menus': []  # List untuk menyimpan menu
                    }

                # Tambahkan menu ke kafe yang sesuai
                cafes[cafe_id]['menus'].append({
                    'Kategori': None,  # Sesuaikan ini dengan kolom kategori
                    'menu_nama': None,  # Sesuaikan ini dengan kolom menu_nama
                    'Harga': None  # Sesuaikan ini dengan kolom Harga
                })

            self.closeDB()
            return list(cafes.values())  # Mengembalikan daftar kafe tanpa duplikasi
        except pymysql.Error as e:
            print("Error retrieving cafe data:", e)
            return None

    def get_cafe_by_id(self, cafe_id):
        try:
            self.openDB()

            # Query untuk mengambil data cafe berdasarkan cafe_id
            query_cafe = """
                SELECT
                    cafe.id AS cafe_id,
                    cafe.nama AS nama_cafe,
                    cafe.nama_lokasi,
                    cafe.Link_gmaps,
                    cafe.deskripsi,
                    cafe.jam_buka,
                    cafe.jam_tutup,
                    cafe.status,
                    cafe.user_id,
                    cafe.rekomendasi_user,
                    cafe.fasilitas
                FROM
                    cafe
                WHERE
                    cafe.id = %s
            """
            self.cursor.execute(query_cafe, (cafe_id,))
            cafe_data = self.cursor.fetchall()

            if cafe_data:
                cafe_detail = {
                    'cafe_id': cafe_data[0][0],
                    'nama_cafe': cafe_data[0][1],
                    'nama_lokasi': cafe_data[0][2],
                    'Link_gmaps': cafe_data[0][3],
                    'deskripsi': cafe_data[0][4],
                    'jam_buka': cafe_data[0][5],
                    'jam_tutup': cafe_data[0][6],
                    'status': cafe_data[0][7],
                    'user_id': cafe_data[0][8],
                    'rekomendasi_user': cafe_data[0][9],
                    'fasilitas': cafe_data[0][10],
                    'menus': {}  # Dictionary untuk menyimpan menu
                }

                # Query untuk mengambil data menu berdasarkan cafe_id tanpa duplikasi
                query_menu = """
                    SELECT DISTINCT
                        menu.Kategori,
                        menu.Nama AS menu_nama,
                        menu.Harga
                    FROM
                        menu
                    WHERE
                        menu.cafe_id = %s
                """
                self.cursor.execute(query_menu, (cafe_id,))
                menu_data = self.cursor.fetchall()

                if menu_data:
                    for row in menu_data:
                        category = row[0]
                        menu = {
                            'menu_nama': row[1],
                            'Harga': row[2]
                        }

                        if category not in cafe_detail['menus']:
                            cafe_detail['menus'][category] = [menu]
                        else:
                            if menu not in cafe_detail['menus'][category]:
                                cafe_detail['menus'][category].append(menu)

                self.closeDB()
                return cafe_detail
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
                    GROUP_CONCAT(DISTINCT menu.Kategori) AS Kategori,
                    GROUP_CONCAT(DISTINCT menu.Nama) AS menu_nama,
                    GROUP_CONCAT(DISTINCT menu.Harga) AS Harga
                FROM
                    cafe
                LEFT JOIN menu ON cafe.id = menu.cafe_id
                WHERE
                    cafe.nama_lokasi LIKE %s
                GROUP BY
                    cafe.id
            """
            self.cursor.execute(query, ('%' + location_name + '%',))
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

        
    def insertBasicInfo(self, nama_cafe, nama_lokasi, link_gmaps):
        try:
            self.openDB()
            sql = "INSERT INTO cafe (nama, nama_lokasi, Link_gmaps) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (nama_cafe, nama_lokasi, link_gmaps))
            self.db.commit()
            self.closeDB()
            return True
        except pymysql.Error as e:
            print("Error inserting basic info into cafe table:", e)
            return False

    def get_cafe_by_user_id(self, user_id):
        try:
            self.openDB()
            query_cafe = """
                SELECT
                    cafe.id AS cafe_id,
                    cafe.nama AS nama_cafe,
                    cafe.nama_lokasi,
                    cafe.Link_gmaps,
                    cafe.deskripsi,
                    cafe.jam_buka,
                    cafe.jam_tutup,
                    cafe.status,
                    cafe.user_id,
                    cafe.rekomendasi_user,
                    cafe.fasilitas
                FROM
                    cafe
                WHERE
                    cafe.user_id = %s
            """
            self.cursor.execute(query_cafe, (user_id,))
            cafes_data = self.cursor.fetchall()

            cafes = []
            for cafe_data in cafes_data:
                cafe_detail = {
                    'cafe_id': cafe_data[0],
                    'nama_cafe': cafe_data[1],
                    'nama_lokasi': cafe_data[2],
                    'Link_gmaps': cafe_data[3],
                    'deskripsi': cafe_data[4],
                    'jam_buka': cafe_data[5],
                    'jam_tutup': cafe_data[6],
                    'status': cafe_data[7],
                    'user_id': cafe_data[8],
                    'rekomendasi_user': cafe_data[9],
                    'fasilitas': cafe_data[10],
                }
                cafes.append(cafe_detail)

            self.closeDB()
            return cafes

        except pymysql.Error as e:
            print("Error retrieving cafes data:", e)
            return None

    def get_menu_by_cafe_id(self, cafe_id):
        try:
            self.openDB()
            query_menu = """
                SELECT
                    menu.Kategori,
                    menu.Nama AS menu_nama,
                    menu.Harga
                FROM
                    menu
                WHERE
                    menu.cafe_id = %s
            """
            self.cursor.execute(query_menu, (cafe_id,))
            menu_data = self.cursor.fetchall()

            menu = {}
            for menu_item in menu_data:
                category = menu_item[0]
                menu_detail = {
                    'menu_nama': menu_item[1],
                    'Harga': menu_item[2],
                }

                if category not in menu:
                    menu[category] = [menu_detail]
                else:
                    menu[category].append(menu_detail)

            self.closeDB()
            return menu

        except pymysql.Error as e:
            print("Error retrieving menu data:", e)
            return None



    def get_all_data(self):
        try:
            self.openDB()
            query = """
                SELECT
                    cafe.id AS cafe_id,
                    cafe.foto,
                    cafe.nama,
                    cafe.Link_gmaps,
                    cafe.deskripsi,
                    cafe.jam_buka,
                    cafe.jam_tutup,
                    cafe.status,
                    cafe.user_id,
                    cafe.nama_lokasi,
                    cafe.rekomendasi_user
                FROM
                    cafe
            """
            self.cursor.execute(query)
            container = []
            data = self.cursor.fetchall()

            for row in data:
                cafe = {
                    'cafe_id': row[0],
                    'foto': row[1],
                    'nama': row[2],
                    'Link_gmaps': row[3],
                    'deskripsi': row[4],
                    'jam_buka': row[5],
                    'jam_tutup': row[6],
                    'status': row[7],
                    'user_id': row[8],
                    'nama_lokasi': row[9],
                    'rekomendasi_user': row[10]
                }
                container.append(cafe)

            self.closeDB()
            return container
        except pymysql.Error as e:
            print("Error retrieving all cafe data:", e)
            return None


    def update_cafe_by_user_id(self, user_id, cafe_id, nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, fasilitas):
        try:
            self.openDB()
            query = """
                UPDATE cafe
                SET nama = %s, Link_gmaps = %s, deskripsi = %s, jam_buka = %s, jam_tutup = %s, status = %s, nama_lokasi = %s, rekomendasi_user = %s, fasilitas = %s
                WHERE id = %s AND user_id = %s
            """
            self.cursor.execute(query, (nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, fasilitas, cafe_id, user_id))
            self.db.commit() 
            self.closeDB()
            return True
        except pymysql.Error as e:
            print("Error updating cafe data:", e)
            return False

    def add_menu(self, cafe_id, category, menu_name, price):
        try:
            self.openDB()
            query = """
                INSERT INTO menu (cafe_id, Kategori, Nama, Harga)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (cafe_id, category, menu_name, price))
            self.db.commit()
            self.closeDB()
            return True
        except pymysql.Error as e:
            print("Error adding menu:", e)
            return False



    def count_cafes_by_user_id(self, user_id):
        try:
            self.openDB()
            query_count = """
                SELECT COUNT(*) AS cafe_count
                FROM cafe
                WHERE user_id = %s
            """
            self.cursor.execute(query_count, (user_id,))
            count_data = self.cursor.fetchone()
            cafe_count = count_data[0] if count_data else 0

            self.closeDB()
            return cafe_count

        except pymysql.Error as e:
            print("Error counting cafes:", e)
            return 0

    def count_food_menus_by_cafe_id(self, cafe_id):
        try:
            self.openDB()
            query_count = """
                SELECT COUNT(*) AS food_menu_count
                FROM menu
                WHERE cafe_id = %s AND Kategori = 'makanan'
            """
            self.cursor.execute(query_count, (cafe_id,))
            count_data = self.cursor.fetchone()
            food_menu_count = count_data[0] if count_data else 0

            self.closeDB()
            return food_menu_count

        except pymysql.Error as e:
            print("Error counting food menus:", e)
            return 0

    def count_drink_menus_by_cafe_id(self, cafe_id):
        try:
            self.openDB()
            query_count = """
                SELECT COUNT(*) AS drink_menu_count
                FROM menu
                WHERE cafe_id = %s AND Kategori = 'minuman'
            """
            self.cursor.execute(query_count, (cafe_id,))
            count_data = self.cursor.fetchone()
            drink_menu_count = count_data[0] if count_data else 0

            self.closeDB()
            return drink_menu_count

        except pymysql.Error as e:
            print("Error counting drink menus:", e)
            return 0
        
    def delete_cafe_owner_by_user_id(self, user_id):
        try:
            self.openDB()
            query = "DELETE FROM user WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            self.db.commit()
            self.closeDB()
            return True
        except pymysql.Error as e:
            print("Error deleting cafe owner:", e)
            return False

    
    def get_all_data(self):
        try:
            self.openDB()
            query = """
                SELECT
                    cafe.id AS cafe_id,
                    cafe.foto,
                    cafe.nama,
                    cafe.Link_gmaps,
                    cafe.deskripsi,
                    cafe.jam_buka,
                    cafe.jam_tutup,
                    cafe.status,
                    cafe.user_id,
                    cafe.nama_lokasi,
                    cafe.rekomendasi_user,
                    cafe.fasilitas
                FROM
                    cafe
            """
            self.cursor.execute(query)
            container = []
            data = self.cursor.fetchall()

            for row in data:
                cafe = {
                    'cafe_id': row[0],
                    'foto': row[1],
                    'nama': row[2],
                    'Link_gmaps': row[3],
                    'deskripsi': row[4],
                    'jam_buka': row[5],
                    'jam_tutup': row[6],
                    'status': row[7],
                    'user_id': row[8],
                    'nama_lokasi': row[9],
                    'rekomendasi_user': row[10],
                    'fasilitas': row[11]
                }
                container.append(cafe)

            self.closeDB()
            return container
        except pymysql.Error as e:
            print("Error retrieving all cafe data:", e)
            return None

    def delete_cafe_by_id(self, cafe_id):
        try:
            self.openDB()
            
            # Periksa apakah ada catatan dalam tabel yang merujuk
            check_query = "SELECT * FROM menu WHERE cafe_id = %s"
            self.cursor.execute(check_query, (cafe_id,))
            referencing_records = self.cursor.fetchall()

            if referencing_records:
                # Jika catatan ada, hapus terlebih dahulu
                delete_referencing_query = "DELETE FROM menu WHERE cafe_id = %s"
                self.cursor.execute(delete_referencing_query, (cafe_id,))
                self.db.commit()

            # Setelah catatan terkait dihapus (atau tidak ada), lanjutkan menghapus catatan cafe
            delete_cafe_query = "DELETE FROM cafe WHERE id = %s"
            self.cursor.execute(delete_cafe_query, (cafe_id,))
            self.db.commit()
            
            self.closeDB()
            return True

        except pymysql.Error as e:
            print("Error deleting cafe:", e)
            return False


    def update_cafe(self, cafe_id, nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas):
        try:
            self.openDB()

            # Cek apakah user_id ada di tabel user sebelum melakukan update
            user_check_query = "SELECT id FROM user WHERE id = %s"
            self.cursor.execute(user_check_query, (user_id,))
            user_exists = self.cursor.fetchone()

            if user_id is None or user_exists:  
                # Jika user_id adalah NULL atau ditemukan dalam tabel user, lakukan update
                query = """
                    UPDATE cafe
                    SET nama = %s, Link_gmaps = %s, deskripsi = %s, jam_buka = %s, jam_tutup = %s, status = %s, nama_lokasi = %s, rekomendasi_user = %s, user_id = %s, fasilitas = %s
                    WHERE id = %s
                """
                self.cursor.execute(query, (nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas, cafe_id))
                self.db.commit() 
                self.closeDB()
                return True
            else:
                # Jika user_id tidak valid, atur user_id menjadi NULL dalam update
                query_null_user_id = """
                    UPDATE cafe
                    SET nama = %s, Link_gmaps = %s, deskripsi = %s, jam_buka = %s, jam_tutup = %s, status = %s, nama_lokasi = %s, rekomendasi_user = %s, user_id = NULL, fasilitas = %s
                    WHERE id = %s
                """
                self.cursor.execute(query_null_user_id, (nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, fasilitas, cafe_id))
                self.db.commit() 
                self.closeDB()
                return True

        except pymysql.Error as e:
            if self.db:
                self.db.rollback()  # Kembalikan perubahan jika terjadi kesalahan
            print("Error updating cafe data:", e)
            return False
        finally:
            self.closeDB()


    def insert_cafe(self, nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas):
        try:
            self.openDB()
            if user_id is not None:  
                # Cek apakah user_id ada di tabel user sebelum menyisipkan data
                user_check_query = "SELECT id FROM user WHERE id = %s"
                self.cursor.execute(user_check_query, (user_id,))
                user_exists = self.cursor.fetchone()

                if user_exists:  # Jika user_id ditemukan, sisipkan data dengan user_id yang valid
                    query = """
                        INSERT INTO cafe (nama, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(query, (nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas))
                    self.db.commit()
                    return True
                else:  # Jika user_id tidak ditemukan, sisipkan data dengan user_id NULL
                    query = """
                        INSERT INTO cafe (nama, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, user_id, fasilitas)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, %s)
                    """
                    self.cursor.execute(query, (nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, fasilitas))
                    self.db.commit()
                    return True
            else:
                query = """
                    INSERT INTO cafe (nama, Link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, fasilitas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, (nama, link_gmaps, deskripsi, jam_buka, jam_tutup, status, nama_lokasi, rekomendasi_user, fasilitas))
                self.db.commit()
                return True
        except pymysql.Error as e:
            print(e)
            if hasattr(self, 'db'):
                self.db.rollback()
            print("Error inserting cafe data:", e)
            return False
        finally:
            self.closeDB()



            
