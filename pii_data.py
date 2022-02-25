import re

def has_email(self, anonymize = False):
    # return True if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9]{2,}\b', self) else None
new, count = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.]{2,}\b', '[email]', self)

        print(new)
        print (bool(count))
        if anonymize:
            return new
        else:
           return bool(count)

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
    prinnt('---')

    pii_data =Pii('My email address is aggiesrule@gmail.com')
    print(pii_data)
    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')