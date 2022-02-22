import re


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp
    def has_us_phone(self):
        # Match a US phone number ddd-ddd-dddd ie 123-456-7890
        match = re.search(r'\d{3}-\d{3}-\d{4}', self)
        if match:
            return True
        return False

    def has_email(self):
        return None

    def has_ipv4(self):
        match = re.search(r'\d{2}\.\d{2}\.\d{3}\.\d{3}', self)
        if match:
            return True
        return False

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

    pii_data = Pii('My phone number is 123-123-1234')
    print(pii_data)
    
    pii_data = Pii('My IPv4 is 99.48.227.227')
    print(pii_data)

    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')
