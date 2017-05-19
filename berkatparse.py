# coding: utf-8

import os, requests, bs4, openpyxl, time

url = 'http://212.109.217.123'
big_list = []


def itemCont(self):
    props = {}
    itemList = bs4.BeautifulSoup(str(self), "lxml")
    props.setdefault('category', itemList.select('.board_list_cat span')[0].getText())
    props.setdefault('idNum', itemList.select('.board_list_id span')[0].getText())
    if len(itemList.select('.board_list_contacts span')) == 1:
        props.setdefault('phone', itemList.select('.board_list_contacts span')[0].getText())
    else:
        props.setdefault('phone', 'nophone')
    if len(itemList.select('.board_list_contacts')) == 2:
        props.setdefault('name', itemList.select('.board_list_contacts')[1].getText().strip('\n\t'))
    else:
        props.setdefault('name', 'noname')
    if len(itemList.select('.board_list_city')) == 1:
        props.setdefault('region', itemList.select('.board_list_city')[0].getText().strip('\n\tРегион:'))
    else:
        props.setdefault('region', ' bomj')
    return props


while True:    
    try:
        res = requests.get(url)
        res.raise_for_status() # Проверка на отзыв сайта
        print('got page number %s' % url[34:])
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    soup = bs4.BeautifulSoup(res.text, "lxml")
    elems = soup.select('.board_list_footer_left')
    nexto = soup.select('.pagebar_nav a')
    for i in elems:
        big_list.append(itemCont(i))
    if len(elems) < 70:
        break
    url = 'http://212.109.217.123' + nexto[1].get('href')


contacts = openpyxl.Workbook()
sheet = contacts.get_sheet_by_name('Sheet')
for i in range(1, len(big_list)):
    sheet['a'+ str(i+1)] = big_list[i]['idNum']
    sheet['b'+ str(i+1)] = big_list[i]['region']
    sheet['c'+ str(i+1)] = big_list[i]['category']
    sheet['e'+ str(i+1)] = big_list[i]['phone']
    sheet['g'+ str(i+1)] = big_list[i]['name']
contacts.save('Contacts.xlsx')