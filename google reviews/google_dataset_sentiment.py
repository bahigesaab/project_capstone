import pandas as pd
import glob
import os
from pathlib import Path
import contractions
import re

from textblob import TextBlob


def preprocess_text_sa(text):
    # convert to lower
    text_preprocessed = text.lower()
    text_preprocessed= text_preprocessed.strip()
    return text_preprocessed

def cont_expand(text):
    expanded_text = contractions.fix(text)
    return expanded_text


def de_emojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)




def convert_rating_to_number(text):
    number = text.split()[0]
    number = int(number)
    return number



def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity


def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def get_all_reviews_for_sentiment_analysis():
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

    # Preprocessing for Sentiment Analysis
    attractions_final["reviewsPreprocessed"] = attractions_final["full_text"].apply(preprocess_text_sa)
    attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(cont_expand)
    attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(de_emojify)
    attractions_final = attractions_final.dropna(subset=['reviewsPreprocessed'])

    # Adding Columns for polarity, sybjectivity, and analysis
    attractions_final["subjectivity"] = attractions_final['full_text'].apply(getSubjectivity)
    attractions_final["polarity"] = attractions_final['full_text'].apply(getPolarity)

    attractions_final["analysis"] = attractions_final['polarity'].apply(getAnalysis)

    return attractions_final


attractions_df = get_all_reviews_for_sentiment_analysis()
attractions_df.to_csv("../final_google_reviews_sa.csv")