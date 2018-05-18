import sqlite3


def create_user_table():
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL PRIMARY KEY,
            name VARCHAR(255)
        );
    ''')
    conn.commit()
    conn.close()


def create_rel_table():
    """Create relation table"""
    conn = sqlite3.connect('stackquestion.db')
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
    conn.commit()
    conn.close()


def create_question_table():
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    cur.execute('''
              CREATE TABLE IF NOT EXISTS questions(
                id INT NOT NULL PRIMARY KEY
              );
          ''')
    conn.commit()
    conn.close()


def check_user_to_be_in_db(chat_id, username):
    """Add user to database if he is new"""
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    try:
        query = "INSERT INTO users(id, name) VALUES ({0}, \"{1}\");".format(
            chat_id,
            username)
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_user_id(username):
    """Get user id by username"""
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = "SELECT id FROM users WHERE name = (\"%s\");" % username
    cur.execute(query)
    answer = cur.fetchone()[0]
    conn.close()
    return answer
    

def compare_answers(user_id, question_id, answer_count):
    """Compare last answer count with new
     of the question from database
     and update it"""
    connection = sqlite3.connect('stackquestion.db')
    cursor = connection.cursor()
    query = '''SELECT ans_number FROM user_question
              WHERE user_id = {0} and
              question_id  = {1};'''.format(user_id, question_id)

    cursor.execute(query)
    answer = cursor.fetchone()[0]
    if answer == answer_count:
        return True

    query = """UPDATE user_question SET ans_number = {2}
              WHERE user_id = {0} and question_id = {1};
            """.format(user_id, question_id, answer_count)

    cursor.execute(query)
    connection.commit()
    connection.close()
    return False


def insert_into_user_question(user_id, question_id, answer_count):
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = """INSERT INTO user_question(user_id, question_id, ans_number)
                         VALUES ( {0}, {1} , {2});""".format(user_id,
                                                             question_id,
                                                             answer_count)
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception:
        return


def add_question(question_id):
    """Add question to question table"""
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = "INSERT INTO questions(id) VALUES ({0});".format(question_id)
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception:
        return


def delete_question(user_id, question_id):
    """Delete question from user_question table"""
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = '''DELETE FROM user_question
                  WHERE user_id = {0} and
                  question_id  = {1};'''.format(user_id, question_id)
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception:
        return


def get_all_user_id():
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = "SELECT id FROM users;"
    cur.execute(query)
    answer = list()
    for x in cur.fetchall():
        answer.append(x[0])
    conn.close()
    return list(answer)


def get_question_by_user_id(user_id):
    conn = sqlite3.connect('stackquestion.db')
    cur = conn.cursor()
    query = """SELECT question_id from user_question
            WHERE user_id = {};
            """.format(user_id)
    cur.execute(query)
    answer = list()
    for x in cur.fetchall():
        answer.append(x[0])
    conn.close()
    return answer


create_question_table()
create_user_table()
create_rel_table()
