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
        test_data = Pii()
        self.assertEqual(test_data.has_email(), None)

    def test_has_ipv4(self):
        # Test a valid address
        test_data = Pii('192.168.168.2')
        self.assertTrue(test_data.has_ipv4())

        # Test a reserved address
        test_data = Pii('255.255.255.255')  # for broadcasting
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('0.0.0.0')  # for default route
        self.assertFalse(test_data.has_ipv4())

        # Test an out of range address
        test_data = Pii('192.168.168.256')
        self.assertFalse(test_data.has_ipv4())

        # Test incorrect format
        test_data = Pii('192.168.168.1.2.5')  # Test address with extra digits
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('192.168')  # incomplete address
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('192..168.168.256')  # extra dot
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('.192.168.168.256')  # dot at beginning
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('192.168.168.256.')  # dot at end
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('1f2.168.168.256')  # with 'f' in place of number
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('192.168.168.$')  # with '$' in place of number
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('192,168,168,$')  # with incorrect delimiters(,)
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('1.2.3')  # incomplete address
        self.assertFalse(test_data.has_ipv4())
        # test_data = Pii('My IP address is 192.168.1.1')  # test an address embedded inside sentence
        # self.assertTrue(test_data.has_ipv4())

    def test_has_ipv6(self):
        test_data = Pii('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test a valid address
        test_data = Pii(':0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test another valid address with empty first 16 bytes
        test_data = Pii(':0db8::0000::8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test another valid address with multiple emtpy 16 byte chunks
        test_data = Pii(':::::::')
        self.assertFalse(test_data.has_ipv6())  # test a preserved address
        test_data = Pii('0:0:0:0:0:0:0:0')
        self.assertFalse(test_data.has_ipv6())  # test a preserved address
        test_data = Pii('2001:0db8:85a3:0000:0000:8a2e:0370:7334:')
        self.assertFalse(test_data.has_ipv6())  # test an invalid address with extra colon
        test_data = Pii('2001:0db8:85a3:0000:0000:8a2e')
        self.assertFalse(test_data.has_ipv6())  # test an invalid incomplete address
        test_data = Pii(':2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertFalse(test_data.has_ipv6())  # extra colon at beginning of invalid address
        test_data = Pii('G001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertFalse(test_data.has_ipv6())  # invalid characters in invalid address ('G' in first set of bytes)
        test_data = Pii('02001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertFalse(test_data.has_ipv6())  # extra digit on first 16 bytes
        test_data = Pii('2001.0db8.85a3.0000.0000.8a2e.0370.7334')
        self.assertFalse(test_data.has_ipv6())  # incorrect delimiter
        test_data = Pii('$001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertFalse(test_data.has_ipv6())  # invalid character ($) in first set of bytes


    def test_has_name(self):
        test_data = Pii()
        self.assertEqual(test_data.has_name(), None)

    def test_has_street_address(self):
        test_data = Pii()
        self.assertEqual(test_data.has_street_address(), None)

    def test_has_credit_card(self):
        test_data = Pii()
        self.assertEqual(test_data.has_credit_card(), None)

    def test_has_at_handle(self):
        test_data = Pii()
        self.assertEqual(test_data.has_at_handle(), None)

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), None)


if __name__ == '__main__':
    unittest.main()
