# -*- coding: utf-8 -*-
"""
******** TF-IDF Keyword Extraction Process *******************************************************
                                                                                                 *
Authors: Team C8 - Aastha Shah, Shradhdha Gupte, Pratyaksh Verma, Aashish Pitchai                *
Input: Job Description from linkedin_process                                                     * 
Extraction Method: Term Frequency - Inverse Document Frequency                                   *   
Output: Extracted list of keywords                                                               *   
                                                                                                 *
**************************************************************************************************

"""



import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import pickle


# Clean text input
def pre_process(text):
    
    # lowercase
    text=text.lower()
    
    #remove tags
    text=re.sub("","",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    return text
    

# Load stop words file
def get_stop_words(stop_file_path):
    """load stop words """
    
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    #use only topn items from vector
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
    
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]

    return results


# Fit TfidfVectorizer on 244k+ job descriptions from Kaggle and store in pickle file
def fit_tfidf():
    # read json into a dataframe
    df_idf=pd.read_csv("data/Train_rev1.csv")
    # print schema
    print("Schema:\n\n",df_idf.dtypes)
    print("Number of questions,columns=",df_idf.shape)
    df_idf["FullDescription"] = df_idf['FullDescription'].apply(lambda x:pre_process(x))
    #load a set of stop words
    stopwords=get_stop_words("resources/stopwords.txt")

    #get the text column 
    docs=df_idf['FullDescription'].tolist()

    #create a vocabulary of words, 
    #ignore words that appear in 85% of documents, 
    #eliminate stop words
 
    tfidf_transformer = TfidfVectorizer(analyzer='word', ngram_range=(1,2), stop_words = stopwords, lowercase = True, max_features = 500000, max_df=0.85)
    tfidf_transformer.fit(docs)    
 
    #Save vectorizer.vocabulary_
    pickle.dump(tfidf_transformer,open("resources/tfidf1.pkl","wb"))


# Load pickle file and extract keywords for input text
def get_keywords(text):
    
    tf1 = pickle.load(open("resources/tfidf1.pkl", 'rb'))
    tfidf_transformer = TfidfVectorizer(smooth_idf=True, use_idf=True, vocabulary = tf1.vocabulary_)
    
    
    doc = pre_process(text)
    feature_names = tfidf_transformer.get_feature_names()
    tf_idf_vector=tfidf_transformer.fit_transform([doc])
    
    
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    
    return list(keywords.keys())



if __name__ == "__main__":
    df_test=pd.read_csv("data/linkedin_jd_test.csv")   
    
    # # read test docs into a dataframe and concatenate title and job description
    df_test['Text'] = df_test['Title'] + ' ' + df_test['Job_Description']
    
    
    print(get_keywords(df_test['Text'][1]))
    # fit_tfidf()
    





    
