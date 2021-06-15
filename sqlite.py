import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_book_data(conn, book):
    """
    Create a new book into the books table
    :param conn:
    :param book:
    :return: book id
    """
    # sql = ''' IF NOT EXISTS (SELECT TOP 1 FROM books WHERE id = ?)
    #             BEGIN
    #                 INSERT OR REPLACE INTO books(id,title,author,first_sentence,year_published)
    #                 VALUES(?,?,?,?,?)
    #             END 
    #         '''
    sql = ''' INSERT OR REPLACE INTO books(id,title,author,first_sentence,year_published)
            VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,book)
    conn.commit()
    return cur.lastrowid

def get_all_book(conn):
    sql = ''' SELECT * FROM books '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def get_id(conn,id):
    sql = ''' SELECT * FROM books where id = ? '''
    cur = conn.cursor()
    cur.execute(sql,tuple(id))


def main():
    database = r"books.db"

    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        author text,
                                        first_sentence text,
                                        year_published text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_books_table)
    else:
        print("Error! cannot create the database connection.")
    books = [
        {'id': 0,
        'title': 'A Fire Upon the Deep',
        'author': 'Vernor Vinge',
        'first_sentence': 'The coldsleep itself was dreamless.',
        'year_published': '1992'},
        {'id': 1,
        'title': 'The Ones Who Walk Away From Omelas',
        'author': 'Ursula K. Le Guin',
        'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
        'published': '1973'},
        {'id': 2,
        'title': 'Dhalgren',
        'author': 'Samuel R. Delany',
        'first_sentence': 'to wound the autumnal city.',
        'published': '1975'}
    ]
    with conn:
        for book in books:
            print(insert_book_data(conn,tuple(book.values())))
            print(get_all_book(conn))


if __name__ == '__main__':
    main()