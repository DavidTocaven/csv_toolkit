import unittest

from generate_diff_list import split_name_surname



class TestStringMethods(unittest.TestCase):
    def test_split(self):
        eleve = [{"Élève": "POTTER Harry",
                  "Sortie": ""}]
        eleve_split = [{"Nom": "POTTER",
                        "Prénom": "Harry",
                        "Sortie": ""}]
        split_name_surname(eleve, "Élève")
        self.assertEqual(eleve_split, eleve)

    # def test_isupper(self):
    #     self.assertTrue('FOdO'.isupper())
    #     self.assertFalse('Fcoo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    unittest.main()
