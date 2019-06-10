import unittest
import numpy as np
from clustring_algorithms import AgglomerativeClustering
from distance_measurement_algorithms import similarity_methods


class TestAgglomarative(unittest.TestCase):
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

    """def test_create_similarity_matrix(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']]

        # similarity_methods: tag_jaccard
        Obj1 = AgglomerativeClustering.Agglomerative(similarity_methods.tag_jaccard_similarity_method)
        np.testing.assert_array_equal(np.matrix(Obj1._create_similarity_matrix(data)), np.matrix( [[ 0, 1, 0.8, 1 ]
                                                                           ,[ 1, 0, 0.75, 0.66666667]
                                                                           ,[ 0.8, 0.75, 0, 1]
                                                                           ,[ 1, 0.66666667, 1, 0]]))

        # similarity_method: character_jaccard
        Obj2 = AgglomerativeClustering.Agglomerative(similarity_methods.character_jaccard_similarity_method)
        np.testing.assert_array_equal(np.matrix(Obj2._create_similarity_matrix(data)), np.matrix([[0, 0.5625, 0.41176471, 0.4375]
                                                                                                 ,[0.5625, 0, 0.5, 0.16666667]
                                                                                                 ,[0.41176471, 0.5, 0, 0.375]
                                                                                                 ,[0.4375, 0.16666667, 0.375, 0]]))

        # similarity_method: edit_distance
        Obj3 = AgglomerativeClustering.Agglomerative(similarity_methods.edit_distance_method)
        np.testing.assert_array_equal(np.matrix(Obj3._create_similarity_matrix(data)), np.matrix([[  1, -19, -15, -18],
                                                                                                 [-19,   1, -20,  -3],
                                                                                                 [-15, -20,   1, -18],
                                                                                                 [-18,  -3, -18,   1]]))

        # similarity_method: hamming
        Obj4 = AgglomerativeClustering.Agglomerative(similarity_methods.hamming_similarity_method)
        np.testing.assert_array_equal(np.matrix(Obj4._create_similarity_matrix(data)), np.matrix([[0, 1, 1, 0.96153846],
                                                                                                  [1, 0, 1, 0.52941176],
                                                                                                  [1, 1, 0, 1],
                                                                                                  [0.96153846,
                                                                                                   0.52941176, 1, 0]]))

        # similarity_method: levenshtein
        Obj5 = AgglomerativeClustering.Agglomerative(similarity_methods.levenshtein_similarity_method)
        np.testing.assert_array_equal(np.matrix(Obj5._create_similarity_matrix(data)), np.matrix([[0, 0.76923077, 0.61538462, 0.73076923],
                                                                                                 [0.76923077, 0, 0.875, 0.23529412]
                                                                                                 [0.61538462, 0.875, 0, 0.79166667],
                                                                                                 [0.73076923, 0.23529412, 0.79166667, 0]]))

        # similarity_method: jaro_winkler
        Obj6 = AgglomerativeClustering.Agglomerative(similarity_methods.jaro_winkler_similarity_method)
        np.testing.assert_array_equal(np.matrix(Obj6._create_similarity_matrix(data)), np.matrix([[0, 0.48397436, 0.36946958, 0.43030417],
                                                                                                 [0.48397436, 0, 0.45904558, 0.04705882],
                                                                                                 [0.36946958, 0.45904558, 0, 0.44971777],
                                                                                                 [0.43030417, 0.04705882, 0.44971777, 0]]))"""






    def test_cluster(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']]

        # similarity_methods: tag_jaccard
        Obj1 = AgglomerativeClustering.Agglomerative(similarity_methods.tag_jaccard_similarity_method)
        np.testing.assert_array_equal(Obj1.cluster(data, 2), [0, 1, 0, 1])

        # similarity_methods: character_jaccard
        Obj2 = AgglomerativeClustering.Agglomerative(similarity_methods.character_jaccard_similarity_method)
        np.testing.assert_array_equal(Obj2.cluster(data, 2), [0, 1, 0, 1])

        # similarity_methods: edit_distance
        Obj3 = AgglomerativeClustering.Agglomerative(similarity_methods.edit_distance_method)
        np.testing.assert_array_equal(Obj3.cluster(data, 2), [0, 1, 1, 0])

        # similarity_methods: hamming
        Obj4 = AgglomerativeClustering.Agglomerative(similarity_methods.hamming_similarity_method)
        np.testing.assert_array_equal(Obj4.cluster(data, 2), [0, 1, 0, 1])

        # similarity_methods: levenshtein
        Obj5 = AgglomerativeClustering.Agglomerative(similarity_methods.levenshtein_similarity_method)
        np.testing.assert_array_equal(Obj5.cluster(data, 2), [0, 1, 0, 1])

        # similarity_methods: jaro_winkler
        Obj6 = AgglomerativeClustering.Agglomerative(similarity_methods.jaro_winkler_similarity_method)
        np.testing.assert_array_equal(Obj6.cluster(data, 2), [0, 1, 0, 1])



if __name__ == '__main__':
    unittest.main()