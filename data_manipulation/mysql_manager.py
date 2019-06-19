from configparser import ConfigParser
from mysql.connector import Error, MySQLConnection
from  entities import opinion

def read_db_config(file_name='data_manipulation\\config.ini', section='mysql'):
    """

    Read database configuration file
    :param file_name: str : directory of the configuration file default("data_manipulation\\config.ini")
    :param section: str : the name of mysql section
    :return db: dictionary object
    """
    
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

def get_opinions(discussion_id):
    """

    Get opinions from the Database at some discussion
    :param discussion_id: int
    :return: opinion_list: list of opinions
    """
    opinion_list = []
    opinion_sql_string = 'SELECT * FROM `opinion` WHERE `d_id` = ' +str(discussion_id)
    opinions = query_with_return(opinion_sql_string)
    for opinion in opinions:
        tag_sql_string = 'SELECT * FROM `hash_tag` WHERE `o_id` = ' + str(opinion[0])
        tags = query_with_return(tag_sql_string)
        tags = [tag[1] for tag in tags]
        op = opinion.Opinion(id=opinion[0], text=opinion[1], hash_tags=tags)
        opinion_list.append(op)
    return opinion_list

def get_discussions():
    """

    Get the all discussions about some topic
    :return: discussions_list: list of str
    """
    discussion_sql_string = 'SELECT * FROM `descussion`'
    discussions_list = query_with_return(discussion_sql_string)
    return  discussions_list


def query_without_results(sql_string):
    """

    Execute The sql quieries without results e.g. insert, delete, update
    :param sql_string: str
    :return: None
    """
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

def query_with_return(sql_string):
    """

    Execute The sql quieries with results e.g. select
    :param sql_string: str
    :return: resultset
    """
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


