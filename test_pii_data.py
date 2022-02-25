import unittest
from pii_data import read_data


class DataTestCases(unittest.TestCase):
    def test_read_data(self):
        expected_data = ['Aggie Pride Worldwide',
                         'Aggies Do', 
                         'Aggie Strong!',
                         'Go Aggies',
                         'And Thats on 1891',
                         "Let's Go Aggies",
                         'Never Ever Underestimate an Aggie',
                         'Every Day The Aggie Way',
                         'Can I get an Aggie Pride',
                         'Aggies Do ^2']

        data = read_data('sample_data.txt')

        self.assertEqual(data, expected_data)
def test_has_email(self):
    test_data = Pii('My email is kaylahen2019@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is martin.complex@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is classof2023@aggies.ncat.edu')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is computerscience.com')
        self.assertEqual(test_data.has_email(), None)

        test_data = Pii('My email is engineering1gmail.com')
        self.assertEqual(test_data.has_email(), None)

if __name__ == '__main__':
    unittest.main()
