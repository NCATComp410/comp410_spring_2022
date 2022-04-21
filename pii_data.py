import re
import requests


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp
    def has_us_phone(self, anonymize=False):
        # Match a US phone number ddd-ddd-dddd ie 123-456-7890
        m, c = re.subn(r'\d{3}-\d{3}-\d{4}', '[us phone]', self)
        if anonymize:
            return m
        return bool(c)

    def has_email(self, anonymize = False):
        #Match a typical email string@string.string
        match = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9]{2,}\b',"[email address]",self)
        if anonymize:
            return match
        else:
            if match != self:
                return True
        return False

    def has_ipv4(self, anonymize = False):
        # Match a typical ipv4 address
        match = re.sub(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', "[ipv4 address]", self)
        if anonymize:
            return match
        else:
            if match != self:
                return True
        return False

    def has_ipv6(self, anonymize = False):
        # Match a IPv6 address
        match = re.sub(r'(^(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?:'
                           r'(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?:'
                           r'(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?:'
                           r'(\b[0-9a-fA-F]{0,4}\b)?:(\b[0-9a-fA-F]{0,4}\b)?$)', '[IPv6 address]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_name(self, anonymize = False):
        # Match a name that is capitalized
        match = re.sub(r'[A-Z][a-zA-Z\-\']+\s[A-Z][a-zA-Z\-\']+', "[name]", self)
        if anonymize:
            return match
        else:
            if match != self:
                return True
        return False

    def has_street_address(self, anonymize = False):
        match = re.sub(r'^[0-9]{1,5}\s[a-zA-Z]{2,}\s[a-zA-Z]{2,}', '[street address]', self)

        if anonymize:
            return match
        else:
            if '[street address]' in match:
                return True
        return False

    def has_credit_card(self):
        # Match a credit card number dddd-dddd-dddd-dddd
        match = re.search(r'(\d{4}-\d{4}-\d{4}-\d{4})', self)
        if match:
            return True
        return None

    def has_at_handle(self):
        match = re.search(r'[@][A-Za-z0-9_]+$', self)
        if match:
            return True
        return None

    def has_ssn(self, anonymize= False):
        newstr = re.sub(r'\d{3}-\d{2}-\d{4}','[ssn number]', self)
        if anonymize:
            return newstr
        else:
            return True if newstr != self else None

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or \
               self.has_street_address() or self.has_credit_card() or self.has_at_handle() or self.has_ssn()

    def anonymize(self):
        return self.has_us_phone(anonymize=True)


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
        data[i] = Pii(data[i]).anonymize()

    # write results to a file
    write_data('case_logs_anonymized.csv', data)
