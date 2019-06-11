import unittest
import numpy as np
from clustring_algorithms import ConnectedComponents
from distance_measurement_algorithms import similarity_methods
from Entities import SparkConnection

sc = SparkConnection.SparkObject('spark')
sc.setCheckpointDir()


def getClusters(s):
    arr = []
    CInd = 0
    lis = []
    lis.append(s[0].id)
    CInd = s[0].component
    for i in range(1, len(s)):
        if s[i].component == CInd:
            lis.append(s[i].id)
        else:
            arr.append(lis)
            lis = []
            lis.append(s[i].id)
            CInd = s[i].component

    arr.append(lis)
    return arr
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
        Obj = ConnectedComponents.ConnectedComponents(similarity_methods.tag_jaccard_similarity_method,sc)
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (2, 2, 1.0), (2, 4, 0.3333333333333333),
                                                                             (3, 3, 1.0), (4, 2, 0.3333333333333333), (4, 4, 1.0)])

        # similarity_methods: character_jaccard
        Obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (1, 2, 0.4375), (1, 3, 0.5882352941176471),
                                                              (1, 4, 0.5625), (2, 1, 0.4375), (2, 2, 1.0), (2, 3, 0.5),
                                                              (2, 4, 0.8333333333333334), (3, 1, 0.5882352941176471),
                                                              (3, 2, 0.5), (3, 3, 1.0), (3, 4, 0.625), (4, 1, 0.5625),
                                                              (4, 2, 0.8333333333333334), (4, 3, 0.625), (4, 4, 1.0)])

        # similarity_methods: edit_distance
        Obj.similarity_method = similarity_methods.edit_distance_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data),[(1, 2, 20), (1, 3, 16), (1, 4, 19), (2, 1, 20),
                                                                            (2, 3, 21),(2, 4, 4), (3, 1, 16), (3, 2, 21),
                                                                            (3, 4, 19), (4, 1, 19), (4, 2, 4), (4, 3, 19)])

        """# similarity_methods: tree
        #Obj4 = ConnectedComponents.ConnectedComponents(similarity_methods.tree_similarity_method,SparkConnection.SparkObject("appName"))
        #np.testing.assert_array_equal(Obj4._create_similarities_list(data), )"""

        # similarity_methods: hamming
        Obj.similarity_method = similarity_methods.hamming_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (2, 2, 1.0), (2, 4, 0.47058823529411764),
                                                                             (3, 3, 1.0), (4, 2, 0.47058823529411764), (4, 4, 1.0)])

        # similarity_methods: levenshtein
        Obj.similarity_method = similarity_methods.levenshtein_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (1, 3, 0.3846153846153846), (2, 2, 1.0),
                                                                             (2, 4, 0.7647058823529411), (3, 1, 0.3846153846153846),
                                                                             (3, 3, 1.0), (4, 2, 0.7647058823529411), (4, 4, 1.0)])

        # similarity_methods: jaro_winkler
        Obj.similarity_method = similarity_methods.jaro_winkler_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1), (1, 2, 0.5160256410256411), (1, 3, 0.6305304172951232),
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
        Obj = ConnectedComponents.ConnectedComponents(similarity_methods.tag_jaccard_similarity_method, sc)
        var = Obj.cluster(data,2)
        var = var.sort('component')
        model = getClusters(var.collect())
        np.testing.assert_array_equal(model, [[1], [2, 4], [3], [5, 6], [7, 8]])

        # similarity_methods: character_jaccard
        Obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        var = Obj.cluster(data, 2)
        var = var.sort('component')
        model = getClusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4], [5, 6], [7, 8]])

        # similarity_methods: edit_distance
        Obj.similarity_method = similarity_methods.edit_distance_method
        var = Obj.cluster(data, 2)
        var = var.sort('component')
        model = getClusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4, 5, 6, 7, 8]])

        # similarity_methods: hamming
        Obj.similarity_method = similarity_methods.hamming_similarity_method
        var = Obj.cluster(data, 2)
        var = var.sort('component')
        model = getClusters(var.collect())
        np.testing.assert_array_equal(model, [[1], [2, 4], [3], [5], [6], [7], [8]])

        # similarity_methods: levenshtein
        Obj.similarity_method = similarity_methods.levenshtein_similarity_method
        var = Obj.cluster(data, 2)
        var = var.sort('component')
        model = getClusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 3], [2, 4], [5], [6], [7], [8]])

        # similarity_methods: jaro_winkler
        Obj.similarity_method = similarity_methods.jaro_winkler_similarity_method
        var = Obj.cluster(data, 2)
        var = var.sort('component')
        model = getClusters(var.collect())
        np.testing.assert_array_equal(model, [[1, 2, 3, 4], [5], [6], [7], [8]])














if __name__ == '__main__':
    unittest.main()