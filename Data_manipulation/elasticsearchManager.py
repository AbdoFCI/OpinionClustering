from elasticsearch import Elasticsearch
import json
from configparser import ConfigParser
from Entities import Opinion
from Data_manipulation import mysqlManager
import semantic_tree.Parser as tree_parser

es = Elasticsearch(['192.168.1.15'],
    # sniff before doing anything
    sniff_on_start=True,
    # refresh nodes after a node fails to respond
    sniff_on_connection_fail=True,
    # and also every 60 seconds
    sniffer_timeout=60)


def read_index_setting(file_name='Data_manipulation\\config.ini', section='elasticsearch'):
    """
    Read Elastic index settings configuration file
    :param file_name: str path of configuration file
    :param section : str the name of the section
    :return: dictionary
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(file_name)
    # get section, default to mysql
    index_body = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            index_body[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, file_name))
    index_body = json.loads(index_body['index_body'])
    return index_body


def read_tree_index_setting(file_name='Data_manipulation\\config.ini', section='tree'):
    """
    Read tree index settings configuration file for Elastic search
    :param file_name: str path of the tree configuration file
    :param section: str the name of section in the file
    :return: dictionary
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(file_name)
    # get section
    index_body = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            index_body[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, file_name))
    index_body = json.loads(index_body['tree_index_body'])
    return index_body


def create_index(index_name):
    """
    Create an index with configuration in the configuration file
    :param index_name: str index name
    :return: None
    """
    index_body = read_index_setting()
    es.indices.create(index=index_name, body=index_body)
    return


def create_tree_index(tree_root):
    """
    create the tree index with the configuration in the configuration file
    :param tree_root: str path of the tree root folder
    :return: None
    """
    index_body = read_tree_index_setting()
    delete_index('tree')
    es.indices.create(index='tree', body=index_body)
    tree = tree_parser.Tree(tree_root)
    tree_files = tree.get_p_files()
    for file in tree_files:
        file_content = tree.read_file(file)
        file_body = tree.file_to_json(file[file.find('root'):], file_content)
        es.index(index='tree', doc_type='tree_leaf', body=file_body, timeout='60m')
    return


def delete_index(index_name):
    """
    Delete an index from elastic search
    :param index_name: str the name of the index
    :return: None
    """
    es.indices.delete(index=index_name)
    return


def insert_opinion(index_name, opinion):
    """
    indexing an opinion in elastic search index
    :param index_name: str
    :param opinion: opinion
    :return: None
    """
    op_body = opinion.opinion_to_json()
    es.index(index=index_name, doc_type="op", body=op_body, id=opinion.id)
    return


def get_opinions(index_name):
    """
    Get 10000 opinions from an index
    :param index_name: str
    :return: list of opinions
    """
    opinion_list = []
    query = {
        'size': 10000,
        'query': {
            'match_all': {}
        }
    }
    res = es.search(index=index_name, doc_type="op", body=query)
    data = [doc for doc in res['hits']['hits']]
    for doc in data:
        temp = Opinion.Opinion()
        temp.json_to_opinion(doc['_source'])
        opinion_list.append(temp)
    return opinion_list


def analyze_hashtag(index_name, hashtag):
    """
    Normalize hashtag
    :param index_name: str
    :param hashtag: str
    :return: str normalized hashtag
    """
    analyzer = {
        "analyzer": "arabicAnalyzer",
        "text": hashtag
    }
    detailed_tokens = es.indices.analyze(index=index_name, body=analyzer, format='text')
    result_string = ''
    tokens = detailed_tokens['tokens']
    for token in tokens:
        result_string += token['token']+' '
    return result_string


def analyze_opinion(index_name, hashtag_list):
    """
    Normalize a list of hashtags
    :param index_name: str
    :param hashtag_list: list of str
    :return: list of str
    """
    analyzed_list = []
    for hashtag in hashtag_list:
        analyzed_list.append(analyze_hashtag(index_name, hashtag))
    return analyzed_list


def analyze_all_opinions(index_name, opinion_list):
    """
    Normalize all lists of hashtags for a list of opinions
    :param index_name: str
    :param opinion_list: list of opinions
    :return: list of opinions
    """
    for index in range(len(opinion_list)):
        opinion_list[index].hash_tags = analyze_opinion(index_name, opinion_list[index].hash_tags)
    return opinion_list


def from_sql_to_elastcsearch():
    """
    Copying the discussions from mysql Database to elastic search by making index for each discussion by its name
    :return: None
    """
    discussions_list = mysqlManager.get_discussions()
    for discussion in discussions_list:
        d_id = discussion[0]
        d_name = discussion[4]
        d_name = d_name.replace(' ', '_')
        opinion_list = mysqlManager.get_opinions(d_id)
        create_index(d_name)
        opinion_list = analyze_all_opinions(d_name, opinion_list)
        for opinion in opinion_list:
            insert_opinion(d_name, opinion)
    return
