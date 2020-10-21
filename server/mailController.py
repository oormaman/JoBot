import re

regex1 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,10}$'
regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{1,4}[.]\w{2,3}$'

def check_if_its_currect_mail_adress(email):
    if (re.search(regex1, email)):
        return True
    if (re.search(regex2, email)):
        return True
    return False

