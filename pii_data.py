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
        newstr = re.sub(
            r'(\d{3}(-|.)\d{3}(-|.)\d{4})|\d{10}', '[phone number]', self)
        if anonymize:
            return newstr
        else:
            return True if newstr != self else None

    def has_email(self, anonymize=False):
        # return True if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9]{2,}\b', self) else None
        new, count = re.subn(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.]{2,}\b', '[email]', self)

        print(new)
        print(bool(count))
        if anonymize:
            return new
        else:
            return bool(count)

    def has_ipv4(self, anonymize = False):
        # the 4 values in the IP address are from 0-255 for each segment each line is 1 segment
        match = re.sub(r'^\b([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b'
                          r'.\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b'
                          r'.\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b'
                          r'.\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b$', '[ipv4]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_ipv6(self, anonymize = False):
        # There are 8 avaliable chunks to place IP data also allowing for no data to be input. Covers 0-9,a-f, and A-F

        match = re.sub(r'(^(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?:'
                          r'(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?:'
                          r'(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?:'
                          r'(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?$)', '[ipv6]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_name(self, anonymize=False):
        namestr = re.sub(r'[A-Z][a-z]+\s[A-Z][a-z]+', '[name]', self)
        if anonymize:
            return namestr
        else:
            return True if namestr != self else None

    def has_street_address(self, anonymize=False):
        addstr = re.sub(r'[0-9]+\s[A-Z][a-z]+\s[A-Z][a-z]+', '[street address]', self)
        if anonymize:
            return addstr
        else:
            return True if addstr != self else None

    def has_credit_card(self, anonymize=False):
        newstr = re.sub(
            r'(\d{4}-\d{4}-\d{4}-\d{4})|(\d{4}-\d{6}-\d{5})', '[credit card number]', self)
        if anonymize:
            return newstr
        else:
            return True if newstr != self else None

    def has_at_handle(self, anonymize = False):
        match = re.sub('(^|\s)@\w+','[at handle]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_ssn(self, anonymize=False):
        newstr = re.sub(
            r'\d{3}-\d{2}-\d{4}', '[social security number]', self)
        if anonymize:
            return newstr
        else:
            return True if newstr != self else None

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or self.has_street_address() or self.has_credit_card() or self.has_at_handle() or self.has_ssn()

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
