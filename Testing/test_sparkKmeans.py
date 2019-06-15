from Entities import SparkConnection
from clustring_algorithms import sparkKmeans
import unittest
import numpy as np


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

    def test_cluster(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']
            , ['1', '2']
            , ['2', '1']
            , ['5', '6']
            , ['6', '7']
            , ['الماجيكو', 'تريكه']]
        sc = SparkConnection.SparkObject('spark')
        sc.setCheckpointDir()

        Obj = sparkKmeans.KMeansClustering(sc)
        model = Obj.cluster(data,4)
        clusters = getClusters(model)
        clusters.sort()
        np.testing.assert_array_equal(clusters,[[0, 1], [2, 7], [3, 4], [5, 6]])