import re
import requests


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp
    def has_us_phone(self, anonymize= False):
    def has_us_phone(self, anonymize=False):
        # Match a US phone number ddd-ddd-dddd ie 123-456-7890
        match = re.sub(r'(\d{3}-\d{3}-\d{4})|(\d{10})', '[us phone]', self)

        if anonymize:
            return match
        else:
            return True if match != self else None


    def has_email(self, anonymize= False):
        match = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.]{2,}\b','[email address]', self)

        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_ipv4(self, anoymize= False):
        # Match all forms of IPv4
        match = re.sub("(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])","[IPv4 address]", self)

        if anoymize:
            return match
        else:
            return True if match != self else None

    def has_ipv6(self, anonymize=False):
        # Match all forms of IPv6
        match = re.sub("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", "[IPv6 address]",self)

        if anonymize:
            return match
        else:
            return True if match != self else None

    def has_name(self, anonymize=False):
        match = re.sub(r'\b([A-Z]{1}[a-z]+\s{1})([A-Z]{1}[a-z]+)\b','[name]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None

        m, c = re.subn(r'\d{3}-\d{3}-\d{4}', '[us phone]', self)
        if anonymize:
            return m
        return bool(c)

    def has_street_address(self, anonymize=False):
        match = re.sub(r'\d{0,9}\s{1}\b([A-Z]{1}[a-z]+\s{1})([A-Z]{1}[a-z]+)\b','[street address]', self)
        if anonymize:
            return match
        else:
            return True if match != self else None



    def has_credit_card(self,anonymize=False):
        match = re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}','[credit card]', self)
        if anonymize:
            return match
        else:
            return True if match!= self else None

    def has_at_handle(self,anonymize=False):

        #Match @ handles for twitter
        match = re.sub(r'[\@][A-z0-9][A-z0-9.]{0,15}','[at handle]', self)
        if anonymize:
            return match
        else:
            print (match)
            return True if match!= self else None



    def has_ssn(self, anonymize= False):
        match = re.sub(r'\d{3}-\d{2}-\d{4}','[ssn number]', self)

        if anonymize:
            return match
        else:
            return True if match != self else None


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
