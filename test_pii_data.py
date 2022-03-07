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

    def test_has_us_phone_anonymize(self):
        # Test a valid US phone number
        test_data = Pii('My phone number is 970-555-1212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),'My phone number is [phone number]')
        # Test a valid US phone number
        test_data = Pii('My phone number is 9705551212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),'My phone number is [phone number]')

        # Test a partial US phone number
        test_data = Pii('My number is 555-1212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),'My number is 555-1212')

        # Updated to allow for this entry
        test_data = Pii('My phone number is 970.555.1212')
        self.assertEqual(test_data.has_us_phone(anonymize=True),'My phone number is [phone number]')

    def test_has_email(self):
        test_data = Pii()
        self.assertEqual(test_data.has_email(), None)

    def test_has_ipv4(self):
        #Successful test cases
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

    def test_has_name(self):
        test_data = Pii('My name is Alex Red')
        self.assertEqual(test_data.has_name(), True)
        test_data = Pii('William Dane')
        self.assertEqual(test_data.has_name(), True)
        test_data = Pii('kate')
        self.assertEqual(test_data.has_name(), None)
        test_data = Pii('rodger samson')
        self.assertEqual(test_data.has_name(), None)

    def test_has_street_address(self):
        test_data = Pii('My house is at 123 Chesnut Steet')
        self.assertEqual(test_data.has_street_address(), True)
        test_data = Pii('1235 Willow Way')
        self.assertEqual(test_data.has_street_address(), True)
        test_data = Pii('Raden Lane')
        self.assertEqual(test_data.has_street_address(), None)
        test_data = Pii('1345 chesnut steet')
        self.assertEqual(test_data.has_street_address(), None)

    def test_has_credit_card(self):
        test_data = Pii('1929-1228-3455-3454')
        self.assertTrue(test_data.has_credit_card())
        test_data = Pii('2345-4567-5678-6789')
        self.assertTrue(test_data.has_credit_card())
        test_data = Pii('2345-1324-3456-1234')
        self.assertTrue(test_data.has_credit_card())
        test_data = Pii('5678-2349-7654-6435')
        self.assertTrue(test_data.has_credit_card())

        # Amex card case
        test_data = Pii('1234-123456-12345')
        self.assertTrue(test_data.has_credit_card())

        # bad symbol
        test_data = Pii('3456=1234=5678=6789')
        self.assertFalse(test_data.has_credit_card())
        # missing symbol
        test_data = Pii('1234764598764567')
        self.assertFalse(test_data.has_credit_card())

    def test_has_at_handle(self):
        test_data = Pii('My social media is handle @tonicarr')
        self.assertEqual(test_data.has_at_handle(), True)
        test_data = Pii('My social media is tonicarr')
        self.assertEqual(test_data.has_at_handle(), None)

    def test_has_ssn(self):
        test_data = Pii('123-45-5667')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('654-45-3456')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('098-67-9878')
        self.assertTrue(test_data.has_ssn())

        test_data = Pii('098.67.9878')
        self.assertFalse(test_data.has_ssn())
        test_data = Pii('098679878')
        self.assertFalse(test_data.has_ssn())
        test_data = Pii('098-6-9878')
        self.assertFalse(test_data.has_ssn())

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), None)



if __name__ == '__main__':
    unittest.main()
 