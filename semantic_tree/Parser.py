"""
this file class tree that responsible for getting the directory url paths and get the distance between the nodes
"""
import os
from Data_manipulation import elasticsearchManager
import pandas as pd
import pyarabic.araby as araby


class Tree:

    root = ""
    files = dict()

    def __init__(self, root=r"F:\my data\GP\root"):
        self.root = root

    def get_p_files(self):
        """
        this function get all file paths in the file system starting from the root
        :return: type list all the file paths in the file system
        """
        files = []
        for r, d, f in os.walk(self.root):
            for file in f:
                if '.ini' not in file:
                    files.append(os.path.join(r, file))
        return files

    def get_p_dirs(self):
        """
        this function returns all directories in the file system starting from the root
        :return: type list all the file paths in the file system
        """
        dirs = []
        for r, d, f in os.walk(self.root):
            for dir in d:
                dirs.append(os.path.join(r, dir))
        return dirs

    @staticmethod
    def get_lca(path1, path2):
        """

        :param path1: list
        :param path2: list
        :return: list lca lowest common ancestor of path1 and path2
        """
        lca = []
        min_len = min(len(path1),len(path2))
        for i in range(min_len):
            if path1[i] == path2[i]:
                lca.append(path2[i])
            else: break
        return lca

    def calc_dist(self,path1,path2):
        """

        :param path1: the first path
        :param path2: the second path
        :return: type int distance between the two paths
        """
        if not path2 or not path1:
            return 0
        path1 = path1.split("\\")
        path2 = path2.split("\\")
        result = len(path1) + len(path2) - 2 * len(self.get_lca(path1,path2))
        return result

    def find_tag_path(self, tag):
        result = ""
        query_arabic = {
            'size': 10000,
            'query': {
                "bool": {
                    "filter": [
                        {"term": {"arabichashtags" : tag }}
                    ]
                }
            }
        }
        query_english = {
            'size': 10000,
            'query': {
                "match": {
                    "englishhashtags": tag
                }
            }
        }
        res = elasticsearchManager.es.search(index='tree', doc_type="tree_leaf", body=query_arabic, timeout='60m')
        if not res['hits']['hits']:
            res = elasticsearchManager.es.search(index='tree', doc_type="tree_leaf", body=query_english, timeout='60m')
        data = [doc for doc in res['hits']['hits']]
        if data:
            result = data[0]['_source']['path']
            return result
        return None

    def read_file(self, file_path):
        result = set()
        if file_path in self.files:
            result = self.files[file_path]
        else:
            file = pd.read_excel(file_path)
            file = set(file["tags"])
            self.files[file_path] = file
            result = self.files[file_path]
        return result

    def find_last_index(self, string, character):

        for i in range(len(string) - 1, -1, -1):
            if string[i] == character:
                return i
        return -1

    def file_to_json(self, file_path, file_content):
        idx_last_char = self.find_last_index(file_path, '\\')
        file_path = file_path[0:idx_last_char]
        file_content = list(file_content)
        if araby.is_arabicword(file_content[0]) or araby.is_arabicword(file_content[0][0]):
            return {"path":file_path, "arabichashtags":list(file_content)}
        return {"path":file_path, "englishhashtags":list(file_content)}


class HashTagSimilarity:

    tag_base = ""
    roots = dict()
    tree = None
    max_depth = 1
    tag_paths = dict()

    def __init__(self, tag_base=r"F:\my data\GP\root"):
        self.tag_base = tag_base
        self.tree = Tree(tag_base)

    def set_root(self,root):
        if root in self.roots :
            self.tree.root = self.roots[root]
        else:
            print("no root with this name")
        return

    def get_path(self,tag):
        """
        this function first search in the memory if tag is loaded if not search using elasticsearch
        :param tag: str
        :return: str
        """
        tag_path = ""

        if tag in self.tag_paths:
            tag_path = self.tag_paths[tag]
        else:
            tag_path = self.tree.find_tag_path(tag)
            self.tag_paths[tag] = tag_path
        return tag_path

    def get_similarity(self,tag1,tag2):
        tag1_path = self.get_path(tag1)
        tag2_path = self.get_path(tag2)
        distance = self.tree.calc_dist(tag1_path,tag2_path)
        if tag1_path and tag2_path:
            self.max_depth = len(tag1_path.split("\\")) + len(tag2_path.split("\\")) - 2
        else:
            return 0.0
        distance = distance / self.max_depth
        return 1 - distance

    def get_list_similarity(self, first_list, second_list):
        """
        taking two lists and compute the similarity between them
        :param first_list: List
        :param second_list: :List
        :return: double
        """
        total_sum = 0
        num_elements = len(first_list) * len(second_list)
        for outer_tag in first_list:
            for inner_tag in second_list:
                total_sum += self.get_similarity(outer_tag, inner_tag)
        return total_sum / num_elements
