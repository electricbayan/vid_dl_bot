import csv


my_miney = 1000
d = {}
with open('wares.csv', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=';')
    for i in reader:
        d[i[0]] = int(i[1])
for i in d.keys():

