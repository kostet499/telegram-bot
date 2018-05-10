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
              question_id INT NOT NULL,
              ans_number INT NOT NULL,
              FOREIGN KEY(user_id) REFERENCES users(id),
              FOREIGN KEY(question_id) REFERENCES questions(id),
              PRIMARY KEY(user_id, question_id)
              );
      ''')


def create_question_table(conn):
    cur = conn.cursor()
    cur.execute('''
              CREATE TABLE IF NOT EXISTS questions(
                id INTEGER NOT NULL PRIMARY KEY
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
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def extract_last_answer_count(user_id, question_id):
    """Extract last answer count of the question from database """
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()

    query = '''SELECT ans_number FROM users
              WHERE user_id = (\"%s\") and
              question_id  =(\"%s\") ''' % (user_id, question_id)

    answer = cur.execute(query).fetchone()
    if answer is None:
        answer = 0
    conn.close()
    return answer


conn = sqlite3.connect('stackquestion.db')
create_question_table(conn)
create_user_table(conn)
create_rel_table(conn)
conn.commit()
conn.close()
