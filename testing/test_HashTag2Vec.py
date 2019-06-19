import unittest
import numpy as np
from tag2vec import hashtag2vec


class TestHashTag2Vec(unittest.TestCase):
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

    def test_sum_matrix(self):
        np.testing.assert_array_equal(hashtag2vec.sum_matrix(np.matrix([[1, 2], [3, 4]])), np.matrix([[4, 6]]))
        np.testing.assert_array_equal(hashtag2vec.sum_matrix(np.matrix([[-1, -2], [3, 4]])), np.matrix([[2, 2]]))
        np.testing.assert_array_equal(hashtag2vec.sum_matrix(np.matrix([[-1, -2], [-3, -4]])), np.matrix([[-4, -6]]))
        np.testing.assert_array_equal(hashtag2vec.sum_matrix(np.matrix([[1.5, 2.5], [3.5, 4.5]])), np.matrix([[5, 7]]))

    def test_avr_matrix(self):
        np.testing.assert_array_equal(hashtag2vec.avr_matrix(np.matrix([[1, 2], [3, 4]])), np.matrix([[2, 3]]))
        np.testing.assert_array_equal(hashtag2vec.avr_matrix(np.matrix([[-1, -2], [3, 4]])), np.matrix([[1, 1]]))
        np.testing.assert_array_equal(hashtag2vec.avr_matrix(np.matrix([[-1, -2], [-3, -4]])), np.matrix([[-2, -3]]))
        np.testing.assert_array_equal(hashtag2vec.avr_matrix(np.matrix([[1.5, 2.5], [3.5, 4.5]])), np.matrix([[2.5, 3.5]]))

    def test_train(self):
        print("test_train")
        pass

    def test_permutation(self):
        self.assertEqual(hashtag2vec.HashTag2Vec._permutation([""]), [""])
        self.assertEqual(hashtag2vec.HashTag2Vec._permutation([["Ali"], ["Bedo", "Hossam"]]), [['Ali'], ['Ali']])
        self.assertEqual(hashtag2vec.HashTag2Vec._permutation([["Ali"], ["Bedo", "Hossam"], ["Abdo", "Lotfy"], ["Zezo"]]),
                         [['Ali'], ['Ali'], ['Bedo', 'Hossam'], ['Bedo', 'Hossam'], ['Hossam', 'Bedo']])


    def test_flat(self):
        self.assertEqual(hashtag2vec.HashTag2Vec.flat([""]), [])
        self.assertEqual(hashtag2vec.HashTag2Vec.flat([["Ali"], ["Bedo"], ["Abdo"], ["Zezo"]]), ['Ali', 'Bedo', 'Abdo', 'Zezo'])
        self.assertEqual(hashtag2vec.HashTag2Vec.flat([["Ali"], ["Bedo", "Hossam"], ["Abdo", "Lotfy"], ["Zezo"]]),
                         ['Ali', 'Bedo', 'Hossam', 'Abdo', 'Lotfy', 'Zezo'])

    def test_op2vec(self):
        print("test_op2vec")
        pass


if __name__ == '__main__':
    unittest.main()

