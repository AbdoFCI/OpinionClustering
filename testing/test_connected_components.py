import unittest
import numpy as np
from clustring_algorithms import connected_components
from distance_measurement import similarity_methods
from entities import spark_connection

spark_connection = spark_connection.SparkObject('spark')
spark_connection.set_checkpoint_dir()


def get_clusters(model):
    clusters_lists = []
    cluster_index = 0
    opinion_indexs = []
    opinion_indexs.append(model[0].id)
    cluster_index = model[0].component
    for i in range(1, len(model)):
        if model[i].component == cluster_index:
            opinion_indexs.append(model[i].id)
        else:
            clusters_lists.append(opinion_indexs)
            opinion_indexs = []
            opinion_indexs.append(model[i].id)
            cluster_index = model[i].component

    clusters_lists.append(opinion_indexs)
    return clusters_lists


class TestConnectedComponents(unittest.TestCase):
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
        obj = connected_components.ConnectedComponents(similarity_methods.tag_jaccard_similarity_method, spark_connection)
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (2, 2, 1.0), (2, 4, 0.3333333333333333),
                                                                             (3, 3, 1.0), (4, 2, 0.3333333333333333), (4, 4, 1.0)])

        # similarity_methods: character_jaccard
        obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (1, 2, 0.4375), (1, 3, 0.5882352941176471),
                                                              (1, 4, 0.5625), (2, 1, 0.4375), (2, 2, 1.0), (2, 3, 0.5),
                                                              (2, 4, 0.8333333333333334), (3, 1, 0.5882352941176471),
                                                              (3, 2, 0.5), (3, 3, 1.0), (3, 4, 0.625), (4, 1, 0.5625),
                                                              (4, 2, 0.8333333333333334), (4, 3, 0.625), (4, 4, 1.0)])

        # similarity_methods: edit_distance
        obj.similarity_method = similarity_methods.edit_distance_method
        np.testing.assert_array_equal(obj._create_similarities_list(data),[(1, 2, 20), (1, 3, 16), (1, 4, 19), (2, 1, 20),
                                                                            (2, 3, 21),(2, 4, 4), (3, 1, 16), (3, 2, 21),
                                                                            (3, 4, 19), (4, 1, 19), (4, 2, 4), (4, 3, 19)])

        # similarity_methods: tree
        obj.similarity_method = similarity_methods.tree_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data),[(1, 1, 0.4444444444444444), (1, 2, 0.5833333333333334),
                                                                           (1, 3, 0.4166666666666667), (1, 4, 0.5833333333333334),
                                                                           (2, 1, 0.5833333333333334), (2, 2, 1.0), (2, 3, 0.625),
                                                                           (2, 4, 1.0), (3, 1, 0.4166666666666667), (3, 2, 0.625),
                                                                           (3, 3, 0.4166666666666667), (3, 4, 0.625), (4, 1, 0.5833333333333334),
                                                                           (4, 2, 1.0), (4, 3, 0.625), (4, 4, 1.0)] )

        # similarity_methods: hamming
        obj.similarity_method = similarity_methods.hamming_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (2, 2, 1.0), (2, 4, 0.47058823529411764),
                                                                             (3, 3, 1.0), (4, 2, 0.47058823529411764), (4, 4, 1.0)])

        # similarity_methods: levenshtein
        obj.similarity_method = similarity_methods.levenshtein_similarity_method
        np.testing.assert_array_equal(obj._create_similarities_list(data), [(1, 1, 1.0), (1, 3, 0.3846153846153846), (2, 2, 1.0),
                                                                             (2, 4, 0.7647058823529411), (3, 1, 0.3846153846153846),
                                                                             (3, 3, 1.0), (4, 2, 0.7647058823529411), (4, 4, 1.0)])

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
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']
            , ['1', '2'], ['2', '1'], ['5', '6'], ['6', '7']]

        # similarity_methods: tag_jaccard
        obj = connected_components.ConnectedComponents(similarity_methods.tag_jaccard_similarity_method, spark_connection)
        var = obj.cluster(data,2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1], [2, 4], [3], [5, 6], [7, 8]])

        # similarity_methods: character_jaccard
        obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        var = obj.cluster(data, 2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4], [5, 6], [7, 8]])

        # similarity_methods: edit_distance
        obj.similarity_method = similarity_methods.edit_distance_method
        var = obj.cluster(data, 2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4, 5, 6, 7, 8]])

        # similarity_methods: hamming
        obj.similarity_method = similarity_methods.hamming_similarity_method
        var = obj.cluster(data, 2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1], [2, 4], [3], [5], [6], [7], [8]])

        # similarity_methods: levenshtein
        obj.similarity_method = similarity_methods.levenshtein_similarity_method
        var = obj.cluster(data, 2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 3], [2, 4], [5], [6], [7], [8]])

        # similarity_methods: jaro_winkler
        obj.similarity_method = similarity_methods.jaro_winkler_similarity_method
        var = obj.cluster(data, 2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4], [5], [6], [7], [8]])

        # similarity_methods: tree
        obj.similarity_method = similarity_methods.tree_similarity_method
        var = obj.cluster(data, 2)
        var = var.sort('component')
        model = get_clusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4], [5], [6], [7], [8]])














if __name__ == '__main__':
    unittest.main()