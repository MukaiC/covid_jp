import re
import mysql.connector

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from links import dict_links_month


def extract_data_row(tr, year):
    '''
    extract data out of a <tr> tag passed as an argument
    '''
    row = []
    # matches airport name and date, eg. 羽田（７/２）
    # pattern = re.compile(r"([一-龥ぁ-んァ-ン]+)\（(\d+/\d+)\）")
    pattern = re.compile(r"([一-龥ぁ-んァ-ン]+)\（(\d+/\d+)\）|([一-龥ぁ-んァ-ン]+)\((\d+/\d+)\)|([一-龥ぁ-んァ-ン]+)\（(\d+/\d+)\)|([一-龥ぁ-んァ-ン]+)\((\d+/\d+)\）")

    for td in tr.find_all('td'):
        text = td.text

        # remove white spaces
        text = ''.join(text.split())
        
        # add airport name and the date separately
        match = pattern.search(text)
        if match:
            if match.group(1):
                row.append(match.group(1))
                row.append(match.group(2))
            elif match.group(3):
                row.append(match.group(3))
                row.append(match.group(4))
            elif match.group(5):
                row.append(match.group(5))
                row.append(match.group(6))
            else:
                row.append(match.group(7))
                row.append(match.group(8))
        else:
            row.append(text)
        
    # add the year
    row.append(year)
    
    return tuple(row)


# *********************

def links_reports_per_month(driver, url):
    '''
    Retrieve urls of daily reports on confirmed cases in a certain month 
    '''

    driver.get(url)

    # get all links under 空港・海港検疫事例
    div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#h2_free3 + div')))

    # this one works only for July - April 2021
    # div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/div[1]/div[6]')))

    elements = div.find_elements_by_css_selector('a')
    links = [e.get_attribute('href') for e in elements]
    
    # driver.close()
    return links


def get_data_from_daily_report(driver, url, year):
    '''
    Go to a given url to a daily report and extract data on that daily report
    '''
    data = []
    # visit all links and extract info
    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # table containing info
    table = soup.find('tbody')
    
    # table_data = []
    for row in table.find_all('tr'): 
        row_data = extract_data_row(row, year)

        if row_data[0] != '事例': # skip the column headers         
            data.append(row_data)
    
    # driver.close()
    return data

    # res.extend(extract_table_data(table, year))

