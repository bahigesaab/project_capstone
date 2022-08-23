import nltk
import pandas as pd
import streamlit as st
from streamlit import components
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

import gensim
from gensim import corpora
import pyLDAvis.gensim_models


from streamlit_objects import selection_box, get_tripadvisor_reviews, get_googlemaps_reviews

nltk.download('stopwords')
nltk.download('punkt')


#***************************************************************************************************


st.set_page_config(page_title="Topic Modeling Analysis of Reviews of Touristic Sites in Lebanon",
                   page_icon="⛰",
                   layout="wide")



st.title("Topic Modeling Analysis of Reviews of Touristic Sites in Lebanon")


#*****************************************************************************************************#

dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews_tm_nouns = get_tripadvisor_reviews("final_trip_advisor_reviews_tm_nouns.csv")

elif dataset_selected == "Google Reviews":
    reviews_tm_nouns = get_googlemaps_reviews("final_google_reviews_tm.csv")


st.markdown("""---""")

#*****************************************************************************************************#

topics_number = st.slider('Please, select the number of topics for modeling:', 3, 5, 3)

def fig_width_and_length(topics_number):
    if topics_number == 3:
        width = 3
        height =1
    elif topics_number == 4:
        width = 2
        height =2
    else:
        width = 3
        height =2

    return height, width


city_cell, attraction_cell = st.columns(2)


with city_cell:
    city_box = selection_box(reviews_tm_nouns, "location", "City")

    reviews_by_city = reviews_tm_nouns.query("location==@city_box")


with attraction_cell:
    disable_attraction_box = True if city_box[0] == "All" else False
    attraction_box = selection_box(reviews_by_city, "attraction", "Attraction", disable_box= disable_attraction_box)

    reviews_by_attractions = reviews_by_city.query("attraction==@attraction_box")

    reviews_queried_tm = reviews_tm_nouns.query(
        "location==@city_box & attraction==@attraction_box"
    )


attraction_name = " " if (attraction_box[0] == "All") else reviews_queried_tm["attraction"].iloc[0]
city_name = f'Location: {reviews_queried_tm["location"].iloc[0]}' if city_box[0] != "All" else "Location: All Locations"
category_value = f'Category: {reviews_queried_tm["category"].iloc[0]}' if attraction_box[0] != "All"  else ""

st.header(attraction_name)
st.subheader(city_name)
st.subheader(category_value)

# ******************************************************************************************

reviews_queried_tm["tokenized_sents"] = reviews_queried_tm["reviewsPreprocessed"].fillna("").map(nltk.word_tokenize)
dictionary = corpora.Dictionary(reviews_queried_tm["tokenized_sents"])

# Convert document into the bag-of-words (BoW) format = list of (token_id, token_count) tuples
doc_term_matrix = [dictionary.doc2bow(x) for x in reviews_queried_tm["tokenized_sents"]]

# Creating the object for LDA model using gensim library
LDA = gensim.models.ldamodel.LdaModel

# Build LDA model, 3 topics, 1000 documents for training phase, 50 passes
lda_model = LDA(corpus=doc_term_matrix, id2word=dictionary, num_topics= topics_number, random_state=100, passes=5,
                    chunksize=1000)

# ******************************************************************************************


sent_topics_df = pd.DataFrame()

# Get main topic in each document
for i, row_list in enumerate(lda_model[doc_term_matrix]):
    row = row_list[0] if lda_model.per_word_topics else row_list
    # print(row)
    row = sorted(row, key=lambda x: (x[1]), reverse=True)
# Get the Dominant topic, Perc Contribution and Keywords for each document
    for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = lda_model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(
                    pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
            else:
                break
sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

texts = [word for word in reviews_queried_tm["full_text"]]

contents = pd.Series(texts)
sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)


pd.options.display.max_colwidth = 100

sentence_topics_df = pd.DataFrame()
sent_topics_outdf_grpd = sent_topics_df.groupby('Dominant_Topic')

for i, grp in sent_topics_outdf_grpd:
    sentence_topics_df = pd.concat([sentence_topics_df,
                                                 grp.sort_values(['Perc_Contribution'], ascending=False).head(1)],
                                                axis=0)

# Reset Index
sentence_topics_df.reset_index(drop=True, inplace=True)

# Format
sentence_topics_df.columns = ["Topic Number", "Topic Perc Contrib", "Keywords", "Representative Text"]

# ******************************************************************************************


tab1, tab2, tab3, tab4  = st.tabs(["Word Clouds of Top N Keywords in Each Topic",
                                   "Most Representative Sentence of each Topic",
                                   "Topics Visualization PyLDAVis",
                                   "Importance of Topic Keywords"])

# ******************************************************************************************

with tab1:
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]

    cloud = WordCloud(stopwords=STOPWORDS,
                      background_color='white',
                      width=2500,
                      height=1800,
                      max_words=10,
                      colormap='tab10',
                      color_func=lambda *args, **kwargs: cols[i],
                      prefer_horizontal=1.0)

    topics = lda_model.show_topics(formatted=False)

    fig, axes = plt.subplots(1, topics_number, figsize=(10, 10), sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
        plt.gca().axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    st.pyplot(fig)
# ******************************************************************************************

with tab2:
    sub_df = sentence_topics_df[["Topic Number","Topic Perc Contrib", "Representative Text"]]
    st.dataframe(sub_df)

# ******************************************************************************************

with tab3:
    st.markdown("""## Topics Visualization
    
    # pyLDAvis is designed to help users interpret the topics in a topic model that has been fit to a corpus of text data. The package extracts information from a fitted LDA topic model to inform an interactive web-based visualization.
    
    1. Each bubble represents a topic. The larger the bubble, the higher percentage of the number of docs in the corpus is about that topic.
    2. Blue bars represent the overall frequency of each word in the corpus. If no topic is selected, the blue bars of the most frequently used words will be displayed.
    3. Red bars give the estimated number of times a given term was generated by a given topic. The word with the longest red bar is the word that is used the most by the docs belonging to that topic.
    4. The further the bubbles are away from each other, the more different they are. 
    5. A good topic model will have big and non-overlapping bubbles scattered throughout the chart. """)

    vis = pyLDAvis.gensim_models.prepare(lda_model, doc_term_matrix, dictionary)
    pyLDAvis.save_html(vis, 'lda.html')

    with open('lda.html', 'r') as f:
        html_string = f.read()

    components.v1.html(html_string, width=1300, height=800, scrolling=True)


# ******************************************************************************************

with tab4:
    height, width = fig_width_and_length(topics_number)

    topics = lda_model.show_topics(formatted=False)
    data_flat = [w for w_list in [reviews_queried_tm["reviewsPreprocessed"]] for w in w_list]

    out = []
    for i, topic in topics:
        for word, weight in topic:
            out.append([word, i, weight])

    imp_df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance'])

    # Plot Word Count and Weights of Topic Keywords
    fig1, axes1 = plt.subplots(height, width, figsize=(16, 10),  dpi=160)
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
    for i, ax1 in enumerate(axes1.flatten()):
        ax1.bar(x='word', height="importance", data=imp_df.loc[imp_df.topic_id == i, :], color=cols[i], width=0.2,
                    label='Weights')
        ax1.set_ylabel('Word Count', color=cols[i])
        ax1.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
        ax1.set_xticklabels(imp_df.loc[imp_df.topic_id == i, 'word'], rotation=30, horizontalalignment='right')


    fig1.tight_layout(w_pad=2)
    fig1.suptitle('Importance of Topic Keywords', fontsize=22, y=1.05)
    st.pyplot(fig1)

# ******************************************************************************************



