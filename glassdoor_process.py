
"""
********************** Glassdoor Scraping Process ****************************************
                                                                                         *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai        *
Input: Comapny Name and Title from linkedin_process                                      * 
Scraping Method: Selenium and Beautiful Soup                                             *   
Output: Name, Website, Size, Industry, Type, Headquarters,                               *
Revenue, Founded, Rating, Recommended to a friend, Approval of CEO                       *   
                                                                                         *
******************************************************************************************

"""



# Importing package to dycrypt stored email and password
from password_decrypt import decrypt

# Importing necessary libraries
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import time
import unidecode

import sys
sys.tracebacklimit = 0

def getGlassdoor(keyword, role):
    print("Glassdoor", end = '')
    keyword = unidecode.unidecode(keyword.lower().strip().replace(' ', '%20').replace(',', '').replace('.', ''))

    # Requesting the search page
    req = Request(
        url = 'https://www.glassdoor.com/Search/results.htm?keyword='+ keyword +'&locId=1&locT=N&locName=United%20States', 
        headers = {'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    # Parsing page into beautiful soup
    bsyc = BeautifulSoup(webpage, 'html.parser')

    # Finding all links (HREF) in the HTML
    company_page = bsyc.find_all \
    ('a', class_ = 'company-tile d-flex flex-column flex-sm-row align-items-start p-std mb-sm-std css-poeuz4 css-1wh1oc8') \
    [0]['href']

    # Creating company link
    company_page = 'https://www.glassdoor.com' + company_page

    # Requesting company specific page
    req = Request(
        url = company_page, 
        headers = {'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    print(".", end = '')
    # Parsing page into beautiful soup
    bsyc = BeautifulSoup(webpage, 'html.parser')

    # Creating a buffer set and a profile set to store company details
    buffer = set()
    profile = set()

    # Two formats of storing data on the website:
    # Possibility A
    for j in \
    [i.find_all(attrs={'data-test' : 'companyDetails'}) for i in bsyc.find_all('article', id = 'MainCol')[0].find_all('div')]:
        for k in j:
            buffer.add(k)

    for i in buffer:
        for j in i.find_all('li'):
            profile.add(j.text)

    # Possibility B
    if(len(profile) == 0):
        for j in [i.text for i in bsyc.find_all('article', id = 'MainCol')[0].find_all('div')[0].find_all(class_ = 'infoEntity')]:
            profile.add(j.strip())

    # Creating a dictionary for company profile
    company_profile = {}

    company_profile['Name'] = keyword.title().strip().replace('%20', ' ')
    for i in profile:
        company_profile[i.split(':')[0]] = i.split(':')[1]

    # Getting the review page link
    review_page = 'https://www.glassdoor.com' + bsyc.find_all(class_ = "eiCell cell reviews")[0]['href']

    # Getting the link for the salary information page
    salary_page = 'https://www.glassdoor.com' + bsyc.find_all(class_ = 'eiCell cell salaries')[0]['href']

    # Requesting the reviews page
    req = Request(url = review_page, headers = {'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    bsyc = BeautifulSoup(webpage, 'html.parser')

    # Adding Company Rating
    company_profile['Rating'] = bsyc.find_all \
                (class_ = "v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large")[0].text.strip()

    # Adding recommendation metrics
    company_profile['Recommended to a friend'] = bsyc.find_all(class_ = "donut__DonutStyle__donutchart_text_val")[0].text.strip() + '%'
    company_profile['Approval of CEO'] = bsyc.find_all(class_ = "donut__DonutStyle__donutchart_text_val")[0].text.strip() + '%'

    # deleting profile variable
    del profile
    print(".", end = '')
    # Setting up Selenium Webdriver to access Salary webpage
    count = 1
    while(True):
        try:
            #print("\nGlassdoor Access: Attempt ", count)
            count += 1
            optn = webdriver.ChromeOptions()
            s = Service(ChromeDriverManager().install())
            optn.add_argument('headless')
            driver = webdriver.Chrome(service = s, options=optn)
            driver.set_window_size(1120, 1000)

            # Logging in to Glassdoor - opening the webpage
            url = 'https://www.glassdoor.com/index.htm'
            driver.get(url)
            time.sleep(10)

            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_close"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass
                
            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_svg_dash"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass

            # Finding and clicking the sign in button
            sign_in_button = driver.find_elements(By.CSS_SELECTOR, "button")[10]
            sign_in_button.click()
            time.sleep(10)

            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_close"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass
            
            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_svg_dash"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass

            # Entering Email address
            search_box = driver.find_element(By.CSS_SELECTOR, '[id="modalUserEmail"]')

            # Decypting email from the text file
            search_box.send_keys(decrypt()[0])

            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_close"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass
                
            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_svg_dash"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass

            # Entering password
            password = driver.find_element(By.CSS_SELECTOR, '[id="modalUserPassword"]')

            # Decypting password from the text file
            password.send_keys(decrypt()[1])
            time.sleep(10)

            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_svg_dash"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass

            try:
                driver.find_element(By.CSS_SELECTOR, '[class="qual_x_close"]').click()
                print("clicked")
                time.sleep(5)
            except Exception:
                pass

            # Clicking to log in
            driver.find_element(By.CSS_SELECTOR, '[class="gd-ui-button mt-std minWidthBtn css-14xfqow evpplnh0"]').click()
            time.sleep(10)
            break
        except Exception as e:
            driver.quit()
            print(".", end = '')
            if count == 2:
                print("Unable to login due to missing Password Field on website. Most posted salary is being fetched...", end='')
                d = staticGlassdoor(salary_page, company_profile)
            return d

    try:
        driver.find_element(By.CSS_SELECTOR, '[class="qual_x_close"]').click()
        print("clicked")
        time.sleep(5)
    except Exception:
        pass

    try:
        driver.find_element(By.CSS_SELECTOR, '[class="qual_x_svg_dash"]').click()
        print("clicked")
        time.sleep(5)
    except Exception:
        pass

    # Loading the salary details webpage
    driver.get(salary_page)
    time.sleep(10)
    print(".", end = '')
    # Searching for the required role
    search_box = driver.find_element("name", 'filter.jobTitleFTS')
    search_box.send_keys(unidecode.unidecode(role.lower().strip()))
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '[data-test = "ContentFiltersFindBtn"]').click()
    time.sleep(10)

    # getting the HTML page and parsing it
    src = driver.page_source
    html = BeautifulSoup(src, 'html.parser')
    driver.quit()

    # Creating Salary data dictionary
    sal_data = {}

    # Getting the salary details in a dictionary
    try:
        for i in html.find_all('article', id = 'MainCol')[0].find_all('main', class_ = 'gdGrid'):
            for j in i.find_all('div', id = 'SalariesRef'):
                for k in j.find_all(attrs={'data-test' : 'salary-list-items'}):
                    sal_data[[x.text for x in k.find_all('a', class_ = 'css-3m8p33 el6ke058')][0]] = \
                    {'Total Pay': [x.text for x in k.find_all(class_ = 'css-1yonf2x e1w3xrxr4')][0], \
                    'Base Pay': [x.text for x in k.find_all(class_ = 'd-flex align-items-center')][0].replace('\xa0','').split('|')[0], \
                    'Bonus': [x.text for x in k.find_all(class_ = 'd-flex align-items-center')][0].replace('\xa0','').split('|')[1]}
    except:
        print("Salary data for the given role is not available.")
    sal = {}
    if len(sal_data) == 0:
        sal = {}
    else:
        sal['Role'] = list(sal_data.keys())[0]
        sal = {**sal, **sal_data[list(sal_data.keys())[0]]}
        
    driver.quit()
    metrics_comp = ['Name', 'Website', 'Size', 'Industry', 'Type', 'Headquarters',
                    'Revenue', 'Founded', 'Rating', 'Recommended to a friend', 'Approval of CEO']
    for i in metrics_comp:
        company_profile.setdefault(i, 'Missing Value')
    metrics_sal = ['Role', 'Total Pay', 'Base Pay', 'Bonus']
    for i in metrics_sal:
        sal.setdefault(i, 'Missing Value')
    print("Executed")
    return {**company_profile, **sal}

def staticGlassdoor(salary_page, company_profile):
    req = Request(
        url = salary_page, 
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    
    bsyc = BeautifulSoup(webpage, "html.parser")
    
    sal_data = {}
    
    for i in bsyc.find_all('article', id = 'MainCol')[0].find_all('main', class_ = 'gdGrid'):
        for j in i.find_all('div', id = 'SalariesRef'):
            for k in j.find_all(attrs={'data-test' : 'salary-list-items'}):
                sal_data[[x.text for x in k.find_all('a', class_ = 'css-3m8p33 el6ke058')][0]] = \
                {'Total Pay': [x.text for x in k.find_all(class_ = 'css-1yonf2x e1w3xrxr4')][0], \
                'Base Pay': [x.text for x in k.find_all(class_ = 'd-flex align-items-center')][0].replace('\xa0','').split('|')[0], \
                'Bonus': [x.text for x in k.find_all(class_ = 'd-flex align-items-center')][0].replace('\xa0','').split('|')[1]}
    metrics_comp = ['Name', 'Website', 'Size', 'Industry', 'Type', 'Headquarters',
                    'Revenue', 'Founded', 'Rating', 'Recommended to a friend', 'Approval of CEO']
    sal = {}
    if len(sal_data) == 0:
        sal = {}
    else:
        sal['Role'] = list(sal_data.keys())[0]
        sal = {**sal, **sal_data[list(sal_data.keys())[0]]}

    metrics_comp = ['Name', 'Website', 'Size', 'Industry', 'Type', 'Headquarters',
                    'Revenue', 'Founded', 'Rating', 'Recommended to a friend', 'Approval of CEO']
    for i in metrics_comp:
        company_profile.setdefault(i, 'Missing Value')
    metrics_sal = ['Role', 'Total Pay', 'Base Pay', 'Bonus']
    for i in metrics_sal:
        sal.setdefault(i, 'Missing Value')
    print("Executed")
    return {**company_profile, **sal}
    