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
        test_data = Pii('My phone number is 970.555.1212')
        self.assertTrue(test_data.has_us_phone())

    def test_has_account_number(self):
        # Test a valid US phone number
        test_data = Pii('My account number is 12-123456')
        self.assertTrue(test_data.has_account_number())

        # Test a partial US phone number
        test_data = Pii('My number is 789-889745')
        self.assertTrue(test_data.has_account_number())

        # Test a phone number with incorrect delimiters
        test_data = Pii('My phone number is 970.555.1212')
        self.assertFalse(test_data.has_account_number())


    def test_has_us_phone_anonymize(self):
        # Valid Cases
        self.assertEqual(Pii('My phone number is 97-789456').has_us_phone(anonymize=True),
                         'My account number is [account number]')
        # period delimiter
        self.assertEqual(Pii('My phone number is 56-765423').has_us_phone(anonymize=True),
                         'My account number is [account phone]')
        # 2 numbers in one sentence
        self.assertEqual(Pii('My phone number is 61-345678 and my other number is 85-324578').has_us_phone(anonymize=True),
                         'My phone number is [account phone] and my other number is [account phone]')
        # number at beginning of sentence
        self.assertEqual(Pii('123-1789 is not a number').has_us_phone(anonymize=True),
                         '123-1789 is not a number')

    def test_has_us_phone_anonymize(self):
        # Valid Cases
        self.assertEqual(Pii('My phone number is 970-555-1212').has_us_phone(anonymize=True),
                         'My phone number is [us phone]')
        # period delimiter
        self.assertEqual(Pii('My phone number is 970.555.1212').has_us_phone(anonymize=True),
                         'My phone number is [us phone]')
        # 2 numbers in one sentence
        self.assertEqual(Pii('My phone number is 970-555-1212 and my other number is 879-000-9889').has_us_phone(anonymize=True),
                         'My phone number is [us phone] and my other number is [us phone]')
        # number at beginning of sentence
        self.assertEqual(Pii('123-123-4567 is a number').has_us_phone(anonymize=True),
                         '[us phone] is a number')
        # Invalid Cases
        # wrong delimiter format
        self.assertEqual(Pii('My phone number is 970555-1212').has_us_phone(anonymize=True),
                         'My phone number is 970555-1212')
        # another wrong format
        self.assertEqual(Pii('My phone number is 970--555-1212').has_us_phone(anonymize=True),
                         'My phone number is 970--555-1212')
        # too few numbers
        self.assertEqual(Pii('My phone number is 970-555-1').has_us_phone(anonymize=True),
                         'My phone number is 970-555-1')
         # alpha character in number
        self.assertEqual(Pii('My phone number is 970-555-121a2').has_us_phone(anonymize=True),
                         'My phone number is 970-555-121a2')
    def test_has_email(self):
        test_data = Pii('My email is kavondean@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kavon.dean@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kxdean@aggies.ncat.edu')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kavondean.com')
        self.assertEqual(test_data.has_email(), False)

        test_data = Pii('My email is kavondeangmail.com')
        self.assertEqual(test_data.has_email(), False)

    def test_anonymize_has_email(self):
        self.assertEqual(Pii('My email is kxdean@aggies.ncat.edu').has_email(anonymize=True), 'My email is [email]')

        self.assertEqual(Pii('My email is kavondeangmail.com').has_email(anonymize=True), 'My email is kavondeangmail.com')

        self.assertEqual(Pii('My email is kavon.dean@gmail.com').has_email(anonymize=True), 'My email is [email]')


    def test_has_ipv4(self):
        test_data = Pii('My IP is 99.48.227.227')
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         'My IP is [ipv4 address]')
        test_data = Pii('192.168.168.28')
        self.assertTrue(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         '[ipv4 address]')

        test_data = Pii('My IP is 192.168.1.1')
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         'My IP is [ipv4 address]')
        # Test a partial ipv4
        test_data = Pii('My IP is 87.43.552')
        self.assertFalse(test_data.has_ipv4())
        test_data = Pii('My IP is 192.343.2')
        self.assertFalse(test_data.has_ipv4())

        # Test an ipv4 with incorrect delimiters
        # TODO discuss changing requirements to support this
        test_data = Pii('My IP is 99-48-227-227')
        self.assertFalse(test_data.has_ipv4(anonymize=False))
        test_data = Pii('My IP is 192-433-1-1')
        self.assertFalse(test_data.has_ipv4(anonymize=False))

    def test_has_ipv6(self):
        # https: // www.ibm.com / docs / en / ts3500 - tape - library?topic = functionality - ipv4 - ipv6 - address - formats
        # valid address
        test_data = Pii('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())
        # invalid - not enough segments
        test_data = Pii('2001:0db8:0001:0000:0000:0ab9:C0A8')
        self.assertFalse(test_data.has_ipv6())
        # invalid - too many colons
        test_data = Pii('2001:0db8:0001:0000:0000:0ab9:C0A8:0102:')
        self.assertTrue(test_data.has_ipv6())
        # invalid - separated by commas not colons
        test_data = Pii('2001,0db8,0001,0000,0000,0ab9,C0A8,0102')
        self.assertFalse(test_data.has_ipv6())

    def test_has_ipv6_anonymize(self):
        self.assertEqual(Pii('My ip address is 2001:0db8:85a3:0000:0000:8a2e:0370:7334').has_ipv6(anonymize=True),
                         'My ip address is [ipv6]')

    def test_anonymize_name(self):
        self.assertEqual(Pii('My name is Robert Hewey and I live on 123 Nocho Street').has_name(anonymize=True), 'My name is [name] and I live on 123 Nocho Street')
        self.assertEqual(Pii('Sean Tidale').has_name(anonymize=True), '[name]')
        self.assertEqual(Pii('789 Bob Rd is where Jack Howard lives notoriously').has_name(anonymize=True), '789 Bob Rd is where [name] lives notoriously')
        self.assertEqual(Pii('Jack Howard knows Hewbert Francis.').has_name(anonymize=True), '[name] knows [name].')

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

    def test_anonymize_has_street_address(self):
        self.assertEqual(Pii('My Street Address is 123 Ocho St').has_street_address(anonymize=True),
                         'My Street Address is [street address]')

        self.assertEqual(Pii('My Sean Tisdale and I stay at is 989 Block Blvd').has_street_address(anonymize=True),
                         'My Sean Tisdale and I stay at is [street address]')

        self.assertEqual(Pii('77989 Block Blvd is invalid').has_street_address(anonymize=True),
                         '77989 Block Blvd is invalid')

    def test_has_street_address(self):
        test_data = Pii(' 123 Addy Rd')
        self.assertEqual(test_data.has_street_address(), True)

        test_data = Pii(' 12356 Michellen Rd')
        self.assertEqual(test_data.has_street_address(), False)

        test_data = Pii(' 123 pope Blvd')
        self.assertEqual(test_data.has_street_address(), False)

        test_data = Pii(' 123 Rich Blvd')
        self.assertEqual(test_data.has_street_address(), True)

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
        test_data = Pii('@tentrell07')
        self.assertEqual(test_data.has_at_handle(), True)

        test_data = Pii('@ten07')
        self.assertEqual(test_data.has_at_handle(), True)

        test_data = Pii('t@entrell07+%-bro')
        self.assertEqual(test_data.has_at_handle(), False)

        test_data = Pii('@tent%_rellyboii')
        self.assertEqual(test_data.has_at_handle(), False)


    def test_has_ssn(self):
        test_data = Pii('My social security is 123-45-5667')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('My social security is 555-55-3456')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('My social security is 098-67-9878')
        self.assertTrue(test_data.has_ssn())

    def test_has_ssn_anonymize(self):
        test_data = Pii('My social security is 123-45-5667')
        self.assertEqual(test_data.has_ssn(anonymize=True), 'My social security is [social security number]')

        test_data = Pii('My social security is 555-55-3456')
        self.assertEqual(test_data.has_ssn(anonymize=True), 'My social security is [social security number]')

        test_data = Pii('My social security is 333-22-1111')
        self.assertEqual(test_data.has_ssn(anonymize=True), 'My social security is [social security number]')

        test_data = Pii('My social security is 777-55-1001')
        self.assertEqual(test_data.has_ssn(anonymize=True), 'My social security is [social security number]')

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), False)

if __name__ == '__main__':
        unittest.main()
