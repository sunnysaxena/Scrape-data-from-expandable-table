# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import requests

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

# set webdriver path here it may vary
driver = webdriver.Chrome('./chromedriver')

url = "https://indiarailinfo.com/trains/passenger/0/0/0/0"

driver.get(url)
main = []


def process_divs(all_line, l):
    for i in range(l):

        one = all_line[i]

        a = []

        for o in one:
            a.append(o.text)

        fill = []

        for aa in a:
            if aa == "":
                fill.append('NULL')
            else:
                fill.append(aa)

        main.append(fill)


count = 0

while True:
    try:

        if not driver.find_element_by_class_name('nextbtn'):
            break
        next_btn = driver.find_element_by_class_name('nextbtn')

        next_btn.click()

        url = 'https://indiarailinfo.com/trains/passenger/0/' + str(count) + '/0/0'

        print(url)

        page = requests.get(url)

        # soup = BeautifulSoup(r.content, 'html5lib')
        soup = BeautifulSoup(page.text, 'html.parser')

        data = soup.find('div', attrs={'class': 'srhres newbg inline alt'})

        all_line = data.find_all('div', attrs={'style': 'line-height:20px;'})
        length = len(all_line)

        process_divs(all_line, length)

        col = ['No', 'Name', 'Type', 'Zone', 'TTChange', 'Date From', 'Date To', 'From', 'Dep', 'To', 'Arr',
               'Duration', 'Halts', 'Dep Days', 'Classes', 'Distance', 'Speed', 'Return']

        # Create the pandas DataFrame
        df = pd.DataFrame(main, columns=col)

        df.to_csv('railway_data.csv')

        print(df)

        print('\nPage No ... ' + str(count))
        count += 1

    except NoSuchElementException as ae:
        print('Next page does not exists')
        driver.close()

driver.close()