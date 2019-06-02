"""
this file class tree that responsible for getting the directory url paths and get the distance between the nodes
"""
import os
import json
from configparser import ConfigParser
import pandas as pd


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
        if path1 == "" or path2 == "":
            return 0
        path1 = path1.split("\\")
        path2 = path2.split("\\")
        result = len(path1) + len(path2) - 2 * len(self.get_lca(path1,path2))
        return result

    def find_tag_path(self, tag):
        result = ""
        files = self.get_p_files()
        for file_path in files:
            file = self.read_file(file_path)

            if tag in file:
                result = file_path
                break
        return result

    def read_file(self,file_path):
        result = set()
        if file_path in self.files:
            result = self.files[file_path]
        else:
            file = pd.read_excel(file_path)
            file = set(file["tags"])
            self.files[file_path] = file
            result = self.files[file_path]
        return result


class HashTagSimilarity:

    tag_base = ""
    roots = dict()
    tree = None
    max_depth = 0
    tag_paths = dict()

    def __init__(self, tag_base=r"F:\my data\GP\root"):
        self.tag_base = tag_base
        init = self.load_init(tag_base)
        self.max_depth = int(init['max_depth'])
        roots = json.loads(init['roots'])
        self.tree = Tree(tag_base)

    def set_root(self,root):
        if root in self.roots :
            self.tree.root = self.roots[root]
        else:
            print("no root with this name")
        return

    def get_path(self,tag):
        """
        this function first search in the memory if tag is loaded if not search in the file system
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
        distance = distance /(2*self.max_depth)
        return 1-distance

    def get_list_similarity(self,first_list,second_list):
        """
        taking two lists and compute the similarity between them
        :param first_list: List
        :param second_list: List
        :return: double
        """
        total_sum = 0
        num_elements = len(first_list) * len(second_list)
        for outer_tag in first_list:
            for inner_tag in second_list:
                total_sum += self.get_similarity(outer_tag,inner_tag)
        return total_sum / num_elements

    @staticmethod
    def load_init(tag_base,section="metadata"):
        """
        this function reads the init file for the file system of the Knowledge
        :param tag_base: str
        :param section: str
        :return: dict
        """
        parser = ConfigParser()
        file_name = tag_base + "\\config.ini"
        parser.read(r"F:\my data\GP\root\config.ini",encoding='utf-8-sig')
        index_body = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                index_body[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section, file_name))
        return index_body
