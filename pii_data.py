import re
import requests


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
        # ipv4, count1 = re.subn(r'\d{4}(\d{12})?', '[iPv4 address]', self)

        match = re.sub(r'(^|(?<=\s))(?:\d{1,3}\.){3}\d{1,3}', "[iPv4 address]", self)
        if anonymize:
            return match
        else:
            if match != self:
                return True
        return False

    def has_ipv6(self, anonymize=False):

        ipv6, count = re.subn(r'((\w((?:[0-9a-fA-F]?){0,4}:)|(:)){7}((?:[0-9a-fA-F]?){0,4}))([^:[0-9a-fA-F]])*',
                              '[iPv6 address]', self)

        ipv6, count0 = re.subn(r'((\w((?:[0-9a-fA-F]?){0,4}:)|(:)){7}((?:[0-9a-fA-F]?){0,4}))([^:[0-9a-fA-F]])*',
                               '[iPv6 address]', ipv6)
        if self.__eq__('0:0:0:0:0:0:0:0') | self.__eq__(':::::::'):
            if anonymize:
                return self
            return False
        elif anonymize:
            if count == 0 and count0 == 0:
                return self
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
        match = re.sub(r'[A-Z][a-z]+\s[A-Z][a-z]+', '[name]', self)
        if anonymize:
            return match
        else:
            if '[name]' in match:
                return True
        return False

    def has_street_address(self, anonymize=False):
        # match the user's address
        match = re.sub(r'\d{2,4}\s[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}', '[street address]', self)
        if anonymize:
            return match
        else:
            if '[street address]' in match:
                return True
        return False

    def has_credit_card(self, anonymize=False):
        # match a standard credit card number
        valid_cc = re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}', '[credit card]', self)
        if anonymize:
            return valid_cc
        if '[credit card]' in valid_cc:
            return True
        return False

    def has_at_handle(self):
        # search "@"
        return True if re.search(r'(^|\s)@[\w._%+-]+', self) else False

    def has_ssn(self, anonymize= False):
        match = re.sub(r'\d{3}-\d{2}-\d{4}','[ssn number]', self)
        if anonymize:
            return match
        else:
            if '[ssn number]' in match:
                return True
        return False

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or \
               self.has_street_address() or self.has_credit_card() or self.has_at_handle()


def anonymize(string: str) -> str:
    result = Pii(string).has_us_phone(anonymize=True)
    result = Pii(result).has_email(anonymize=True)
    result = Pii(result).has_ipv4(anonymize=True)
    result = Pii(result).has_ipv6(anonymize=True)
    result = Pii(result).has_street_address(anonymize=True)
    result = Pii(result).has_credit_card(anonymize=True)
    result = Pii(result).has_name(anonymize=True)
    # result = Pii(result).has_at_handle(anonymize=True)
    result = Pii(result).has_ssn(anonymize=True)
    return result


# Read data from source file secured with an api key and return a list of lines
def read_data() -> list:
    # Load the API_KEY from .env file
    # https://www.datascienceexamples.com/env-file-for-passwords-and-keys/
    with open('.env') as f:
        for line in f.readlines():
            m = re.search(r'API_KEY="(\w+-\w+)"', line)
            if m:
                api_key = m.group(1)

    # Construct the URL from the API key
    url = requests.get('https://drive.google.com/uc?export=download&id=' + api_key)

    # Return the data as a list of lines
    return url.text.split('\n')


# Writes a list of strings to a local file
# Returns the number of lines that were written
def write_data(filename: str, str_list: list) -> int:
    line_count = 0
    with open(filename, 'w') as f:
        for s in str_list:
            f.write(s+'\n')
            line_count += 1
    return line_count


if __name__ == '__main__':
    # read the data from the case logs
    data = read_data()

    # anonymize the data
    for i in range(len(data)):
        data[i] = anonymize(data[i])

    # write results to a file
    write_data('case_logs_anonymized.csv', data)
