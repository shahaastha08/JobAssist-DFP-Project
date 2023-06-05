# -*- coding: utf-8 -*-
"""
******** Indeed Resume Scraping Process ****************************************************
                                                                                           *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai          *
Input: Job Title from linkedin_process                                                     * 
Scraping Method: Selenium and Beautiful Soup                                               *   
Output: Two sample resumes from Indeed that best match the job title                       *   
                                                                                           *
********************************************************************************************

"""

#All imports
from selenium import webdriver
from bs4 import BeautifulSoup
import time
#import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.by import By

#Using fuzzywuzzy for matching
#from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from Levenshtein import jaro_winkler
#from selenium import webdriver
import pickle
#import requests
import sys

sys.setrecursionlimit(100000)


def scrapeIndeed():
    # Scrape Indeed
    
    s=Service(ChromeDriverManager().install())
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    #, options = op
    driver = webdriver.Chrome(service=s)

    driver.maximize_window()
    driver.get("https://www.indeed.com/career-advice/resume-samples")
    time.sleep(5)
    time.sleep(5)
    src = driver.page_source
    
    # Using beautiful soup to get all the role names
    soup = BeautifulSoup(src, 'lxml') 
    #s = soup.findAll("div", {"class":"css-fd7g31 eu4oa1w0"})
    roles = soup.findAll("span", {"class": "css-wl7i5v eu4oa1w0"})
    role_names =[]
    for i in roles:
        role_names.append(i.get_text())
        

    #getting href for all roles

    url_list = []
    roles = soup.findAll("a", {"class": "css-qc2xbz e8ju0x50"})
    for i in roles:
        url_list.append(i.get('href'))
        #print(url_list)

    
    #getting link for role from fuzzy logic output
    all_final_urls = []
    for i in url_list:
        all_final_urls.append("https://www.indeed.com/career-advice/"+i)
        
    
    #Scraping resumes for all the roles
    all_resumes = []
    for url in all_final_urls:
        driver.get(url)
        resume_src = driver.page_source
        resume_soup = BeautifulSoup(resume_src, 'lxml')
        all_resumes.append(resume_soup.findAll("div", {"class":"css-1bl5pna eu4oa1w0"}))
        
    #Creating a dictionary for resumes to be cached
    all_roles_resumes={}
    for i,j in zip(role_names,all_resumes):
        all_roles_resumes[i] = j
    #all_roles_resumes
    

    with open('resources/indeed_resume_cache.pickle', 'wb') as handle:
        pickle.dump(all_roles_resumes, handle, protocol=pickle.HIGHEST_PROTOCOL)

def fetch_resume(str2Match):
    
    print("Indeed.", end = '')
    with open('resources/indeed_resume_cache.pickle', 'rb') as handle:
        all_roles_resumes = pickle.load(handle)
        
    #Getting the best match for the role input by the user
    
    # Using fuzzywuzzy
    # highest = process.extractOne(str2Match,role_names)
    # print(highest)
    role_names = list(all_roles_resumes.keys())
    # Calculating Levensthein distance to find best match
    
    word_scores = [jaro_winkler(str2Match, possible) for possible in role_names]
    matched_word = role_names[word_scores.index(max(word_scores))]
    #print(matched_word)
    
    print(".", end = '')
    resume = all_roles_resumes.get(matched_word)
    html_prefix = """
    <html>
    <link href= "static/styles/main.css" rel="stylesheet" />
    <link href= "static/styles/indeed_styles.css" rel="stylesheet" />
        <div  class = "card">
	       <img class="card-img-top" src="static\media\Indeed.png" alt="Card image cap" style="width:100px;height:50px;">
		<br>

	<div >
		<h3 class="card-title">Sample Resume from Indeed</h3>
        <br>
        <br>"""
    html_suffix = """</div></div></html>"""    
        

    resume = [html_prefix + str(i)\
              + html_suffix for i in resume]
    
    f1 = open("templates/resume1.html", "w")
    f1.write(resume[0])
    f1.close()
    
    f2 = open("templates/resume2.html", "w")
    f2.write(resume[1])
    f2.close()
    print(".", end = '')    
    print("Executed")
    return matched_word


if __name__ == "__main__":
    #scrapeIndeed()
    resume_res = fetch_resume("Tax Services Associate Analyst - FSO - Fiduciary Trust Tax Services - International Tax Services")
    print(resume_res)


    
        