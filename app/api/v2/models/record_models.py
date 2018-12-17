from app.db_config import connection, url, init_db
from psycopg2.extras import RealDictCursor


class RaiseRedFlagModel():

    def __init__(self):
        self.conn = init_db()
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)

    def save(self, user_id, type, location, status, comments):

        payload = {            
            "createdBy": user_id,
            "type": type,
            "location": location,
            "status": status,
            "comments": comments
        }
        query = """INSERT INTO incidents(createdBy, type, location, status, comments) VALUES('{0}', '{1}', '{2}', '{3}', '{4}');""".format(payload["createdBy"], payload['type'], payload['location'], payload['status'], payload['comments'])
        self.curr.execute(query)
        self.conn.commit()

    def get_redFlag(self, user):
        query = '''SELECT * FROM incidents WHERE createdby=%s'''
        curr = self.curr
        curr.execute(query, (user,))
        records = curr.fetchall()
        if not records:
            return None
        return records
    
    def get_record_by_id(self, id):
        query = """SELECT * FROM incidents WHERE incident_id=%s"""
        curr = self.curr
        curr.execute(query, (id,))
        record = curr.fetchone()
        if not record:
            return None
        return record

    def del_record(self, id):
        query = """DELETE FROM incidents  where incident_id=%s"""
        curr = self.curr
        curr.execute(query, (id,))
        self.conn.commit()

    @staticmethod
    def check_record(records):
        result = []
        if not records:
            return {
                'message': 'No record(s) found'
            }
        for record in records:
            record['createdon'] = record['createdon'].strftime('%A %d. %B %Y')
            result.append(record)
        return result

    def find(self, id, user):
        query = '''SELECT * FROM incidents where incident_id= %s AND createdby=%s'''
        curr = self.curr
        curr.execute(query, (id, user,))
        record = curr.fetchall()
        return record

    def update_location(self, location, id):
        query = """UPDATE incidents SET location=%s WHERE  incident_id=%s"""
        curr = self.curr
        curr.execute(query, (location, id,))
        self.conn.commit()

    def update_comment(self, comment, id):
        query = """UPDATE incidents SET comments=%s WHERE  incident_id=%s"""
        curr = self.curr
        curr.execute(query, (comment, id,))
        self.conn.commit()

    def update_status(self, status, id):
        query = """UPDATE incidents SET status=%s WHERE  incident_id=%s"""
        curr = self.curr
        curr.execute(query, (status, id,))
        self.conn.commit()

    def check_isAdmin(self, current_user):
        query = """SELECT isadmin FROM users WHERE username=%s"""
        curr = self.curr
        curr.execute(query, (current_user,))
        user = curr.fetchone()
        return user
        