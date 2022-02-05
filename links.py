'''
Retrieve links for pages that contain information about covid-19 positive cases cofirmed at Japanese airports
'''
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

def main():
    dict_links_month = {}

    driver = webdriver.Chrome(ChromeDriverManager().install())

    url = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00086.html'

    # visit the url
    driver.get(url)
    # <div> containing relevant hrefs
    div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div[4]/div')))

    elements = div.find_elements_by_tag_name('a')

    links = [e.get_attribute('href') for e in elements]

    # save the retrieved link with relevant year
    dict_links_month = {'2021': links[0:7], '2020': links[7:]}

    driver.close()
    print(dict_links_month)

    return dict_links_month

# **** this is the outcome ******
dict_links_month = {'2021': ['https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00274.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00268.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00262.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00254.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00244.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00231.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00210.html'], '2020': ['https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00204.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00202.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00197.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00196.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00195.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00194.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00193.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00192.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00191.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00190.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00189.html', 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00188.html']}


if __name__ == '__main__':
    main()
