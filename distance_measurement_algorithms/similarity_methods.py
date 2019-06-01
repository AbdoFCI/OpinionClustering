import nltk
from semantic_tree import Parser

def tag_jaccard_similarity_method(list1,list2):
    """
    get the jaccard similarity between two lists based on tag
    :param list1: list of str
    :param list2: list of str
    :return: double
    """

    return 1 - (len(set.intersection(set(list1), set(list2)))) / \
           (len(set.union(set(list1), set(list2))))


def character_jaccard_similarity_method(list1,list2):
    """
    get the jaccard similarity between two lists based on characters
    :param list1: list of str
    :param list2: list of str
    :return: double
    """

    opinion1_str = str(set(list1))
    opinion2_str = str(set(list2))
    return nltk.jaccard_distance(set(opinion1_str), set(opinion2_str))


def edit_distance_method(list1,list2):
    """
    get the levenshtein distance between two lists
    :param list1: list of str
    :param list2: list of str
    :return: int
    """

    return nltk.edit_distance(str(set(list1)), str(set(list2)))


def tree_similarity_method(list1,list2):
    """
    get the similarity between two lists
    :param list1: list of str
    :param list2: list of str
    :return: double
    """

    sim = Parser.HashTagSimilarity()
    return sim.get_list_similarity(list1, list2)

