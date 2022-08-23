import pandas as pd
import glob
import os
from pathlib import Path
import datetime
import re

import nltk

from topic_modeling import preprocess_text, remove_stopwords, lemmatization

def de_emojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)



def convert_to_year(text):
    current_year = datetime.datetime.now().year
    if (text.split()[0]=="a") and (text.split()[1]=="year"):
        review_year =  current_year - 1
    elif text.split()[1]=="years":
        number = text.split()[0]
        number = int(number)
        review_year = current_year - number
    else:
        review_year = current_year

    return review_year


def convert_rating_to_number(text):
    number = text.split()[0]
    number = int(number)
    return number


# ************************************************************************************************ #

def get_all_reviews_topic_modeling():
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # Instantiate an empty array list
    attractions_csv_files_list = []

    # Loop through the csv files, get the name of each of them, and append it to the list
    for f in csv_files:
        csv_file_name = f.split("\\")[-1]
        attractions_csv_files_list.append(csv_file_name)

    # concatenate the pandas dfs togethere
    attractions_df = pd.concat(map(pd.read_csv, attractions_csv_files_list))

    # Get the all attractions df
    attractions_path = Path(__file__).parents[1] / 'google attractions.csv'
    all_attractions_df = pd.read_csv(attractions_path)
    # all_attractions_df = pd.read_csv("../tripadvisor_attractions.csv")

    # Merge attractions_df and all_attractions_df on "attraction_name"
    attractions_final = pd.merge(attractions_df, all_attractions_df, on="attraction")

    # Drop duplicate rows
    attractions_final = attractions_final.drop_duplicates()

    # drop empty columns whose all values are empty
    attractions_final = attractions_final.dropna(axis=1, how='all')

    attractions_final.rename(columns={'review': 'full_text', 'date': 'review_date'}, inplace=True)

    # Drop empty reviews
    attractions_final = attractions_final.dropna(subset=['full_text'])
    attractions_final = attractions_final.dropna(subset=['review_date'])

    # Convert ratings into integers
    attractions_final['rating'] = attractions_final['rating'].apply(convert_rating_to_number)

    # Removing reviews translated by Google
    attractions_final = attractions_final[attractions_final["full_text"].str.contains("(Translated by Google)|(Original)") == False]
    # Apply the necessary preprocessing for topic modeling
    attractions_final["reviewsPreprocessed"] = attractions_final["full_text"].apply(preprocess_text)
    attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(de_emojify)
    attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(remove_stopwords)

    attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(lemmatization)
    attractions_final = attractions_final.dropna(subset=['reviewsPreprocessed'])

    return attractions_final


attractions_df_topic_modeling = get_all_reviews_topic_modeling()
attractions_df_topic_modeling.to_csv("../final_google_reviews_tm.csv")



# ************************************************************************************************ #


