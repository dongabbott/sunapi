import random
from datetime import datetime, timedelta, date
import os


def code_number(length=1):
    """随机取一个数字符串可以包括0开头"""
    number = []
    for n in range(length):
        number.append(str(random.randint(0, 9)))
    return ''.join(number)


def en_letter(length=1, capital=False):
    """随机英文字符串"""
    en = ''
    for n in range(length):
        letter = chr(random.randint(97, 122))
        if capital is True:
            letter = letter.upper()
        en += letter
    return en


def chinese(num=1):
    """随机生成中文字符"""
    ch = ""
    for x in range(0, int(num)):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
        val = f'{head:x}{body:x}'
        str = bytes.fromhex(val).decode('gb2312')
        ch += str
    return ch


def identity(id_number=None, age=None, gender=1):
    dist_file = os.path.join(os.path.dirname(__file__), 'districtcode.txt')
    with open(dist_file, 'rb') as f:
        codelist = [x.decode('gbk').split('\t')[0] for x in f.readlines()]
    id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]

    if not id_number:
        id_number = ('%s' % random.choice(codelist))
    if id_number and id_number not in codelist:
        return None
    if not age:
        age = random.choice(range(18, 50))

    datestring = str(date(date.today().year - age, 1, 1) + timedelta(days=random.randint(0, 364))).replace("-", "")
    rd = random.randint(0, 999)
    if gender == 0:
        gender_num = rd if rd % 2 == 0 else rd + 1
    else:
        gender_num = rd if rd % 2 == 1 else rd - 1
    result = str(id_number) + datestring + str(gender_num).zfill(3)
    b = result + str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 11])
    return b


def mobile_phone(src=131, num=1, file_path=None):
    """随机手机号，支持批量"""
    if num == 1:
        return str(src) + code_number(8)
    if num >= 1:
        members = []
        for n in range(num):
            members.append(str(src) + code_number(8))
        if file_path:
            with open(file_path, 'a') as f:
                f.write('\n'.join(members))
        else:
            return members


def email(domain='163.com', length=8):
    """随机生成电子邮箱"""
    return en_letter(length) + '@{}'.format(domain)