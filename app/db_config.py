import psycopg2

url = "dbname='ireporter' host='localhost' port='5432' user='postgres'\
     password='root'"

test_url = "dbname='ireporter_test' host='localhost' port='5432' user='postgres' password='root'"
test_url2 = 'postgresql://localhost/ireporter_test?user=postgres&password=root'


def connection(url):
    # connect to database
    print("connecting...")
    conn = psycopg2.connect(url)
    return conn


def init_db():
    conn = connection(url)
    return conn
    

def init_test_db():
    conn = connection(test_url2)
    return conn


def create_tables(url_str=url):
    conn = psycopg2.connect(url_str)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()
    return curr


def tables():
    users = """CREATE TABLE IF NOT EXISTS users(
        user_id serial PRIMARY KEY NOT NULL,
        fname varchar(255) NOT NULL,
        lname varchar(255) NOT NULL,
        othernames varchar(255),
        email varchar(255) NOT NULL,
        phoneNumber varchar(255) NOT NULL,
        username varchar(255) NOT NULL,
        registeredOn TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        isAdmin BOOLEAN NOT NULL,
        password varchar(1000)
    )"""

    incidents = """CREATE TABLE IF NOT EXISTS incidents(
        incident_id serial PRIMARY KEY NOT NULL,
        createdOn TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        createdBy INTEGER NOT NULL,
        type varchar(50) NOT NULL,
        location varchar(1000) NOT NULL,
        status varchar(50) NOT NULL,
        comments varchar(1000)
    )"""

    queries = [users, incidents]
    return queries


if __name__ == "__main__":
    init_db()
