import pymysql
import config
import hashlib

db = cursor = None

class user:
    def __init__(self, username=None, password=None, role=None):
        self.username =username
        self.password = password
        self.role = role

    
    def openDB(self):
        self.db = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        self.cursor = self.db.cursor()

    def closeDB(self):
        self.db.close()

    def insertDB(self, data):
        self.openDB()
        username, password, role = data

        # Melakukan hashing pada password sebelum disimpan
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        sql = "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (username, hashed_password, role))
        self.db.commit()
        self.closeDB()

    def authenticate(self):
        try:
            self.openDB()
            hashed_password = hashlib.sha256(self.password.encode()).hexdigest()
            cursor.execute("SELECT COUNT(*) FROM user WHERE username = %s AND password = %s", (self.username, hashed_password))
            count_account = cursor.fetchone()[0]
            self.closeDB()
            return True if count_account > 0 else False
        except Exception as e:
            print("Authentication error:", str(e))
            return False