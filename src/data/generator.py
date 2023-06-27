import random
import names
import string
from random_username.generate import generate_username
import random_address

# genetate password with length = 8
def password():
    pwd = ""
    for i in range(0, 8):
        charType = random.randint(0, 1)
        if charType:
            pwd += str(random.randint(0, 9))
        else:
            pwd += random.choice(string.ascii_letters)
    return pwd

# genetate phone number with length = 11
def phone():
    phoneNum = ""
    for i in range(0, 11):
        phoneNum += str(random.randint(0, 9))
    return phoneNum

# genetate mail address
def mail():
    mails = ['@gmail.com', '@yahoo.com', '@outlook.com']
    mailAdd = ''
    for i in range(random.randint(5, 15)):
        mailAdd += random.choice(string.ascii_letters)
    mailAdd += mails[random.randint(0, 2)]
    return mailAdd

def gen_date(ymin, ymax):
    date = ''
    year = random.randint(ymin, ymax)
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        last = 31
    elif month in [4, 6, 9, 11]:
        last = 30
    else:
        if year % 4 == 0:
            last = 29
        else:
            last = 28
    day = random.randint(1, last)
    if day <= 9:
        date = '0'
    if month <= 9:
        date += str(day) + '/0' + str(month) + '/' + str(year)
    else:
        date += str(day) + '/' + str(month) + '/' + str(year)
    return date


cities = ['Belgrade', 'Rome', 'Paris', 'Berlin', 'Beijing', 'Seoul', 'Tokyo', 'Istanbul', 'Toronto', 'Brasilia' , 'Abuja', 
            'Sofia', 'Cairo', 'NurSultan', 'Bangkok', 'Hanoi', 'Minsk', 'Zagreb', 'NDjamena', 'Bogota']
countries = ['Serbia', 'Italy', 'France', 'Germany', 'China', 'South Korea', 'Japan', 'Turkey', 'Canada', 'Brasil', 'Nigeria', 
             'Bulgaria', 'Egypt', 'Kazahstan', 'Thailand', 'Vietnam', 'Belarus', 'Croatia', 'Chad', 'Colombia']
ordersUsed = []

users = open('users.txt', 'w')
unm = []
for i in range(1, 5000):
    u = generate_username(1)[0]
    while u in unm:
        u = generate_username(1)[0]
        print(0)
    unm.append(u)
    users.write(unm[i - 1] + '|')                                  #username
    users.write(password() + '|')                                               #password
    users.write(names.get_first_name() + '|')                                   #first name
    users.write(names.get_last_name() + '|')                                    #last name
    users.write(phone() + '|')                                                  #phone number
    users.write(mail() + '|')                                                   #mail address
    users.write(random_address.real_random_address()['address1'] + '|')         #address
    plc = random.randint(0, 19)
    users.write(cities[plc] + '|')                                              #city
    users.write(countries[plc] + '\n')                                           #country
users.close()

orders = open('orders.txt', 'w')
i = 1
for i in range(1, 10):
    orders.write(str(i) + '|')
    orders.write(gen_date(2022, 2023) + '|')
    orders.write('normal\n')
orders.close()
ordalb = open('oa.txt', 'w')
i = 1
for i in range(1, 5000):
    ordalb.write(str(i) + '|')
    ordalb.write(str(random.randint(1, 10)) + '|')
    ordalb.write(str(random.randint(1, 246)) + '|')
    ordalb.write(unm[random.randint(0, 4998)] + '\n')
ordalb.close()


def comb(m, n, x, y, inx, mix):
    i, j = m, n
    while i < x + 1:
        while j < y + 1:
            mix.write(str(inx) + '|')
            mix.write(str(i) + '|')
            mix.write(str(j) + '\n')
            j += 1
            inx += 1
        j = n
        i += 1
    return inx
"""
mix = open('ag.txt', 'w')
inx = 1
inx = comb(1, 1, 3, 8, inx, mix)
inx = comb(4, 9, 6, 16, inx, mix)
inx = comb(7, 17, 9, 24, inx, mix)
inx = comb(10, 25, 12, 33, inx, mix)
inx = comb(13, 34, 13, 42, inx, mix)
inx = comb(14, 43, 15, 51, inx, mix)
inx = comb(16, 52, 18, 54, inx, mix)
inx = comb(19, 55, 20, 57, inx, mix)
inx = comb(21, 58, 23, 60, inx, mix)
inx = comb(24, 61, 25, 61, inx, mix)
inx = comb(26, 62, 27, 62, inx, mix)
inx = comb(28, 63, 29, 63, inx, mix)
inx = comb(30, 64, 31, 64, inx, mix)
inx = comb(32, 65, 34, 65, inx, mix)
inx = comb(35, 66, 37, 66, inx, mix)
inx = comb(38, 67, 40, 70, inx, mix)
inx = comb(41, 71, 42, 74, inx, mix)
inx = comb(43, 75, 44, 78, inx, mix)
inx = comb(45, 79, 46, 86, inx, mix)
inx = comb(47, 87, 48, 94, inx, mix)
inx = comb(49, 95, 49, 102, inx, mix)
inx = comb(50, 103, 51, 103, inx, mix)
inx = comb(52, 104, 53, 104, inx, mix)
inx = comb(54, 105, 55, 105, inx, mix)
inx = comb(56, 106, 56, 110, inx, mix)
inx = comb(57, 111, 57, 111, inx, mix)
inx = comb(58, 112, 58, 112, inx, mix)
inx = comb(59, 113, 59, 113, inx, mix)
mix.close()"""