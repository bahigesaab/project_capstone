import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import plotly.express as px
from wordcloud import WordCloud, STOPWORDS


def plot_scatter_sentiment_analysis(df):

    fig = px.scatter(df, x="polarity", y="subjectivity", color="analysis",
                     title="Sentiment Analysis",
                     labels={"polarity": "Reviews Polarity", "subjectivity": "Reviews Subjectivity"})

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig

def plot_bar_sentiment_analysis(df):
    # Get percentage of positive reviews
    positive_reviews = df[df.analysis == 'Positive']['reviewsPreprocessed']
    round((positive_reviews.shape[0] / df.shape[0]) * 100, 1)
    # Get percentage of neutral reviews
    neutral_reviews = df[df.analysis == 'Neutral']['reviewsPreprocessed']
    round((neutral_reviews.shape[0] / df.shape[0]) * 100, 1)
    # Get the percentage of negative reviews
    negative_reviews = df[df.analysis == 'Negative']['reviewsPreprocessed']
    round((negative_reviews.shape[0] / df.shape[0]) * 100, 1)
    df['analysis'].value_counts()

    # plot and visualize the counts
    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(12)
    ax = sns.countplot(data=df, x="analysis", order=df['analysis'].value_counts().index)
    ax.bar_label(ax.containers[0])
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Counts')
    ax.set_title("Sentiment Analysis")
    return fig




def plot_time_series_count(df, title="Time Series Graph of Reviews According to Years"):
    df["review_date"] = pd.to_datetime(df["review_date"])
    df["year"] = df["review_date"].dt.year
    df_by_year = df.groupby("year", as_index=False)[["attraction_id"]].count()
    df_by_year = df_by_year.sort_values(by="year")
    fig = px.line(df_by_year, x="year", y="attraction_id", title=title,
                  labels={
                      "year": "Reviews Year",
                      "attraction_id": "Number of Reviews"
                  },
                  )
    return fig



def plot_word_cloud_for_sa(df, condition, column, sentiment, title, display_mask=False):
    text = ' '.join(map(str, [words for words in df[df[condition] == sentiment][column]]))

    if len(text) == 0:
        text = "Empty Wordcloud"

    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    stopwords = set(STOPWORDS)
    stopwords.update(["place", "site", "location", "venue", "nan"])

    if display_mask == True:
        wordCloud = WordCloud(width=1000,height=400, random_state=21, max_font_size=120,
                              background_color='white', collocations=False, mask=mask, stopwords=stopwords).generate(text)
    else:
        wordCloud = WordCloud(width=1000,height=400, random_state=21, max_font_size=120,
                              background_color='white', collocations=False, stopwords=stopwords).generate(text)

    plt.imshow(wordCloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(title, size=15, weight="bold")
    return plt


def plot_time_series_count_google_reviews(df, title="Time Series Graph of Reviews According to Years"):
    df_by_year = df.groupby("review_date", as_index=False)[["attraction_id"]].count()
    df_by_year = df_by_year.sort_values(by="review_date")
    fig = px.line(df_by_year, x="review_date", y="attraction_id", title=title,
                  labels={
                      "review_date": "Reviews Year",
                      "attraction_id": "Number of Reviews"
                  },
                  )
    return fig
