import unittest
from distance_measurement_algorithms.similarity_methods import *

class TestDistanceMeasurementAlgorithms(unittest.TestCase):

    def test_tag_jaccard_similarity_method_1(self):
        """
        jaccord similarity len intersection/union

        :return:
        """
        list1 = ['tag1','tag2']
        list2 = ['tag1','tag3']
        self.assertEqual(tag_jaccard_similarity_method(list1,list2), 0.3333333333333333)

    def test_tag_jaccard_similarity_method_2(self):
        list1 = ['tag4','tag2']
        list2 = ['tag1','tag3']
        self.assertEqual(tag_jaccard_similarity_method(list1,list2),0)

    def test_tag_jaccard_similarity_method_3(self):
        list1 = ['tag1','tag3']
        list2 = ['tag1','tag3']
        self.assertEqual(tag_jaccard_similarity_method(list1,list2),1)

#============================================================================================

    def test_character_jaccard_similarity_method_1(self):
        """
        char base jaccord similarity char level
        :return:
        """
        list1 = ['tag1','tag3']
        list2 = ['tag1','tag3']
        self.assertEqual(character_jaccard_similarity_method(list1,list2), 1)

    def test_character_jaccard_similarity_method_2(self):
        list1 = ['tag2','tag3']
        list2 = ['tag1','tag3']
        self.assertEqual(character_jaccard_similarity_method(list1,list2),4/6)

    def test_character_jaccard_similarity_method_3(self):
        """
        char list1 => {a,g,h,s,t}
        char list2 => {a,i,p,n,t}
        :return:
        """
        list1 = ['tag','hash']
        list2 = ['opinion','data']
        self.assertEqual(character_jaccard_similarity_method(list1,list2),.2)

    def test_edit_distance_method_1(self):
        list1 = ['tag1', 'tag3']
        list2 = ['tag1', 'tag3']
        self.assertEqual(edit_distance_method(list1, list2), 0)

    def test_edit_distance_method_2(self):
        list1 = ['tag2', 'tag3']
        list2 = ['tag1', 'tag3']
        self.assertEqual(edit_distance_method(list1, list2), 1)

    def test_edit_distance_method_2(self):
        list1 = ['tag','hash']
        list2 = ['opinion','data']
        self.assertEqual(edit_distance_method(list1, list2), 10)


if __name__ == '__main__':
    unittest.main()

