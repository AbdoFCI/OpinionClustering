import unittest
import numpy as np
from clustring_algorithms import pic
from distance_measurement import similarity_methods
from entities import spark_connection

sc = spark_connection.SparkObject('spark')
sc.set_checkpoint_dir()

def get_clusters(model):
    clusters_lists = []
    maxx = max(model)
    for clusterIndex in range(0, maxx + 1):
        indices = [i for i, x in enumerate(model) if x == clusterIndex]
        clusters_lists.append(indices)
    return clusters_lists

class TestPIC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('setupClass\n')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass\n')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    def test_create_similarities_list(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']]

        # similarity_methods: tag_jaccard
        obj = pic.PIC(similarity_methods.tag_jaccard_similarity_method,sc)
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (1, 3, 0.2), (2, 2, 1.0),
                                                                            (2, 3, 0.25), (2, 4, 0.3333333333333333),
                                                                            (3, 1, 0.2), (3, 2, 0.25), (3, 3, 1.0),
                                                                            (4, 2, 0.3333333333333333), (4, 4, 1.0)])

        # similarity_methods: character_jaccard
        obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (1, 2, 0.4375), (1, 3, 0.5882352941176471),
                                                                            (1, 4, 0.5625), (2, 1, 0.4375), (2, 2, 1.0), (2, 3, 0.5),
                                                                            (2, 4, 0.8333333333333334), (3, 1, 0.5882352941176471),
                                                                            (3, 2, 0.5), (3, 3, 1.0), (3, 4, 0.625), (4, 1, 0.5625),
                                                                            (4, 2, 0.8333333333333334), (4, 3, 0.625), (4, 4, 1.0)])

        # similarity_methods: edit_distance
        obj.similarity_method = similarity_methods.edit_distance_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 2, 20), (1, 3, 16), (1, 4, 19), (2, 1, 20),
                                                                            (2, 3, 21), (2, 4, 4), (3, 1, 16), (3, 2, 21),
                                                                            (3, 4, 19), (4, 1, 19), (4, 2, 4), (4, 3, 19)])

        # similarity_methods: tree
        obj.similarity_method = similarity_methods.tree_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 0.4444444444444444), (1, 2, 0.5833333333333334),
                                                                            (1, 3, 0.4166666666666667), (1, 4, 0.5833333333333334),
                                                                            (2, 1, 0.5833333333333334), (2, 2, 1.0), (2, 3, 0.625),
                                                                            (2, 4, 1.0), (3, 1, 0.4166666666666667), (3, 2, 0.625),
                                                                            (3, 3, 0.4166666666666667), (3, 4, 0.625),
                                                                            (4, 1, 0.5833333333333334), (4, 2, 1.0), (4, 3, 0.625), (4, 4, 1.0)])

        # similarity_methods: hamming
        obj.similarity_method = similarity_methods.hamming_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (2, 2, 1.0), (2, 4, 0.47058823529411764),
                                                                            (3, 3, 1.0), (4, 2, 0.47058823529411764), (4, 4, 1.0)])

        # similarity_methods: levenshtein
        obj.similarity_method = similarity_methods.levenshtein_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (1, 2, 0.23076923076923073), (1, 3, 0.3846153846153846),
                                                                            (1, 4, 0.2692307692307693), (2, 1, 0.23076923076923073), (2, 2, 1.0),
                                                                            (2, 3, 0.125), (2, 4, 0.7647058823529411), (3, 1, 0.3846153846153846),
                                                                            (3, 2, 0.125), (3, 3, 1.0), (3, 4, 0.20833333333333337),
                                                                            (4, 1, 0.2692307692307693), (4, 2, 0.7647058823529411),
                                                                            (4, 3, 0.20833333333333337), (4, 4, 1.0)])

        # similarity_methods: jaro_winkler
        obj.similarity_method = similarity_methods.jaro_winkler_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1), (1, 2, 0.5160256410256411), (1, 3, 0.6305304172951232),
                                                                            (1, 4, 0.5696958270487683), (2, 1, 0.5160256410256411), (2, 2, 1),
                                                                            (2, 3, 0.540954415954416), (2, 4, 0.9529411764705882),
                                                                            (3, 1, 0.6305304172951232), (3, 2, 0.540954415954416), (3, 3, 1),
                                                                            (3, 4, 0.5502822341057635), (4, 1, 0.5696958270487683),
                                                                            (4, 2, 0.9529411764705882), (4, 3, 0.5502822341057635), (4, 4, 1)])


    def test_cluster(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']
            , ['1', '2']
            , ['2', '1']
            , ['5', '6']
            , ['6', '7']
            , ['الماجيكو', 'تريكه']]

        # similarity_methods: tag_jaccard
        obj = pic.PIC(similarity_methods.tag_jaccard_similarity_method, sc)
        model = obj.cluster(data)
        clusters = get_clusters(model)
        np.testing.assert_array_equal(clusters, [[5, 6], [3, 4], [1, 2], [0,7]])

        # similarity_methods: character_jaccard
        obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        model = obj.cluster(data)
        clusters = get_clusters(model)
        np.testing.assert_array_equal(clusters, [[5, 6], [0, 1, 7], [3, 4], [2]])

        # similarity_methods: edit_distance
        obj.similarity_method = similarity_methods.edit_distance_method
        model = obj.cluster(data)
        clusters = get_clusters(model)
        np.testing.assert_array_equal(clusters, [[3, 4, 5, 6], [0, 1], [7], [2]])

        # similarity_methods: hamming
        obj.similarity_method = similarity_methods.hamming_similarity_method
        model = obj.cluster(data)
        clusters = get_clusters(model)
        np.testing.assert_array_equal(clusters, [[0, 1]])

        # similarity_methods: levenshtein
        obj.similarity_method = similarity_methods.levenshtein_similarity_method
        model = obj.cluster(data)
        clusters = get_clusters(model)
        np.testing.assert_array_equal(clusters, [[2], [3], [0], [1]])

        # similarity_methods: jaro_winkler
        obj.similarity_method = similarity_methods.jaro_winkler_similarity_method
        model = obj.cluster(data)
        clusters = get_clusters(model)
        np.testing.assert_array_equal(clusters, [[2], [3], [0], [1]])

        # similarity_methods: tree
        obj.similarity_method = similarity_methods.tree_similarity_method
        model = obj.cluster(data)
        clusters = get_clusters(model)
        print(clusters)
        np.testing.assert_array_equal(clusters, [[2, 3], [0], [1]])

