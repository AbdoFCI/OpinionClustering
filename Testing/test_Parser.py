import unittest
from semantic_tree import Parser


class TestTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Tree = Parser.Tree("E:\\root")
        print('setupClass\n')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass\n')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    def test_get_p_files(self):
        self.assertEqual(self.Tree.get_p_files(), ['E:\\root\\Arts\\Visual Art\\Cinema\\Action\\A.xlsx',
                                                   'E:\\root\\Arts\\Visual Art\\Cinema\\Comedy\\Comedy_Hashtags.xlsx',
                                                   'E:\\root\\Arts\\Visual Art\\Cinema\\Horror\\H.xlsx',
                                                   'E:\\root\\Arts\\Visual Art\\Cinema\\Romance\\Romantic_Hashtags.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\Administrators\\beboA.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\Administrators\\beboE.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\PLAYERS\\trekaA.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\PLAYERS\\trekaE.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Chelsea\\PLAYERS\\D.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Liverpool\\PLAYERS\\sala7A.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Liverpool\\PLAYERS\\sala7E.xlsx',
                                                   'E:\\root\\Sports\\Team\\foolball\\UEFA\\SPAIN\\La Liga\\FC Barcelona\\PLAYERS\\E.xlsx'])

    def test_get_p_dirs(self):
        self.assertEqual(self.Tree.get_p_dirs(), ['E:\\root\\Arts', 'E:\\root\\Sports', 'E:\\root\\Arts\\Animation Art',
                                                  'E:\\root\\Arts\\Body Art', 'E:\\root\\Arts\\Graffiti Art', 'E:\\root\\Arts\\Visual Art',
                                                  'E:\\root\\Arts\\Visual Art\\Cinema', 'E:\\root\\Arts\\Visual Art\\Cinema\\Action',
                                                  'E:\\root\\Arts\\Visual Art\\Cinema\\Adventure', 'E:\\root\\Arts\\Visual Art\\Cinema\\Comedy',
                                                  'E:\\root\\Arts\\Visual Art\\Cinema\\Horror', 'E:\\root\\Arts\\Visual Art\\Cinema\\Romance',
                                                  'E:\\root\\Arts\\Visual Art\\Cinema\\Action\\Expendables', 'E:\\root\\Sports\\Individual',
                                                  'E:\\root\\Sports\\Team', 'E:\\root\\Sports\\Individual\\Tennis', 'E:\\root\\Sports\\Team\\foolball',
                                                  'E:\\root\\Sports\\Team\\foolball\\AFC', 'E:\\root\\Sports\\Team\\foolball\\CAF',
                                                  'E:\\root\\Sports\\Team\\foolball\\CONCACAF', 'E:\\root\\Sports\\Team\\foolball\\CONMEBOL',
                                                  'E:\\root\\Sports\\Team\\foolball\\OFC', 'E:\\root\\Sports\\Team\\foolball\\UEFA',
                                                  'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1', 'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT',
                                                  'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\Morocco', 'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY',
                                                  'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\Administrators',
                                                  'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\PLAYERS', 'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\League 1', 'E:\\root\\Sports\\Team\\foolball\\UEFA\\SPAIN',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Arsenal',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Chelsea',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Liverpool',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Manchester United',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Chelsea\\PLAYERS',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\ENGLAND\\FA Premier League\\Liverpool\\PLAYERS',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\SPAIN\\La Liga', 'E:\\root\\Sports\\Team\\foolball\\UEFA\\SPAIN\\La Liga\\FC Barcelona',
                                                  'E:\\root\\Sports\\Team\\foolball\\UEFA\\SPAIN\\La Liga\\FC Barcelona\\PLAYERS'])

    def test_get_lca(self):
        self.assertEqual(self.Tree.get_lca('E:\\root\\Arts\\Visual Art\\Cinema\\Action\\A.xlsx', 'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\PLAYERS\\trekaA.xlsx'),
                                                 ['E', ':', '\\', 'r', 'o', 'o', 't', '\\'])
        self.assertEqual(self.Tree.get_lca('E:\\root\\Arts\\Animation Art', 'E:\\root\\Arts\\Visual Art\\Cinema\\Action'),
                                              ['E', ':', '\\', 'r', 'o', 'o', 't', '\\', 'A', 'r', 't', 's', '\\'])
        self.assertEqual(self.Tree.get_lca('E:\\root\\Sports\\Team\\foolball\\AFC', 'E:\\root\\Sports\\Team\\foolball\\CAF'),
                                          ['E', ':', '\\', 'r', 'o', 'o', 't', '\\', 'S', 'p', 'o', 'r', 't', 's', '\\', 'T',
                                           'e', 'a','m', '\\', 'f', 'o', 'o', 'l', 'b', 'a', 'l', 'l', '\\'])

    def test_calc_dist(self):
        self.assertEqual(self.Tree.calc_dist('E:\\root\\Arts\\Visual Art\\Cinema\\Action\\A.xlsx', 'E:\\root\\Sports\\Team\\foolball\\CAF\\ZONE 1\\EGYPT\\ELAHLY\\PLAYERS\\trekaA.xlsx'), 14)
        self.assertEqual(self.Tree.calc_dist('E:\\root\\Arts\\Animation Art', 'E:\\root\\Arts\\Visual Art\\Cinema\\Action'), 4)
        self.assertEqual(self.Tree.calc_dist('E:\\root\\Sports\\Team\\foolball\\AFC', 'E:\\root\\Sports\\Team\\foolball\\CAF'), 2)
        self.assertEqual(self.Tree.calc_dist('E:\\root\\Sports\\Team\\foolball\\AFC', 'E:\\root\\Sports\\Team\\foolball\\AFC'), 0)

    def test_find_tag_path(self):
        print("test_find_tag_path")
        pass

    def test_file_to_json(self):
        print("test_file_to_json")
        pass

class TestHashTagSimilarity(unittest.TestCase):
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

    def test_set_root(self):
        print("test_set_root")
        pass

    def test_get_path(self):
        print("test_get_path")
        pass

    def test_get_similarity(self):
        print("test_get_similarity")
        pass

    def test_get_list_similarity(self):
        print("test_get_list_similarity")
        pass

    def test_load_init(self):
        print("test_load_init")
        pass

if __name__ == '__main__':
    unittest.main()

