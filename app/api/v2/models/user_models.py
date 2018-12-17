from app.db_config import connection, url, init_db
from psycopg2.extras import RealDictCursor


class UserModel():

    def __init__(self):
        self.conn = init_db()
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)
        self.isAdmin = False

    def save(self, firstname, lastname, othernames, email, phoneNumber, username, password):

        payload = {
            'firstname': firstname,
            'lastname': lastname,
            'othernames': othernames,
            'email': email,
            'phoneNumber': phoneNumber,
            'username': username,
            'isAdmin': self.isAdmin,
            'password': password
        }
        query = """INSERT INTO users(fname, lname, othernames, email, phoneNumber, username, isAdmin, password)
                VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');""".format(payload['firstname'], payload['lastname'], payload['othernames'], payload['email'], payload['phoneNumber'], payload['username'], payload['isAdmin'], payload['password'])
        self.curr.execute(query)
        self.conn.commit()

    def get_username(self, username):
        query = """SELECT username FROM users WHERE username='{0}'""".format(username)
        curr = self.curr
        curr.execute(query)
        get_username = curr.fetchone()

        if get_username:
            return get_username
        return None

    def get_passw(self, username):
            query = """SELECT * FROM users WHERE username='{0}'""".format(username)
            curr = self.curr
            curr.execute(query)
            get_pass = curr.fetchone()
            if get_pass:
                return get_pass
            return None

    def get_user(self, username):
        query = """SELECT * FROM users WHERE username='{0}'""".format(username)
        curr = self.curr
        curr.execute(query)
        get_username = curr.fetchone()

        if get_username:
            return get_username
        return None
        
    def get_email(self, email):
        query = """SELECT email FROM users WHERE email='{0}'""".format(email)
        curr = self.curr
        curr.execute(query)
        get_username = curr.fetchone()

        if get_username:
            return get_username
        return None
