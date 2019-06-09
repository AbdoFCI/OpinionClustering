import unittest
import numpy as np
from clustring_algorithms import pic
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

    def test_create_similarities_list(self):
        data = [['بيبو', 'الخطيب', 'الاسطوره_المصريه']
            , ['الماجيكو', 'تريكه']
            , ['تريكه', 'الخطيب', 'ارهابى_القلوب']
            , ['الماجيكو', 'ابو_تريكه']]

        # similarity_methods: tag_jaccard
        Obj1 = pic.PIC(similarity_methods.tag_jaccard_similarity_method)
        np.testing.assert_array_equal(np.matrix(Obj1._create_similarity_matrix(data)), np.matrix())