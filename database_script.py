import sqlite3


def create_user_table(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255)
        );
    ''')


def create_rel_table(conn):
    cur = conn.cursor()
    cur.execute('''
          CREATE TABLE IF NOT EXISTS user_question(
              user_id INT NOT NULL,
              name VARCHAR(255) NOT NULL,
              ans_number INT NOT NULL,
              FOREIGN KEY(user_id) REFERENCES users(id)
          );
      ''')


def check_user_to_be_in_db(username):
    """Add user to database if he is new"""
    conn = sqlite3.connect('stackquestion.db')
    query = "SELECT name FROM users WHERE name = (\"%s\")" % username
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    if row is None:
        query = "INSERT INTO users(name) VALUES (\"%s\");" % username
        conn.cursor().execute(query)
        return True
    return False
