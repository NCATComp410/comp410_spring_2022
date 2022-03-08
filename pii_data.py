import re


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

    def has_email(self):
        return True if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9]{2,}\b', self) else None

    def has_ipv4(self):
        # the 4 values in the IP address are from 0-255 for each segment each line is 1 segment
        match = re.search(r'^\b([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b'
                          r'.\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b'
                          r'.\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b'
                          r'.\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b$', self)

        if match:
            return True
        return False

    def has_ipv6(self):
        # There are 8 avaliable chunks to place IP data also allowing for no data to be input. Covers 0-9,a-f, and A-F
        match = re.search(r'(^(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?:'
                          r'(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?:'
                          r'(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?:'
                          r'(\b[0-9A-Fa-f]{0,4}\b)?:(\b[0-9A-Fa-f]{0,4}\b)?$)', self)
        if match:
            return True
        return False

    def has_name(self):
        return True if re.search(r'[A-Z][a-z]+\s[A-Z][a-z]+', self) else None

    def has_street_address(self):
        return True if re.search(r'[0-9]+\s[A-Z][a-z]+\s[A-Z][a-z]+', self) else None

    def has_credit_card(self, anonymize=False):
        newstr = re.sub(
            r'(\d{4}-\d{4}-\d{4}-\d{4})|(\d{4}-\d{6}-\d{5})', '[credit card number]', self)
        if anonymize:
            return newstr
        else:
            return True if newstr != self else None

    def has_at_handle(self):
        match = re.search('(^|\s)@\w+', self)
        if match:
            return True
        else:
            return None

    def has_ssn(self, anonymize=False):
        newstr = re.sub(
            r'\d{3}-\d{2}-\d{4}', '[social security number]', self)
        if anonymize:
            return newstr
        else:
            return True if newstr != self else None

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or self.has_street_address() or self.has_credit_card() or self.has_at_handle() or self.has_ssn()


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
    print('----------------------------------')

    pii_data = Pii('My social media handle is @tonicarr')
    print(pii_data)

    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')
