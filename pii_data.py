import re


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp
    def has_us_phone(self, anonymize=False):
        # https://docs.python.org/3.9/library/re.html?highlight=subn#re.subn
        newstr, count1 = re.subn(r'\d{9}', '[us phone]', self)

        # Match a US phone number ddd-ddd-dddd ie 123-456-7890
        newstr, count2 = re.subn(r'\d{3}[-.]\d{3}[-.]\d{4}', '[us phone]', newstr)

        if anonymize:
            # Since str is immutable it's better to stay with the spec and return a new
            # string rather than modifying self
            return newstr
        else:
            # Keep the original requirement in place by returning True or False if
            # a us phone number was present or not.
            return bool(count2 + count1)

    def has_email(self, anonymize=False):
        # Match a user's email
        validemail = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[email]', self)
        if anonymize:
            return validemail
        if '[email]' in validemail:
            return True
        return False

    def has_ipv4(self, anonymize=False):
        # Match an IPv4 address: num.num.num.num where num range = 0 - 255

        # [0-9]:        match numbers 0 - 9
        # [1-9][0-9]:   match numbers 10 - 99
        # 1[0-9][0-9]:  match numbers 100 - 199
        # 2[0-4][0-9]:  match numbers 200 - 249
        # 25[0-5]:      match numbers 250 - 255
        ipv4, count1 = re.subn(r'^\d{4}(\d{12})?$', '[iPv4 address]', self)

        ipv4, count2 = re.subn(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)'
                               r'{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
                               r'([^.^[0-9])*\b', '[iPv4 address]', ipv4)


        # 255.255.255.255 is already preserved for broadcasting and would be valid
        if self.__eq__('255.255.255.255') | self.__eq__('0.0.0.0'):
            if anonymize:
                return self
            return False
        elif anonymize:
            if count1 == 0 and count2 == 0:
                return self
            return ipv4
        return bool(count2 + count1)

    def has_ipv6(self, anonymize=False):

        ipv6, count = re.subn(r'((\w((?:[0-9a-fA-F]?){0,4}:)|(:)){7}((?:[0-9a-fA-F]?){0,4}))([^:[0-9a-fA-F]])*',
                              '[iPv6 address]', self)

        ipv6, count0 = re.subn(r'((\w((?:[0-9a-fA-F]?){0,4}:)|(:)){7}((?:[0-9a-fA-F]?){0,4}))([^:[0-9a-fA-F]])*',
                               '[iPv6 address]', ipv6)
        if self.__eq__('0:0:0:0:0:0:0:0') | self.__eq__(':::::::'):
            if anonymize:
                return "Invalid address"
            return False
        elif anonymize:
            if count == 0 and count0 == 0:
                return "Invalid address"
            if '[iPv6 address]' in ipv6 or ' [iPv6 address]' in ipv6 or '[iPv6 address] ' in ipv6 or ' [iPv6 address] '\
                    in ipv6:
                return ipv6
            else:
                count = 0
                count0 = 0
                return "Invalid address"
        return bool(count + count0)


    def has_name(self, anonymize=False):
        # match the user's name
        match = re.sub(r'^[A-Z][a-z]+\s[A-Z][a-z]+', '[name]', self)
        if anonymize:
            return match
        else:
            if '[name]' in match:
                return True
        return False

    def has_street_address(self, anonymize=False):
        # match the user's address
        match = re.sub(r'^[0-9]{3,4}\s[a-zA-Z]{2,}\s[a-zA-Z]{2,}', '[street address]', self)
        if anonymize:
            return match
        else:
            if '[street address]' in match:
                return True
        return False


    def has_credit_card(self):
        # match a standard credit card number
        match = re.search(r'\d{4}-\d{4}-\d{4}-\d{4}', self)
        if match:
            return True
        return False

    def has_at_handle(self):
        # search "@"
        return True if re.search(r'(^|\s)@[\w._%+-]+', self) else False

    def has_ssn(self):
        return True if re.search(r'\d{3}-\d{2}-\d{4}', self) else False

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or \
               self.has_street_address() or self.has_credit_card() or self.has_at_handle() or self.has_ssn()


def read_data(filename: str):
    data = []
    with open(filename) as f:
        # Read one line from the file stripping off the \n
        for line in f:
            data.append(line.rstrip())
    return data


if __name__ == '__main__':
    data = read_data('sample_data.txt')
    print(data)
    print('---')
    num = Pii('123-123-1234')
    pii_data = Pii('My phone number is ' + num.has_us_phone(True))
    print(pii_data)

    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')
