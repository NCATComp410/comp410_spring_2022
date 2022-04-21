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

    def has_email(self):
        return None

    def has_ipv4(self):
        return None

    def has_ipv6(self):
        return None

    def has_name(self):
        return None

    def has_street_address(self):
        return None

    def has_credit_card(self):
        return None

    def has_at_handle(self):
        return None

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or \
               self.has_street_address() or self.has_credit_card() or self.has_at_handle()

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
