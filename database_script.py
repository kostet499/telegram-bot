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


def get_user_id(username):
    conn = sqlite3.connect('stackquestion.db')
    query = "SELECT id FROM users WHERE name = (\"%s\")" % username
    cur = conn.cursor()
    cur.execute(query)
    user_id = cur.fetchone()
    conn.close()
    return user_id


def compare_answers(user_id, question_id, answer_count):
    """Compare last answer count with new
     of the question from database
     and update it"""

    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()

    query = '''SELECT ans_number FROM user_question
              WHERE user_id = %d and
              question_id  = %d ''' % (user_id, question_id)

    answer = cur.execute(query).fetchone()
    if answer is not None and answer == answer_count:
        return True
    if answer is None:
        query = """INSERT INTO user_question(user_id, question_id, ans_number)
                  VALUES ( %d, %d , %d);""" \
                % (user_id, question_id, answer_count)
    else:
        query = """UPDATE user_question SET ans_number = %d
                      WHERE user_id = %d and question_id = %d
                   """ % (user_id, question_id, answer_count)

    cur.execute(query)
    conn.commit()
    conn.close()
    return False


def add_question(question_id):
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = "INSERT INTO questions(id) VALUES (%d)" % question_id
    try:
        cur.execute(query)
        conn.commit()
    except Exception:
        pass
    conn.close()


def delete_question(user_id, question_id):
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()

    query = '''DELETE FROM user_question
                  WHERE user_id = %d and
                  question_id  = %d ''' % (user_id, question_id)
    try:
        cur.execute(query)
        conn.commit()
    except Exception:
        conn.close()


def get_all_user_names():
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()

    query = "SELECT name FROM users"
    answer = list(cur.execute(query).fetchall())
    conn.close()
    return answer


def get_question_by_user_id(user_id):
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()

    query = """SELECT question_id from user_question
            WHERE user_id = %d
            """ % user_id
    answer = set(cur.execute(query).fetchall())
    conn.close()
    return answer


conn = sqlite3.connect('stackquestion.db')
create_question_table(conn)
create_user_table(conn)
create_rel_table(conn)
conn.commit()
conn.close()
