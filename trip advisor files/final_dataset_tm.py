import pandas as pd
import glob
import os
from pathlib import Path

import nltk

from topic_modeling import preprocess_text, remove_stopwords

import spacy


# lemmatize using spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


def lemmatization(text, tags=['NOUN', 'ADJ']):  # filter noun and adjective
    doc = nlp(text)
    output = ' '.join([token.lemma_ for token in doc if token.pos_ in tags])
    return output


# ************************************************************************************************ #

def get_all_reviews_topic_modeling(lemm_by_Noun = True):
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # Instantiate an empty array list
    attractions_csv_files_list = []

    # Loop through the csv files, get the name of each of them, and append it to the list
    for f in csv_files:
        csv_file_name = f.split("\\")[-1]
        attractions_csv_files_list.append(csv_file_name)

    # concatenate the pandas dfs togethere
    attractions_df = pd.concat(map(pd.read_csv,attractions_csv_files_list))

    # Get the all attractions df
    attractions_path = Path(__file__).parents[1] / 'tripadvisor_attractions.csv'
    all_attractions_df = pd.read_csv(attractions_path)
    # all_attractions_df = pd.read_csv("../tripadvisor_attractions.csv")

    # Merge attractions_df and all_attractions_df on "attraction_name"
    attractions_final = pd.merge(attractions_df, all_attractions_df, on="attraction_name")

    # Drop duplicate rows
    attractions_final = attractions_final.drop_duplicates()

    # drop empty columns whose all values are empty
    attractions_final = attractions_final.dropna(axis=1, how='all')


    # add a new column "written_reviews_number"
    attractions_final["written_reviews_number"] = 1

    # We group the reviews by their number to get the written reviews number
    group_df = attractions_final.groupby("attraction_name", as_index=False)["written_reviews_number"].count()
    group_attractions_df = group_df[["attraction_name", "written_reviews_number"]]

    # Drop the written_reviews_number column from the dataset
    attractions_final = attractions_final.drop('written_reviews_number', axis=1)

    # We add a "full_text" column that includes the review_title and review_body columns
    attractions_final["full_text"] = attractions_final["review_title"] + attractions_final["review_text"]

    # Apply the necessary preprocessing for topic modeling
    attractions_final["reviewsPreprocessed"] = attractions_final["full_text"].apply(preprocess_text)
    attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(remove_stopwords)

    if lemm_by_Noun == True:
        attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(lemmatization)
    else:
        attractions_final["reviewsPreprocessed"] = attractions_final["reviewsPreprocessed"].apply(lambda item : lemmatization(item, tags=["VERB", "ADV"]))

    attractions_final['tokenizedRev'] = attractions_final['reviewsPreprocessed'].apply(nltk.word_tokenize)

    # Merge attractions_df and group_attractions_df on "attraction_name"
    attractions_final = pd.merge(attractions_final, group_attractions_df, on="attraction_name")

    return attractions_final


attractions_df_topic_modeling = get_all_reviews_topic_modeling()
attractions_df_topic_modeling.to_csv("../final_trip_advisor_reviews_tm_nouns.csv")

# attractions_df_topic_modeling = get_all_reviews_topic_modeling(lemm_by_Noun = False)
# attractions_df_topic_modeling.to_csv("../final_trip_advisor_reviews_tm_verbs.csv")


# ************************************************************************************************ #


