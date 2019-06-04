import nltk
#from semantic_tree import Parser
import textdistance


def tag_jaccard_similarity_method(list1,list2):
    """
    get the jaccard similarity between two lists based on tag
    :param list1: list of str
    :param list2: list of str
    :return: double
    """

    return  (len(set.intersection(set(list1), set(list2)))) / \
           (len(set.union(set(list1), set(list2))))


def character_jaccard_similarity_method(list1,list2):
    """
    get the jaccard similarity between two lists based on characters
    :param list1: list of str
    :param list2: list of str
    :return: double
    """

    opinion1_str = "".join(list1)
    opinion2_str = "".join(list2)

    return tag_jaccard_similarity_method(list(set(opinion1_str))
                                         , list(set(opinion2_str)))


def edit_distance_method(list1,list2):
    """
    get the levenshtein distance between two lists
    :param list1: list of str
    :param list2: list of str
    :return: int
    """
    opinion1_str = "".join(list1)
    opinion2_str = "".join(list2)
    return nltk.edit_distance(opinion1_str,opinion2_str)


# def tree_similarity_method(list1,list2):
#     """
#     get the similarity between two lists using similarity tree
#     :param list1: list of str
#     :param list2: list of str
#     :return: double
#     """
#
#     sim = Parser.HashTagSimilarity()
#     return sim.get_list_similarity(list1, list2)


def hamming_similarity_method(list1, list2):
    """

    :param list1:list of str
    :param list2:list of str
    :return:
    """
    text1 = "".join(list1)
    text2 = "".join(list2)
    return textdistance.hamming.normalized_similarity(text1, text2)


def levenshtein_similarity_method(list1, list2):
    """

    :param list1:list of str
    :param list2:list of str
    :return:
    """
    text1 = "".join(list1)
    text2 = "".join(list2)
    return textdistance.levenshtein.normalized_similarity(text1, text2)


def jaro_winkler_similarity_method(list1, list2):
    """

    :param list1:list of str
    :param list2:list of str
    :return:
    """
    text1 = "".join(list1)
    text2 = "".join(list2)
    return textdistance.jaro_winkler(text1, text2)