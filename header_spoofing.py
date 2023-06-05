# -*- coding: utf-8 -*-
"""

********************** Header Spoofing for LinkedIn Scraping ****************************************
                                                                                         *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai        *
LinkedIn changes its layout and tags when it detects an attempt to scrape
This file generates random headers that can be passed to navigate through this issue     *   
                                                                                         *
******************************************************************************************

"""
import requests, random

def get_user_agent():
    
    user_agent_list = [
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    
    for _ in user_agent_list:
        #Pick a random user agent
        user_agent = random.choice(user_agent_list)
    
        #Set the headers 
        headers = {'User-Agent': user_agent}
    
    return headers

if __name__ == "__main__":
    print(get_user_agent())