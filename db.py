import sqlite3
import bcrypt

# Database class to be instanced within the GUI app


class chatDB():
    # Creating connections with DB as well as creating tables if doesn't exist
    def __init__(self):
        self.conn = sqlite3.connect('chat_app_db.db')
        self.create_db_tables()

    # opening cursor connection
    def open_cursor_connection(self):
        self.cur = self.conn.cursor()

    # closing cursor connection
    def close_cursor_connection(self):
        self.cur.close()

    # used in the __init__ to create tables if doesn't exist
    def create_db_tables(self):
        self.open_cursor_connection()
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS users (id integer primary key,firstname text, lastname text, username text, password text)
            ''')
        except sqlite3.Error as error:
            print('SQLite error: %s' % (' '.join(error.args)))
        finally:
            self.conn.commit()
            self.close_cursor_connection()

    # Inserting User in DB
    # checking iif username used already though self.user_exists(arg:username)
    # hashing password using bcrypt
    def insert_user_db(self, firstname, lastname, username, password):
        if self.user_exists(username) == None:
            hashed_password = bcrypt.hashpw(
                password.strip().encode('utf-8'), bcrypt.gensalt())
            self.open_cursor_connection()
            try:
                self.cur.execute('''
                    INSERT INTO users (firstname, lastname, username, password) values (?,?,?,?) 
                ''', (firstname.lower().strip(), lastname.lower().strip(), username.lower().strip(), hashed_password))

            except sqlite3.Error as error:
                print('SQLite error: %s' % (' '.join(error.args)))
            finally:
                self.conn.commit()
                self.close_cursor_connection()
            print('user added to DB')
            return True

        else:
            print('user already exists')
            return False

    # loading user from DB matching both username & password
    # returning bool
    # TODO: return user object to be used in the GUI App
    def retrieve_user_db(self, username, password):
        self.open_cursor_connection()
        try:
            user_cur = self.cur.execute('''
                select * from users where username=?
            ''', (username.lower().strip(),))
            user = user_cur.fetchone()
        except sqlite3.Error as error:
            print('SQLite error: %s' % (' '.join(error.args)))

        if user:
            match = bcrypt.checkpw(password.strip().encode('utf-8'), user[4])
            if match:
                print('all good to login')
                return user
            else:
                print('password not matching')
                return None
        else:
            print('User not found')
            return None

    # checking if username used already
    def user_exists(self, username):
        self.open_cursor_connection()
        try:
            user_cur = self.cur.execute('''
                SELECT * from users where username=? 
            ''', (username.lower().strip(),))
            user = user_cur.fetchone()
        except sqlite3.Error as error:
            print('SQLite error: %s' % (' '.join(error.args)))
        finally:
            self.close_cursor_connection()
        return user
