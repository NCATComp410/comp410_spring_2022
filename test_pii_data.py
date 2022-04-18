import unittest
from pii_data import read_data
from pii_data import Pii


class DataTestCases(unittest.TestCase):
    def test_read_data(self):
        expected_data = ['Aggie Pride Worldwide',
                         'Aggies Do',
                         'Go Aggies',
                         'Aggie Strong!',
                         'Go Aggies',
                         'And Thats on 1891',
                         "Let's Go Aggies",
                         'Never Ever Underestimate an Aggie',
                         'Every Day The Aggie Way',
                         'Can I get an Aggie Pride',
                         'Aggies Do ^2',
                         'Aggie Pride For The Culture',
                         'We Are Aggies! We Are Proud!',
                         'Set My Future Self Up for Success!',
                         'AGGIE PRIDE!',
                         'We are Aggies',
                         'A-G-G-I-E, WHAT? P-R-I-D-E',
                         'Aggie Pride',
                         'Leaders Can Aggies Do',
                         'Mens et Manus',
                         'Aggies Aggies Aggies',
                         'Aggie Pride',
                         'Aggies are always number 1!',
                         'Because thats what Aggies do',
                         'Aggie Bred']

        data = read_data('sample_data.txt')

        self.assertEqual(data, expected_data)

    def test_has_us_phone(self):
        # Test a valid US phone number
        test_data = Pii('My phone number is 970-555-1212')
        self.assertTrue(test_data.has_us_phone())

        # Test a partial US phone number
        test_data = Pii('My number is 555-1212')
        self.assertFalse(test_data.has_us_phone())

        # Test a phone number with incorrect delimiters
        test_data = Pii('My phone number is 970.555.1212')
        self.assertTrue(test_data.has_us_phone())

    def test_has_email(self):
        test_data = Pii('My email is kavondean@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kavon.dean@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kxdean@aggies.ncat.edu')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kavondean.com')
        self.assertEqual(test_data.has_email(), None)

        test_data = Pii('My email is kavondeangmail.com')
        self.assertEqual(test_data.has_email(), None)

    def test_has_ipv4(self):
        test_data = Pii('My IP is 99.48.227.227')
        self.assertEqual(test_data.has_ipv4(), True)

        test_data = Pii('My IP is 192.168.1.1')
        self.assertEqual(test_data.has_ipv4(), True)

        # Test a partial ipv4
        test_data = Pii('My IP is 87.43.552')
        self.assertEqual(test_data.has_ipv4(), False)

        test_data = Pii('My IP is 192.343.2')
        self.assertEqual(test_data.has_ipv4(), False)

        # Test an ipv4 with incorrect delimiters
        # TODO discuss changing requirements to support this
        test_data = Pii('My IP is 99-48-227-227')
        self.assertEqual(test_data.has_ipv4(), False)

        test_data = Pii('My IP is 192-433-1-1')
        self.assertEqual(test_data.has_ipv4(), False)

    def test_has_ipv6(self):
        test_data = Pii()
        self.assertEqual(test_data.has_ipv6(), None)

    def test_has_name(self):
        #Test case for valid name
        test_data = Pii('Sean Tisdale')
        self.assertEqual(test_data.has_name(), True)

        #Test case for invalid name with number
        test_data = Pii('S3an Tisdale')
        self.assertEqual(test_data.has_name(), False)

         #Test case for invalid first name only
        test_data = Pii('Sean ')
        self.assertEqual(test_data.has_name(), False)


    def test_has_street_address(self):
        test_data = Pii()
        self.assertEqual(test_data.has_street_address(), None)

    def test_has_credit_card_anonymize(self):
        self.assertEqual(Pii('My credit card number is 9702-5552-1212-1234').has_credit_card(anonymize=True),
                         'My credit card number is [credit card]')

    def test_has_credit_card(self):
        test_data = Pii('My card is 1234-1234-1234-1234')
        self.assertTrue(test_data.has_credit_card())
        # invalid card
        test_data = Pii('My card is 123456-123456-1234-1234')
        self.assertFalse(test_data.has_credit_card())

    def test_has_at_handle(self):
        test_data = Pii()
        self.assertEqual(test_data.has_at_handle(), None)

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), None)


if __name__ == '__main__':
    unittest.main()
