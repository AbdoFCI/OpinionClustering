import unittest
import numpy as np
from clustring_algorithms import pic
from distance_measurement_algorithms import similarity_methods
from Entities import SparkConnection


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
        Obj = pic.PIC(similarity_methods.tag_jaccard_similarity_method,SparkConnection.SparkObject("appName"))
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (1, 3, 0.2), (2, 2, 1.0),
                                                                            (2, 3, 0.25), (2, 4, 0.3333333333333333),
                                                                            (3, 1, 0.2), (3, 2, 0.25), (3, 3, 1.0),
                                                                            (4, 2, 0.3333333333333333), (4, 4, 1.0)])

        # similarity_methods: character_jaccard
        Obj.similarity_method = similarity_methods.character_jaccard_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (1, 2, 0.4375), (1, 3, 0.5882352941176471),
                                                                            (1, 4, 0.5625), (2, 1, 0.4375), (2, 2, 1.0), (2, 3, 0.5),
                                                                            (2, 4, 0.8333333333333334), (3, 1, 0.5882352941176471),
                                                                            (3, 2, 0.5), (3, 3, 1.0), (3, 4, 0.625), (4, 1, 0.5625),
                                                                            (4, 2, 0.8333333333333334), (4, 3, 0.625), (4, 4, 1.0)])

        # similarity_methods: edit_distance
        Obj.similarity_method = similarity_methods.edit_distance_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 2, 20), (1, 3, 16), (1, 4, 19), (2, 1, 20),
                                                                            (2, 3, 21), (2, 4, 4), (3, 1, 16), (3, 2, 21),
                                                                            (3, 4, 19), (4, 1, 19), (4, 2, 4), (4, 3, 19)])

        """# similarity_methods: tree
        Obj.similarity_method = similarity_methods.tree
        #np.testing.assert_array_equal(Obj._create_similarities_list(data), )"""

        # similarity_methods: hamming
        Obj.similarity_method = similarity_methods.hamming_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (2, 2, 1.0), (2, 4, 0.47058823529411764),
                                                                            (3, 3, 1.0), (4, 2, 0.47058823529411764), (4, 4, 1.0)])

        # similarity_methods: levenshtein
        Obj.similarity_method = similarity_methods.levenshtein_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1.0), (1, 2, 0.23076923076923073), (1, 3, 0.3846153846153846),
                                                                            (1, 4, 0.2692307692307693), (2, 1, 0.23076923076923073), (2, 2, 1.0),
                                                                            (2, 3, 0.125), (2, 4, 0.7647058823529411), (3, 1, 0.3846153846153846),
                                                                            (3, 2, 0.125), (3, 3, 1.0), (3, 4, 0.20833333333333337),
                                                                            (4, 1, 0.2692307692307693), (4, 2, 0.7647058823529411),
                                                                            (4, 3, 0.20833333333333337), (4, 4, 1.0)])

        # similarity_methods: jaro_winkler
        Obj.similarity_method = similarity_methods.jaro_winkler_similarity_method
        np.testing.assert_array_equal(Obj._create_similarities_list(data), [(1, 1, 1), (1, 2, 0.5160256410256411), (1, 3, 0.6305304172951232),
                                                                            (1, 4, 0.5696958270487683), (2, 1, 0.5160256410256411), (2, 2, 1),
                                                                            (2, 3, 0.540954415954416), (2, 4, 0.9529411764705882),
                                                                            (3, 1, 0.6305304172951232), (3, 2, 0.540954415954416), (3, 3, 1),
                                                                            (3, 4, 0.5502822341057635), (4, 1, 0.5696958270487683),
                                                                            (4, 2, 0.9529411764705882), (4, 3, 0.5502822341057635), (4, 4, 1)])