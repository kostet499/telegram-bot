import sqlite3
import functools


def connection_to_database(func):
    @functools.wraps(func)
    def wrapper(*args):
        conn = sqlite3.connect('stackquestion.db')
        cur = conn.cursor()
        answer = func(conn, cur, *args)
        conn.close()
        return answer
    return wrapper


@connection_to_database
def create_user_table(conn, cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            name VARCHAR(255)
        );
    ''')
    conn.commit()


@connection_to_database
def create_rel_table(conn, cur):
    """Create relation table"""
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
    conn.commit()


@connection_to_database
def create_question_table(conn, cur):
    cur.execute('''
              CREATE TABLE IF NOT EXISTS questions(
                id INT PRIMARY KEY
              );
          ''')
    conn.commit()


@connection_to_database
def check_user_to_be_in_db(conn, cur, chat_id, username):
    """Add user to database if he is new"""
    try:
        query = "INSERT INTO users(id, name) VALUES ({0}, \"{1}\");".format(
            chat_id,
            username)
        cur.execute(query)
        conn.commit()
        return True
    except Exception:
        return False


@connection_to_database
def get_user_id(conn, cur, username):
    """Get user id by username"""
    query = "SELECT id FROM users WHERE name = (\"%s\");" % username
    cur.execute(query)
    answer = cur.fetchone()[0]
    return answer


@connection_to_database
def compare_answers(connection, cursor, user_id, question_id, answer_count):
    """Compare last answer count with new
     of the question from database
     and update it"""
    query = '''SELECT ans_number FROM user_question
            WHERE user_id = {0} AND
            question_id  = {1};'''.format(user_id, question_id)

    cursor.execute(query)
    answer = cursor.fetchone()[0]
    if answer == answer_count:
        return True

    query = """UPDATE user_question SET ans_number = {2}
            WHERE user_id = {0} AND question_id = {1};
            """.format(user_id, question_id, answer_count)

    cursor.execute(query)
    connection.commit()
    return False


@connection_to_database
def insert_into_user_question(conn, cur, user_id, question_id, ans_count):
    query = """INSERT INTO user_question(user_id, question_id, ans_number)
            VALUES ({0}, {1} , {2});""".format(user_id, question_id, ans_count)
    try:
        cur.execute(query)
        conn.commit()
    except Exception:
        return


@connection_to_database
def add_question(conn, cur, question_id):
    """Add question to question table"""
    query = "INSERT INTO questions(id) VALUES ({0});".format(question_id)
    try:
        cur.execute(query)
        conn.commit()
    except Exception:
        return


@connection_to_database
def delete_question(conn, cur, user_id, question_id):
    """Delete question from user_question table"""
    query = '''DELETE FROM user_question
            WHERE user_id = {0} AND
            question_id  = {1};'''.format(user_id, question_id)
    try:
        cur.execute(query)
        conn.commit()
    except Exception:
        return


@connection_to_database
def get_all_user_id(conn, cur):
    query = "SELECT id FROM users;"
    cur.execute(query)
    answer = list()
    for x in cur.fetchall():
        answer.append(x[0])
    return list(answer)


@connection_to_database
def get_question_by_user_id(conn, cur, user_id):
    query = """SELECT question_id FROM user_question
            WHERE user_id = {};
            """.format(user_id)
    cur.execute(query)
    answer = list()
    for x in cur.fetchall():
        answer.append(x[0])
    return answer


create_question_table()
create_user_table()
create_rel_table()
