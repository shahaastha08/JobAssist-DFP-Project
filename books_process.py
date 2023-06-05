# -*- coding: utf-8 -*-
"""
******** Google Books API Scraping Process *******************************************
                                                                                     *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai    *
Input: Keywords from linkedin_process                                                *
Scraping Method: Google Books API                                                    *   
Output: List of book recommendations using Google Books API                          *   
                                                                                     *
**************************************************************************************

"""

#import packages

#packages for making API
import requests

#packages for export of data
import pandas as pd
import os

def getBooks(keywords):
    print("Google Books.", end = '')
    #set variables for authentication
    googlebooks_url = 'https://www.googleapis.com/auth/books'
    API_key = 'AIzaSyDXiEkJTjBRtpyHVpK_aFPeALDyN2k3NfU'

    #set variables for performing a search

    #keywords
    #these have been hardcoded. They have to be converted to dynamic while integrating
    #keywords = ['machine learning', 'computer vision', 'speaking', 'database', 'communication skills', 'artificial intelligence',
    #           'java', 'data warehouse', 'data analytics', 'data structures']

    #search URL
    search_url = 'https://www.googleapis.com/books/v1/volumes?q='

    #number of results to be extracted
    num_results = 5

    #set variables for exporting the data

    #create directories for storing data
    mode = 0o666

    #create directory for storing raw data
    raw_path = os.path.join('Raw_Data')
    if not(os.path.exists(raw_path)):
        os.mkdir(raw_path, mode)
    else:pass

    #create directory for storing clean data
    clean_path = os.path.join('Cleaned_Data')
    if not(os.path.exists(clean_path)):
        os.mkdir(clean_path, mode)
    else:pass
    
    #columns to be present in the output excel
    columns = ['ID','Book_Title', 'Author', 'Description', 'Publisher', 'Download_Purchase_Link', 'Thumbnail']
    #output dataframe parameters
    #df_scraped_data = pd.DataFrame()

    #authentication to google books using API
    response = requests.get(
        url = googlebooks_url,
        params = {'key' : API_key},
        )
    print(".", end = '')
    if response.status_code == 200:

        #if keyword contains spaces replace with %20
        keyword_str =  '+'.join(['+'.join(i.split()) for i in keywords])

        #create the URL and receive response
        updated_url = search_url+keyword_str+'&maxResults='+str(num_results)+'&orderBy=relevance&key='+API_key
        response = requests.get(updated_url)
        response_json = response.json()

        #extract the list of books from the response
        list_books = response_json.get('items')
        #print(list_books)
        # #export the raw data in text files
        # keyword_path = os.path.join('Raw_Data', keyword)
        # if not(os.path.exists(keyword_path)):
        #     os.mkdir(keyword_path, mode)
        # else:pass

        print(".", end = '')
        #create a dictionary to store the books data for a keyword
        dict_scraped_data = {col: [] for col in columns}

        #iterate through the list of books
        for i, book in enumerate(list_books):
            dict_scraped_data['ID'].append(i+1)

            #extract the title
            title = book.get('volumeInfo').get('title')
            
            dict_scraped_data['Book_Title'].append(title)

            #extract the authors
            list_authors = book.get('volumeInfo').get('authors')
            
            str_authors = ' ; '.join(author for author in list_authors) if (list_authors != None) else None
            dict_scraped_data['Author'].append(str_authors)

            #extract the description
            description = book.get('volumeInfo').get('description')
            dict_scraped_data['Description'].append(description)

            #extract the publisher
            publisher = book.get('volumeInfo').get('publisher')
            dict_scraped_data['Publisher'].append(publisher)

            #extract the download or purchase link (as the book can be an eBook)
            down_purchase_link = book.get('volumeInfo').get('canonicalVolumeLink')
            dict_scraped_data['Download_Purchase_Link'].append(down_purchase_link)
            
            #extract the thumbnail link 
            imageLinks = book.get('volumeInfo').get('imageLinks')
            thumbnail_link = imageLinks.get("thumbnail") if imageLinks != None else None
            dict_scraped_data['Thumbnail'].append(thumbnail_link if thumbnail_link != None else None)

            df = pd.DataFrame.from_dict(dict_scraped_data, orient = 'columns')
            books = df.to_dict('records')
            # for i in range(len(df)):
            #     temp = {}
            #     for j in range(len(df.loc[0])):
            #         temp[df.columns[j]] =  df.iloc[i,j]
            #     books[i] = temp
    print("Executed")
    return books

if __name__ == "__main__":
    df = getBooks(['analyst', 'data', 'business', 'teams', 'opportunity', 'team', 'support', 'solutions', 'organizations', 'key', 'environments'])[0]