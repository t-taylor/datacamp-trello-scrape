import sys
import requests as rq
import pandas as pd
from trello import TrelloClient as tc
from bs4 import BeautifulSoup as bs

def _get_courses():
    page = rq.get('https://www.datacamp.com/courses/all')
    stat = str(page.status_code)
    print('Status: ' + stat)
    if stat != '200':
        return
    soup = bs(page.content, 'html.parser')
    course_blocks = soup.find_all(class_='course-block')
    
    df = pd.DataFrame([], columns=['Name', 'Type', 'Description','Link'])
    for course in course_blocks:
        name = str(list(course.children)[1].find(class_='course-block__title').get_text())
        desc = str(list(course.children)[1].find(class_='course-block__description').get_text())[11:].replace('\n', '')
        link = 'https://www.datacamp.com' + str(list(course.children)[1].get('href'))
        type_ = str(list(course.children)[1].find_all('div',
            class_= lambda value: value and value.startswith(
                'course-block__technology'))[0]).replace(
                        '<div class=\"course-block__technology course-block__technology--', '').replace(
                                '\"></div>', '')
                         #Okay, this is pretty bad but it 
                         #means I don't have to import re at least

        df = df.append(pd.DataFrame([[name, type_, desc, link]], columns=['Name', 'Type', 'Description', 'Link']))
    return(df.reset_index(drop=True))
    
def update_progress():
    return None


def _get_tclient(creds='api.xml'):
    hand = open(creds).read()
    soup = bs(hand, 'lxml')
    client = tc(
            api_key=soup.find('key').get_text(),
            api_secret=soup.find('secret').get_text(),
            token=soup.find('token').get_text())
    return client

def _add_card(pl, rl, ol, row, board):
    type_ = row['Type']
    l = ol
    if type_ == 'python':
        l = pl
    elif type_ == 'r':
        l = rl

    dupe = False
    for c in board.all_cards():
        if c.name == row['Name']:
            #duplicate so don't add
            dupe = True
    if not(dupe):
        l.add_card(row['Name'], row['Description'] + '\n' + row['Link'])

def populate_all_courses(client=_get_tclient()):
    cb = None
    for b in client.list_boards():
        if b.name == 'All DC Courses':
            cb = b

    lists = cb.open_lists()
    pl = None
    rl = None
    ol = None
    for l in lists:
        if l.name == 'Python':
            pl = l
        elif l.name == 'R':
            rl = l
        else:
            ol = l

    for index, row in _get_courses().iterrows():
        print(index)
        _add_card(pl, rl, ol, row, cb)

def delete_all_cards(client=_get_tclient()):
    cb = None
    for b in client.list_boards():
        if b.name == 'All DC Courses':
            cb = b
    for c in cb.all_cards():
        print(c)
        c.delete()


def main():
    delete_all_cards()
    populate_all_courses()
    #update_progress()
    #_get_courses()
    exit(0)
    
if __name__ == '__main__':
    main()
