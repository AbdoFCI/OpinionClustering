from configparser import ConfigParser
from mysql.connector import Error, MySQLConnection
from  Entities import Opinion

def read_db_config(file_name='Data_manipulation\\config.ini', section='mysql'):
    """Read database configuration file and return a dictionary object"""

    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(file_name)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, file_name))

    return db


# def query_with_fetchone():
#     try:
#         dbconfig = read_db_config()
#         conn = MySQLConnection(**dbconfig)
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM books")
#
#         row = cursor.fetchone()
#
#         while row is not None:
#             print(row)
#             row = cursor.fetchone()
#
#     except Error as e:
#         print(e)
#
#     finally:
#         cursor.close()
#         conn.close()
#     return
#
#
# def query_with_fetchall():
#     rows = []
#     try:
#         dbconfig = read_db_config()
#         conn = MySQLConnection(**dbconfig)
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM books")
#         rows = cursor.fetchall()
#         print('Total Row(s):', cursor.rowcount)
#         for row in rows:
#             print(row)
#     except Error as e:
#         print(e)
#         return None
#     finally:
#         cursor.close()
#         conn.close()
#     return rows
#
#
# def insert_book(title, isbn):
#
#     query = "INSERT INTO books(title,isbn) VALUES({},{})".format("car",1234)
#     try:
#         db_config = read_db_config()
#         conn = MySQLConnection(**db_config)
#         cursor = conn.cursor()
#         cursor.execute(query)
#
#         conn.commit()
#     except Error as error:
#         print(error)
#     finally:
#         cursor.close()
#         conn.close()
#     return
#
#
# def delete_book(book_id):
#
#     db_config = read_db_config()
#
#     query = "DELETE FROM books WHERE id = %s"
#
#     try:
#         # connect to the database server
#         conn = MySQLConnection(**db_config)
#
#         # execute the query
#         cursor = conn.cursor()
#         cursor.execute(query, (book_id,))
#
#         # accept the change
#         conn.commit()
#
#     except Error as error:
#         print(error)
#
#     finally:
#         cursor.close()
#         conn.close()
#     return


################################################################

# Get opinions from the Database at some discussion and return them as a list of opinions
def get_opinions(discussion_id):
    opinion_list = []
    opinion_sql_string = 'SELECT * FROM `opinion` WHERE `d_id` = ' +str(discussion_id)
    opinions = query_with_return(opinion_sql_string)
    for opinion in opinions:
        tag_sql_string = 'SELECT * FROM `hash_tag` WHERE `o_id` = ' + str(opinion[0])
        tags = query_with_return(tag_sql_string)
        tags = [tag[1] for tag in tags]
        op = Opinion.Opinion(id=opinion[0],text=opinion[1],hash_tags=tags)
        opinion_list.append(op)
    return opinion_list
# return list of discussions
def get_discussions():
    discussion_sql_string = 'SELECT * FROM `descussion`'
    discussions_list = query_with_return(discussion_sql_string)
    return  discussions_list
# Execute The sql quieries without results return back
def query_without_results(sql_string):
    conn = None
    cursor = None
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql_string)

        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return

# Execute The sql quieries with results return back
def query_with_return(sql_string):
    rows = None
    cursor = None
    conn = None
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql_string)
        rows = cursor.fetchall()
        rows = list(rows)
        rows = [list(i)for i in rows]
        for row in rows:
            for i in range (len(row)):
                if (type(row[i])== bytes):
                    row[i]= row[i].decode("utf8")
    except Error as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()
    return rows


