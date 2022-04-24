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

    def test_has_email(self):
        test_data = Pii('My email is kaylahen2019@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is martin.complex@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is classof2023@aggies.ncat.edu')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is computerscience.com')
        self.assertEqual(test_data.has_email(), False)

        test_data = Pii('My email is engineering1gmail.com')
        self.assertEqual(test_data.has_email(), False)

    def test_anonymize_has_email(self):
        self.assertEqual(Pii('My email is computerscience.com').has_email(anonymize=True),
                         'My email is computerscience.com')

        self.assertEqual(Pii(
            'My email is kaylahen2019@gmail.com').has_email(anonymize=True), 'My email is [email]')

        self.assertEqual(Pii(
            'My email is martin.complex@gmail.com').has_email(anonymize=True), 'My email is [email]')

        self.assertEqual(Pii('My email is engineering1gmail.com').has_email(anonymize=True),
                         'My email is engineering1gmail.com')

    def test_has_us_phone(self):
        # Test a valid US phone number
        test_data = Pii('My phone number is 970-555-1212')
        self.assertTrue(test_data.has_us_phone())
        # Test a valid US phone number
        test_data = Pii('My phone number is 9705551212')
        self.assertTrue(test_data.has_us_phone())

        # Test a partial US phone number
        test_data = Pii('My number is 555-1212')
        self.assertFalse(test_data.has_us_phone())

        # Updated to allow for this entry
        test_data = Pii('My phone number is 970.555.1212')
        self.assertTrue(test_data.has_us_phone())

    def test_has_account_number(self):
        test_data = Pii('My account number is 14-243496')
        self.assertTrue(test_data.has_account_number())
        test_data = Pii('My account number is 14-435234')
        self.assertTrue(test_data.has_account_number())
        test_data = Pii('My account number is 14.243496')
        self.assertIsNone(test_data.has_account_number())
        test_data = Pii('My account number is 14-45234')
        self.assertIsNone(test_data.has_account_number())

    def test_has_account_number_anonymize(self):
        test_data = Pii('My account number is 14-243496')
        self.assertEqual(test_data.has_account_number(
            anonymize=True), 'My account number is [account number]')
        test_data = Pii('My account number is 14-435234')
        self.assertEqual(test_data.has_account_number(
            anonymize=True), 'My account number is [account number]')
        test_data = Pii('My account number is 14.243496')
        self.assertEqual(test_data.has_account_number(
            anonymize=True), 'My account number is 14.243496')
        test_data = Pii('My account number is 14-45234')
        self.assertEqual(test_data.has_account_number(
            anonymize=True), 'My account number is 14-45234')

    def test_has_us_phone_anonymize(self):
        # Test a valid US phone number
        test_data = Pii('My phone number is 970-555-1212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),
                         'My phone number is [phone number]')
        # Test a valid US phone number
        test_data = Pii('My phone number is 9705551212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),
                         'My phone number is [phone number]')

        # Test a partial US phone number
        test_data = Pii('My number is 555-1212')
        self.assertEqual(test_data.has_us_phone(
            anonymize=True), 'My number is 555-1212')

        # Updated to allow for this entry
        test_data = Pii('My phone number is 970.555.1212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),
                         'My phone number is [phone number]')

    def test_has_ipv4(self):
        # Successful test cases
        test_data = Pii('222.33.100.12')
        self.assertTrue(test_data.has_ipv4())

        test_data = Pii('45.68.195.254')
        self.assertTrue(test_data.has_ipv4())

        # Test values are out of the range for allowed addresses
        test_data = Pii('300.22.555.256')
        self.assertFalse(test_data.has_ipv4())

        # Test wrong format
        test_data = Pii('145')  # incomplete address
        self.assertFalse(test_data.has_ipv4())

    def test_has_ipv4_an(self):
        # Successful test cases
        test_data = Pii('222.33.100.12')
        self.assertEqual(test_data.has_ipv4(anonymize=True), '[ipv4]')

        test_data = Pii('45.68.195.254')
        self.assertEqual(test_data.has_ipv4(anonymize=True), '[ipv4]')

        # Test values are out of the range for allowed addresses
        test_data = Pii('300.22.555.256')
        self.assertEqual(test_data.has_ipv4(anonymize=True), '300.22.555.256')

        # Test wrong format
        test_data = Pii('145')  # incomplete address
        self.assertEqual(test_data.has_ipv4(anonymize=True), '145')

    def test_has_ipv6(self):
        # test a valid address
        test_data = Pii('0045:Fa34:53d9:4d53:0020:0000:6491:8485')
        self.assertTrue(test_data.has_ipv6())

        test_data = Pii('0000::5248:ee43::8789:1234:1200')
        self.assertTrue(test_data.has_ipv6())

        # test an invalid address with to many digits in segment
        test_data = Pii('00000:::::')
        self.assertFalse(test_data.has_ipv6())

        # test an invalid address w letter outside of bounds
        self.assertFalse(test_data.has_ipv6())
        test_data = Pii('r445:rtyu:vd45:nmkl:af24:kb78')

    def test_has_ipv6a(self):
        # test a valid address
        test_data = Pii('0045:Fa34:53d9:4d53:0020:0000:6491:8485')
        self.assertEqual(test_data.has_ipv6(anonymize=True), '[ipv6]')

        test_data = Pii('0000::5248:ee43::8789:1234:1200')
        self.assertEqual(test_data.has_ipv6(anonymize=True), '[ipv6]')

        # test an invalid address with to many digits in segment
        test_data = Pii('00000:::::')
        self.assertEqual(test_data.has_ipv6(anonymize=True), '00000:::::')

        # test an invalid address w letter outside of bounds
        test_data = Pii('r445:rtyu:vd45:nmkl:af24:kb78')
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         'r445:rtyu:vd45:nmkl:af24:kb78')

    def test_has_name(self):
        test_data = Pii('My name is Alex Red')
        self.assertEqual(test_data.has_name(), True)
        test_data = Pii('William Dane')
        self.assertEqual(test_data.has_name(), True)
        test_data = Pii('kate')
        self.assertEqual(test_data.has_name(), None)
        test_data = Pii('rodger samson')
        self.assertEqual(test_data.has_name(), None)

    def test_has_name_anonymize(self):
        test_data = Pii('My name is Alex Red')
        self.assertEqual(test_data.has_name(
            anonymize=True), 'My name is [name]')
        test_data = Pii('William Dane')
        self.assertEqual(test_data.has_name(anonymize=True), '[name]')
        test_data = Pii('kate')
        self.assertEqual(test_data.has_name(anonymize=True), 'kate')
        test_data = Pii('rodger samson')
        self.assertEqual(test_data.has_name(anonymize=True), 'rodger samson')

    def test_has_street_address(self):
        test_data = Pii('My house is at 123 Chesnut Steet')
        self.assertEqual(test_data.has_street_address(), True)
        test_data = Pii('1235 Willow Way')
        self.assertEqual(test_data.has_street_address(), True)
        test_data = Pii('Raden Lane')
        self.assertEqual(test_data.has_street_address(), None)
        test_data = Pii('1345 chesnut steet')
        self.assertEqual(test_data.has_street_address(), None)

    def test_has_street_address_anonymize(self):
        test_data = Pii('My house is at 123 Chesnut Steet')
        self.assertEqual(test_data.has_street_address(
            anonymize=True), 'My house is at [street address]')
        test_data = Pii('1235 Willow Way')
        self.assertEqual(test_data.has_street_address(
            anonymize=True), '[street address]')
        test_data = Pii('Raden Lane')
        self.assertEqual(test_data.has_street_address(
            anonymize=True), 'Raden Lane')
        test_data = Pii('1345 chesnut steet')
        self.assertEqual(test_data.has_street_address(
            anonymize=True), '1345 chesnut steet')

    def test_has_credit_card(self):
        test_data = Pii('My credit card number is 1929-1228-3455-3454')
        self.assertTrue(test_data.has_credit_card())
        test_data = Pii('My credit card number is 2345-4567-5678-6789')
        self.assertTrue(test_data.has_credit_card())
        test_data = Pii('My credit card number is 2345-1324-3456-1234')
        self.assertTrue(test_data.has_credit_card())
        test_data = Pii('My credit card number is 5678-2349-7654-6435')
        self.assertTrue(test_data.has_credit_card())

        # Amex card case
        test_data = Pii('My credit card number is 1234-123456-12345')
        self.assertTrue(test_data.has_credit_card())

        # bad symbol
        test_data = Pii('My credit card number is 3456=1234=5678=6789')
        self.assertFalse(test_data.has_credit_card())
        # missing symbol
        test_data = Pii('My credit card number is 1234764598764567')
        self.assertFalse(test_data.has_credit_card())

    def test_has_credit_card_anonymize(self):
        test_data = Pii('My credit card number is 1929-1228-3455-3454')
        self.assertEqual(test_data.has_credit_card(
            anonymize=True), 'My credit card number is [credit card number]')
        test_data = Pii('My credit card number is 2345-4567-5678-6789')
        self.assertEqual(test_data.has_credit_card(
            anonymize=True), 'My credit card number is [credit card number]')

        # bad symbol
        test_data = Pii('My credit card number is 3456=1234=5678=6789')
        self.assertEqual(test_data.has_credit_card(
            anonymize=True), 'My credit card number is 3456=1234=5678=6789')
        # missing symbol
        test_data = Pii('My credit card number is 1234764598764567')
        self.assertEqual(test_data.has_credit_card(
            anonymize=True), 'My credit card number is 1234764598764567')

    def test_has_at_handle(self):
        test_data = Pii('My social media is handle @tonicarr')
        self.assertEqual(test_data.has_at_handle(), True)
        test_data = Pii('My social media is tonicarr')
        self.assertEqual(test_data.has_at_handle(), None)

    def test_has_at_handle_anonymize(self):
        test_data = Pii('My social media is handle @tonicarr')
        self.assertEqual(test_data.has_at_handle(anonymize=True),
                         'My social media is handle[at handle]')
        test_data = Pii('My social media is tonicarr')
        self.assertEqual(test_data.has_at_handle(
            anonymize=True), 'My social media is tonicarr')

    def test_has_ssn(self):
        test_data = Pii('My social security is 123-45-5667')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('My social security is 654-45-3456')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('My social security is 098-67-9878')
        self.assertTrue(test_data.has_ssn())

        test_data = Pii('My social security is 098.67.9878')
        self.assertFalse(test_data.has_ssn())
        test_data = Pii('My social security is 098679878')
        self.assertFalse(test_data.has_ssn())
        test_data = Pii('My social security is 098-6-9878')
        self.assertFalse(test_data.has_ssn())

    def test_has_ssn_anonymize(self):
        test_data = Pii('My social security is 123-45-5667')
        self.assertEqual(test_data.has_ssn(anonymize=True),
                         'My social security is [social security number]')
        test_data = Pii('My social security is 654-45-3456')
        self.assertEqual(test_data.has_ssn(anonymize=True),
                         'My social security is [social security number]')
        test_data = Pii('My social security is 098-67-9878')
        self.assertEqual(test_data.has_ssn(anonymize=True),
                         'My social security is [social security number]')

        test_data = Pii('My social security is 098.67.9878')
        self.assertEqual(test_data.has_ssn(anonymize=True),
                         'My social security is 098.67.9878')
        test_data = Pii('My social security is 098679878')
        self.assertEqual(test_data.has_ssn(anonymize=True),
                         'My social security is 098679878')
        test_data = Pii('My social security is 098-6-9878')
        self.assertEqual(test_data.has_ssn(anonymize=True),
                         'My social security is 098-6-9878')

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), None)


if __name__ == '__main__':
    unittest.main()
