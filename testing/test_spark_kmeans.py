from entities import spark_connection
from clustring_algorithms import spark_kmeans
import unittest
import numpy as np


def get_clusters(model):
    clusters_lists = []
    maxx = max(model)
    for clusterIndex in range(0, maxx + 1):
        indices = [i for i, x in enumerate(model) if x == clusterIndex]
        clusters_lists.append(indices)
    return clusters_lists

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

    def test_cluster(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']
            , ['1', '2']
            , ['2', '1']
            , ['5', '6']
            , ['6', '7']
            , ['الماجيكو', 'تريكه']]
        spark_connections = spark_connection.SparkObject('spark')
        spark_connections.set_checkpoint_dir()

        obj = spark_kmeans.KMeansClustering(spark_connections)
        model = obj.cluster(data,4)
        clusters = get_clusters(model)
        clusters.sort()
        np.testing.assert_array_equal(clusters,[[0, 1], [2, 7], [3, 4], [5, 6]])