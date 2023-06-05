# -*- coding: utf-8 -*-

"""
******** LinkedIn Scraping Process *******************************************************
                                                                                         *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai        *
Input: Job listing URL from user                                                         * 
Scraping Method: Selenium and Beautiful Soup                                             *   
Output:  Job Title, Company, Location, Job Description, Extracted Keywords, Company Logo *   
                                                                                         *
******************************************************************************************

"""


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time
#import pandas as pd
from password_decrypt import decrypt
from jd_tf_idf import get_keywords
import numpy as np




def scrapeLinkedIn(url):
    print("LinkedIn", end = '')
    # Selenium Tutorial: https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/
    
    s=Service(ChromeDriverManager().install())
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    driver = webdriver.Chrome(service = s, options=op)
    #driver = uc.Chrome(options = op)
      
    # Logging into LinkedIn
    driver.get("https://linkedin.com/uas/login")
    time.sleep(np.random.randint(5,10))
    print(".", end = '')  
    username = driver.find_element("id","username")
    username.send_keys(decrypt()[0])  # Email Address
      
    pword = driver.find_element("id","password")
    pword.send_keys(decrypt()[1])        # Password
      
    driver.find_element("xpath","//button[@type='submit']").click()
    
    print(".", end = '')
    
    driver.get(url) 
    src = driver.page_source

    html = BeautifulSoup(src, 'lxml')

    # Extracting Elements
    title_el = html.find("h1", class_ = ["t-24 t-bold jobs-unified-top-card__job-title", "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"])
    company_el = html.find("span", class_ = ["jobs-unified-top-card__company-name", "topcard__flavor"])
    loc_el = html.find("span", class_ = ["jobs-unified-top-card__bullet","topcard__flavor topcard__flavor--bullet"])
    logo_el = html.find("img", class_ = ["lazy-image ember-view EntityPhoto-square-3 mb3", "artdeco-entity-image artdeco-entity-image--square-3 sub-nav-cta__image", "artdeco-entity-image artdeco-entity-image--square-5", "artdeco-entity-image artdeco-entity-image--square-5 lazy-loaded", "artdeco-entity-image artdeco-entity-image--square-3 sub-nav-cta__image lazy-loaded"])
    jd_el = html.find('div', class_= ['jobs-unified-description__content', 'show-more-less-html__markup'])
    print(".", end = '')
    try:
        title = title_el.get_text().strip()
    except Exception as e:
        title = "Attribute Error"
        print(str(e))
    try:
        company = company_el.get_text().strip()
    except Exception as e:
        company = "Attribute Error"
        print(str(e))
    try:
        loc = loc_el.get_text().strip()
    except Exception as e:
        loc = "Attribute Error"
        print(str(e))
    
    try:
        jd = jd_el.get_text().strip()
    except:
        jd = "Attribute Error"
    try:
        jd = jd_el.get_text().strip()
    except:
        jd = "Attribute Error"
    try: 
        logo = logo_el["src"]
    except Exception as e:
        print(e)
        logo = "Attribute Error"
        
    keywords = get_keywords(title + " " + jd)
    driver.close()    
    print("Executed")
    return html, title, company, loc, jd, keywords, logo

if __name__ == '__main__':
    html1, title, company, loc, jd, keywords, logo = scrapeLinkedIn("https://www.linkedin.com/jobs/view/3270040917")
    print(logo)