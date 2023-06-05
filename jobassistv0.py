# -*- coding: utf-8 -*-
"""

******** Jobassistv0 main file *******************************************
                                                                                        *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai       *
Main file that imports all other files and fetches the information from all data sources*   
Displays all the information on a GUI using Flask                                       *
**************************************************************************************

"""

from flask import Flask, render_template, request, send_file
from linkedin_process import scrapeLinkedIn
from indeed_process import fetch_resume
from books_process import getBooks
from glassdoor_process import getGlassdoor
import os

app = Flask(__name__)


@app.route('/')
def home(): 
   return render_template('index.html')

@app.route('/resume1')
def show_resume1():
    return render_template('resume1.html')

@app.route('/resume2')
def show_resume2():
    return render_template('resume2.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   try: 
       if request.method == 'POST':
          form_inp = request.form
          if (form_inp != None) and (form_inp['url'] != "") and form_inp['url'].startswith("https://www.linkedin.com/jobs/view/"):
              li_vars = {}
              gl_vars = {}
              
              
              # LinkedIn
              li_vars['html'], li_vars['title'], li_vars['company'], li_vars['loc'], li_vars['jd'],\
                              li_vars['keywords'], li_vars['logo'] = scrapeLinkedIn(form_inp['url'])
              print(li_vars)
              
              # Glassdoor
              temp = getGlassdoor(li_vars['company'], li_vars['title'])
              gl_vars = {}
              gl_vars['Name'], gl_vars['Type'], gl_vars['Website'],\
                            gl_vars['Founded'], gl_vars['Headquarters'], gl_vars['Industry'], \
                            gl_vars['Revenue'], gl_vars['Size'], gl_vars['Role'], gl_vars['Total Pay'], \
                            gl_vars['Base Pay'], gl_vars['Bonus'], gl_vars['Rating'], \
                            gl_vars['Recommended to a friend'], gl_vars['Approval of CEO'] = (
                                                                                    temp['Name'], temp['Type'], temp['Website'],
                                                                                    temp['Founded'], temp['Headquarters'], temp['Industry'],
                                                                                    temp['Revenue'], temp['Size'], temp['Role'], temp['Total Pay'],
                                                                                    temp['Base Pay'], temp['Bonus'], temp['Rating'],
                                                                                    temp['Recommended to a friend'], temp['Approval of CEO'])
              del temp
              try:
                    gl_vars['Rating'] = int(float(gl_vars['Rating']))
              except:
                    gl_vars['Rating'] = 0
              
              if gl_vars != None:
                  print("Glassdoor Executed Succesfully")
              
              # Indeed
              ind_vars = {}
              ind_vars["title"] = fetch_resume(li_vars['title'])
              if ind_vars != None:
                  print("Indeed Executed Successfully")
              
                
              # Load Books results
              books = {}
              books = getBooks(li_vars['keywords'])
    
              
              results = 1
              
              
              
              
              return render_template("index.html", results = results, li_vars = li_vars,\
                                                 gl_vars = gl_vars, ind_vars = ind_vars, books = books)
   except:
       return render_template("index.html", results = 0, li_vars = None,\
                                          gl_vars = None, ind_vars = None, books = None)
          

if __name__ == '__main__':
    app.run(debug = True) 
   
   
   
   
   
   
   
   
   
   
   
     