def save_data(data):
    # insert into table
    query = '''INSERT INTO `cases_airport_jp` (case_id, airport, date, age, gender, residence, history, symptom, year)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

    cursor.executemany(query, data)
    mydb.commit()

    print(f"{cursor.rowcount} rows inserted successfully")


def retrieve_per_month(urls, year):
    '''
    Given a list of urls for daily data for a certain month, this function retrieves data from these urls and saves in a database
    '''
    # print('*******URLS**********')
    print(f"{len(urls)} urls in total")
    # print(urls)
    for url in urls:
        data = get_data_from_daily_report(driver, url, year)
        print('*****DATA*****')
        print(url)
        print(data)

        try:
            save_data(data)
        except:
            print('******could not save*****')
            cursor.close()
            mydb.close()
            driver.close()
            exit()


def create_driver():
    
    """creates webdriver"""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


# def close_driver(driver):
#     driver.close()

def connect_to_db():
    """establishes connection to database, e.g. mydb, cursor = connect_to_db()"""

    try:
        mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        )
        cursor = mydb.cursor()
    except:
        print("**** Erro connecting to database ***")
        exit()

    return mydb, cursor

def create_db_table():
    """Creates a database and table """
    # connect to database
    mydb, cursor = connect_to_db()
    # mydb = mysql.connector.connect(
    #     host='localhost',
    #     user='root',
    # )
    # cursor = mydb.cursor()

    # create database and table
    queries = ['CREATE DATABASE IF NOT EXISTS `covid`;', 
            'USE `covid`', 
            '''CREATE TABLE IF NOT EXISTS `cases_airport_jp`(
                id INT AUTO_INCREMENT PRIMARY KEY,
                case_id INT,
                airport VARCHAR(255),
                date VARCHAR(255),
                age VARCHAR(255),
                gender VARCHAR(255),
                residence VARCHAR(255),
                history VARCHAR(255),
                symptom VARCHAR(255),
                year INT)
                ''']

    for q in queries:
        cursor.execute(q)

    print('database and table ready')
    cursor.close()
    mydb.close()



# ******************
# driver = create_driver()
# mydb, cursor = connect_to_db()

# july = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00274.html'
# july_reports = links_reports_per_month(driver, july)
# print('*****JULY******')
# print(july_reports)

# July 10-15
# reports_jul_10_15 = ['https://www.mhlw.go.jp/stf/newpage_19900.html', 'https://www.mhlw.go.jp/stf/newpage_19858.html', 'https://www.mhlw.go.jp/stf/newpage_19827.html', 'https://www.mhlw.go.jp/stf/newpage_19811.html', 'https://www.mhlw.go.jp/stf/newpage_19774.html', 'https://www.mhlw.go.jp/stf/newpage_19772.html']

# retrieve_per_month(reports_jul_10_15, '2021')

# scrape data and save it in the database between Jan and July 9th reports 2021

# June 2021
# urls_june_2021 = links_reports_per_month(driver, dict_links_month['2021'][1])
# retrieve_per_month(urls_june_2021, '2021')

# July 2021
# urls_july_2021 = links_reports_per_month(driver, dict_links_month['2021'][0])
# print()
# print(len(urls_july_2021))
# print()
# retrieve_per_month(urls_july_2021, '2021')


# May 2021
# urls_may_2021 = links_reports_per_month(driver, dict_links_month['2021'][2])
# print()
# print(len(urls_may_2021))
# print()
# retrieve_per_month(urls_may_2021, '2021')

# April 2021
# urls_april_2021 = links_reports_per_month(driver, dict_links_month['2021'][3])
# print()
# print(len(urls_april_2021))
# print()
# retrieve_per_month(urls_april_2021, '2021')

# # March 2021
# urls_march_2021 = links_reports_per_month(driver, dict_links_month['2021'][4])
# # print(urls_march_2021)
# retrieve_per_month(urls_march_2021, '2021')

# # February 2021
# urls_february_2021 = links_reports_per_month(driver, dict_links_month['2021'][5])
# print(urls_february_2021)
# retrieve_per_month(urls_february_2021, '2021')

# successfully saved up to https://www.mhlw.go.jp/stf/newpage_16860.html
# save the rest of feb 2021 as follows:
# reports feb 2021
# feb_2021_reports = ['https://www.mhlw.go.jp/stf/newpage_17047.html', 'https://www.mhlw.go.jp/stf/newpage_17038.html', 'https://www.mhlw.go.jp/stf/newpage_17008.html', 'https://www.mhlw.go.jp/stf/newpage_16975.html', 'https://www.mhlw.go.jp/stf/newpage_16924.html', 'https://www.mhlw.go.jp/stf/newpage_16919.html', 'https://www.mhlw.go.jp/stf/newpage_16905.html', 'https://www.mhlw.go.jp/stf/newpage_16878.html', 'https://www.mhlw.go.jp/stf/newpage_16870.html', 'https://www.mhlw.go.jp/stf/newpage_16860.html', 'https://www.mhlw.go.jp/stf/newpage_16796.html', 'https://www.mhlw.go.jp/stf/newpage_16771.html', 'https://www.mhlw.go.jp/stf/newpage_16740.html', 'https://www.mhlw.go.jp/stf/newpage_16727.html', 'https://www.mhlw.go.jp/stf/newpage_16730.html', 'https://www.mhlw.go.jp/stf/newpage_16705.html', 'https://www.mhlw.go.jp/stf/newpage_16701.html', 'https://www.mhlw.go.jp/stf/newpage_16665.html', 'https://www.mhlw.go.jp/stf/newpage_16646.html', 'https://www.mhlw.go.jp/stf/newpage_16622.html', 'https://www.mhlw.go.jp/stf/newpage_16606.html', 'https://www.mhlw.go.jp/stf/newpage_16601.html', 'https://www.mhlw.go.jp/stf/newpage_16592.html', 'https://www.mhlw.go.jp/stf/newpage_16562.html', 'https://www.mhlw.go.jp/stf/newpage_16526.html', 'https://www.mhlw.go.jp/stf/newpage_16496.html', 'https://www.mhlw.go.jp/stf/newpage_16477.html']

# rest_feb_reports_2021 = feb_2021_reports[10:]
# retrieve_per_month(rest_feb_reports_2021, '2021')

# # January 2021
# urls_january_2021 = links_reports_per_month(driver, dict_links_month['2021'][6])
# # print(urls_january_2021)
# retrieve_per_month(urls_january_2021, '2021')

# Successfully scraped and saved cases: Jan-Jul 2021

# sleep(3)
# driver.close()

# cursor.close()
# mydb.close()




