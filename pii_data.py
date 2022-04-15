import re


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp
    def has_us_phone(self, anonymize= False):
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


def read_data(filename: str):
    data = []
    with open(filename) as f:
        # Read one line from the file stripping off the \n
        for line in f:
            data.append(line.rstrip())
    return data


if __name__ == '__main__':

    # Removed hard coded windows path.  We'll discuss this in sprint3
    # data = read_data('C:\Users\taido\comp4100\comp410_spring_2022\sample_data.txt')
    # print(data)
    # print('---')

    pii_data = Pii('My phone number is 123-123-1234')
    print(pii_data)

    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')
