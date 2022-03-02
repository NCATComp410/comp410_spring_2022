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
                         'Aggie Bred',
                         'Move forward with purpose',
                         'GO Aggie!',
                         'Aggie Pride']

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
        # TODO discuss changing requirements to support this
        test_data = Pii('My phone number is 970.555.1212')
        self.assertFalse(test_data.has_us_phone())

    def test_has_email(self):
        test_data = Pii('My email is user@domain.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is user.name@domain.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is user@domain.site.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is userdomain.com')
        self.assertEqual(test_data.has_email(), False)

    def test_has_ipv4(self):

        #Valid ip address
        test_data = Pii('This is an IP address: 192.142.42.32')
        self.assertTrue(test_data.has_ipv4())

        # Valid ip Address
        test_data = Pii('This is an IP address: 1.1.1.1')
        self.assertTrue(test_data.has_ipv4())

        # Incomplete address
        test_data = Pii('This is an IP address: 142.42.32')
        self.assertFalse(test_data.has_ipv4())

        # Non numbers in ip address
        test_data = Pii('This is an IP address: 1.X.X.1')
        self.assertFalse(test_data.has_ipv4())

    def test_has_ipv6(self):
        test_data = Pii()
        self.assertEqual(test_data.has_ipv6(), None)

    def test_has_name(self):
        test_data = Pii('My name is Alexander Hamilton.')
        self.assertTrue(test_data.has_name())

        test_data = Pii("His name is Marc'o O'Reilly-Villa.")
        self.assertTrue(test_data.has_name())

        test_data = Pii('Her name is Janet jackson.')
        self.assertFalse(test_data.has_name())

        test_data = Pii("Their name is not in this test.")
        self.assertFalse(test_data.has_name())
        
    def test_has_street_address(self):
        test_data = Pii()
        self.assertEqual(test_data.has_street_address(), None)

    def test_has_credit_card(self):
        # Test a valid credit card number
        test_data = Pii('0000-1111-2222-3333')
        self.assertTrue(test_data.has_credit_card())

        # Test a partial credit card number
        test_data = Pii('1111-2222-3333')
        self.assertFalse(test_data.has_credit_card())

        # Test an invalid credit card number
        test_data = Pii('00000-111-22-33333')
        self.assertFalse(test_data.has_credit_card())

    def test_has_at_handle(self):
        # Test a valid at handle
        test_data = Pii('My handle is @john_192')
        self.assertTrue(test_data.has_at_handle())

        # Test an invalid at handle
        test_data = Pii('My handle is @john$!')
        self.assertFalse(test_data.has_at_handle())

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), None)


if __name__ == '__main__':
    unittest.main()