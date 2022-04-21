import unittest
from pii_data import read_data, write_data
from pii_data import Pii
import os


class DataTestCases(unittest.TestCase):
    def test_write_data(self):
        # Create some expected data to write
        expected = ['this', 'is', 'some', 'test', 'data']
        # Write the data
        count = write_data('test_write_data.txt', expected)

        # Check to make sure the count was correct
        self.assertEqual(count, len(expected))

        # Check to make sure the data was written correctly
        actual = []
        with open('test_write_data.txt') as f:
            for line in f.readlines():
                actual.append(line.rstrip())
        self.assertEqual(expected, actual)

        # clean-up the test file
        os.remove('test_write_data.txt')

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
        test_data = Pii()
        self.assertEqual(test_data.has_ipv4(), None)

    def test_has_ipv6(self):
        test_data = Pii()
        self.assertEqual(test_data.has_ipv6(), None)

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
