import sqlite3

def create_user_table(conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL PRIMARY KEY,
            name VARCHAR(255)
        );
    ''')


def create_rel_table(conn):
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
    cur.execute('''
              CREATE TABLE IF NOT EXISTS questions(
                id INT NOT NULL PRIMARY KEY
              );
          ''')


def check_user_to_be_in_db(chat_id, username):
    """Add user to database if he is new"""
    query = "SELECT id FROM users WHERE id = %d;" % chat_id
    cur.execute(query)
    row = cur.fetchone()
    if row is None:
        query = "INSERT INTO users(id, name) VALUES ({0}, \"{1}\");".format(
            chat_id,
            username)
        cur.execute(query)
        conn.commit()
        return True

    return False


def get_user_id(username):
    query = "SELECT id FROM users WHERE name = (\"%s\");" % username
    return cur.execute(query).fetchone()
    

def compare_answers(user_id, question_id, answer_count):
    """Compare last answer count with new
     of the question from database
     and update it"""

    query = '''SELECT ans_number FROM user_question
              WHERE user_id = {0} and
              question_id  = {1};'''.format(user_id, question_id)

    answer = cur.execute(query).fetchone()
    if answer == answer_count:
        return True

    query = """UPDATE user_question SET ans_number = {2}
              WHERE user_id = {0} and question_id = {1};
            """.format(user_id, question_id, answer_count)

    cur.execute(query)
    conn.commit()
    return False


def insert_into_user_question(user_id, question_id, answer_count):
    query = """INSERT INTO user_question(user_id, question_id, ans_number)
                      VALUES ( {0}, {1} , {2});""".format(user_id, question_id,
                                                          answer_count)

    cur.execute(query)
    conn.commit()


def add_question(question_id):
    query = "INSERT INTO questions(id) VALUES ({0});".format(question_id)
    cur.execute(query)
    conn.commit()


def delete_question(user_id, question_id):
    query = '''DELETE FROM user_question
                  WHERE user_id = {0} and
                  question_id  = {1};'''.format(user_id, question_id)
    try:
        cur.execute(query)
        conn.commit()
    except Exception:
        pass


def get_all_user_id():
    query = "SELECT id FROM users;"
    return list(cur.execute(query).fetchall())


def get_question_by_user_id(user_id):
    query = """SELECT question_id from user_question
            WHERE user_id = {};
            """.format(user_id)
    cur.execute(query)
    answer = cur.fetchall()
    return answer


def close_database():
    conn.close()


conn = sqlite3.connect('stackquestion.db')
cur = conn.cursor()
create_question_table(conn)
create_user_table(conn)
create_rel_table(conn)
conn.commit()
