import unittest
import numpy as np
from clustring_algorithms import AgglomerativeClustering
from distance_measurement_algorithms import similarity_methods

def getClusters(s):
    arr = []
    maxx = max(s)
    for clusterIndex in range(0,maxx+1):
        indices = [i for i, x in enumerate(s) if x == clusterIndex]
        arr.append(indices)
    return arr

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

    def test_create_similarity_matrix(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']]

        # similarity_methods: tag_jaccard
        out1 = [[0, 1, 0.8, 1], [1, 0, 0.75, 0.6666666666666667], [0.8, 0.75, 0, 1], [1, 0.6666666666666667, 1, 0]]
        Obj1 = AgglomerativeClustering.Agglomerative(similarity_methods.tag_jaccard_similarity_method)
        np.testing.assert_array_equal(Obj1._create_similarity_matrix(data).tolist(), np.matrix(out1).tolist())

        # similarity_method: character_jaccard
        out2 = [[0.0, 0.5625, 0.4117647058823529, 0.4375], [0.5625, 0.0, 0.5, 0.16666666666666663], [0.4117647058823529, 0.5, 0.0, 0.375], [0.4375, 0.16666666666666663, 0.375, 0.0]]
        Obj2 = AgglomerativeClustering.Agglomerative(similarity_methods.character_jaccard_similarity_method)
        np.testing.assert_array_equal(Obj2._create_similarity_matrix(data).tolist(), np.matrix(out2).tolist())

        # similarity_method: edit_distance
        out3 = [[  1, -19, -15, -18],[-19,   1, -20,  -3],[-15, -20,   1, -18],[-18,  -3, -18,   1]]
        Obj3 = AgglomerativeClustering.Agglomerative(similarity_methods.edit_distance_method)
        np.testing.assert_array_equal(Obj3._create_similarity_matrix(data).tolist(), np.matrix(out3).tolist())

        # similarity_method: hamming
        out4 =[[0.0, 1.0, 1.0, 0.9615384615384616], [1.0, 0.0, 1.0, 0.5294117647058824], [1.0, 1.0, 0.0, 1.0], [0.9615384615384616, 0.5294117647058824, 1.0, 0.0]]
        Obj4 = AgglomerativeClustering.Agglomerative(similarity_methods.hamming_similarity_method)
        np.testing.assert_array_equal(Obj4._create_similarity_matrix(data).tolist(), np.matrix(out4).tolist())

        # similarity_method: levenshtein
        out5 = [[0.0, 0.7692307692307693, 0.6153846153846154, 0.7307692307692307], [0.7692307692307693, 0.0, 0.875, 0.23529411764705888], [0.6153846153846154, 0.875, 0.0, 0.7916666666666666], [0.7307692307692307, 0.23529411764705888, 0.7916666666666666, 0.0]]
        Obj5 = AgglomerativeClustering.Agglomerative(similarity_methods.levenshtein_similarity_method)
        np.testing.assert_array_equal(Obj5._create_similarity_matrix(data).tolist(), np.matrix(out5).tolist())

        # similarity_method: jaro_winkler
        out6 = [[0.0, 0.4839743589743589, 0.36946958270487684, 0.4303041729512317], [0.4839743589743589, 0.0, 0.45904558404558404, 0.04705882352941182], [0.36946958270487684, 0.45904558404558404, 0.0, 0.4497177658942365], [0.4303041729512317, 0.04705882352941182, 0.4497177658942365, 0.0]]
        Obj6 = AgglomerativeClustering.Agglomerative(similarity_methods.jaro_winkler_similarity_method)
        np.testing.assert_array_equal(Obj6._create_similarity_matrix(data).tolist(), np.matrix(out6).tolist())

        # similarity_method: tree
        out7 = [[0.5555555555555556, 0.41666666666666663, 0.5833333333333333, 0.41666666666666663], [0.41666666666666663, 0.0, 0.375, 0.0], [0.5833333333333333, 0.375, 0.5833333333333333, 0.375], [0.41666666666666663, 0.0, 0.375, 0.0]]
        Obj7 = AgglomerativeClustering.Agglomerative(similarity_methods.tree_similarity_method)
        np.testing.assert_array_equal(Obj7._create_similarity_matrix(data).tolist(), np.matrix(out7).tolist())






    def test_cluster(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']]

        # similarity_methods: tag_jaccard
        Obj1 = AgglomerativeClustering.Agglomerative(similarity_methods.tag_jaccard_similarity_method)
        model = Obj1.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal( clusters , [[0,2],[1,3]])

        # similarity_methods: character_jaccard
        Obj2 = AgglomerativeClustering.Agglomerative(similarity_methods.character_jaccard_similarity_method)
        model = Obj2.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal(clusters, [[0,2],[1,3]])

        # similarity_methods: edit_distance
        Obj3 = AgglomerativeClustering.Agglomerative(similarity_methods.edit_distance_method)
        model = Obj3.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal(clusters, [[0,3],[1,2]])

        # similarity_methods: hamming
        Obj4 = AgglomerativeClustering.Agglomerative(similarity_methods.hamming_similarity_method)
        model = Obj4.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal(clusters, [[0,2],[1,3]])

        # similarity_methods: levenshtein
        Obj5 = AgglomerativeClustering.Agglomerative(similarity_methods.levenshtein_similarity_method)
        model = Obj5.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal(clusters, [[0,2],[1,3]])

        # similarity_methods: jaro_winkler
        Obj6 = AgglomerativeClustering.Agglomerative(similarity_methods.jaro_winkler_similarity_method)
        model = Obj6.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal(clusters, [[0,2],[1,3]])

        # similarity_methods: tree
        Obj7 = AgglomerativeClustering.Agglomerative(similarity_methods.tree_similarity_method)
        model = Obj7.cluster(data, 2)
        clusters = getClusters(model)
        np.testing.assert_array_equal(clusters, [[1, 2, 3], [0]])


if __name__ == '__main__':
    unittest.main()