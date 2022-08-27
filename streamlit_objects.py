import datetime
import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from geographic_locations import nations, us_states, us_states_codes, canadian_provinces_code, canadian_provinces, australian_provinces, australian_provinces_codes



@st.cache
def options_list(df, column):
    options_list = np.sort(df[column].unique())
    options_list = np.insert(options_list, 0, ["All"])
    return options_list


def selection_box(df, column, item, disable_box=False):
    selected_option = st.selectbox(
        f'Select {item}:',
        options=options_list(df, column),
        disabled= disable_box
        )
    if selected_option == "All":
        selected_option = [i for i in options_list(df, column)]

    return selected_option


def selection_box_two(df, column, item, disable_box=False):
    options_list = np.sort(df[column].unique())
    selected_option = st.selectbox(
        f'Select {item}:',
        options=options_list,
        disabled= disable_box
        )
    return selected_option

def get_tripadvisor_reviews(csv_file):
    reviews = pd.read_csv(csv_file)
    reviews['review_date'] = pd.to_datetime(reviews['review_date'])
    reviews['review_date'] = reviews['review_date'].dt.date
    reviews["review_rating"] = reviews["review_rating"].apply(pd.to_numeric).astype('Int64')

    return reviews


def display_info(title, value, left_unit="", right_unit=""):
    container = st.container()
    with container:
        st.markdown(f'**{title}**')
        st.subheader(f'{left_unit} {value} {right_unit}')
    return container


def plot_word_cloud(df, column, title):
    allWords = ' '.join(map(str, [words for words in df[column]]))
    wordCloud = WordCloud(width=1000,height=400, random_state=21, max_font_size=120, background_color='white', collocations=False).generate(allWords)
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(title, size=15, weight="bold")
    return plt

def get_attractions_dataframe(df, written_reviews = True ):
    if written_reviews == True:
        df_attractions = df[["attraction", "governorate","category","overall_rating","total_ratings","written_reviews_number"]]
        df_attractions = df_attractions.drop_duplicates(subset = "attraction")
        df_attractions = df_attractions.sort_values(by=["total_ratings","written_reviews_number"])
    else:
        df_attractions = df[["attraction", "governorate","category","overall_rating","total_ratings"]]
        df_attractions = df_attractions.drop_duplicates(subset = "attraction")
        df_attractions = df_attractions.sort_values(by=["total_ratings"])
    return df_attractions


def plot_horiz_group_barchart(df, y_column, x_column1, x_column2, title, height=500):
    fig = px.bar(df, y=y_column, x=[x_column1, x_column2], orientation='h',
                 barmode="group", height = height,  hover_data={'attraction': True},
                 title=title)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    yaxis_title=None,
    xaxis_title=None,
    )


    return fig


def get_reviewers_nationalities_df(df_input):
    countries = pd.read_csv("countries.csv")
    arab_emirates = ['UAE', 'United Arab Emirates', 'Abu Dhabi', 'Dubai', 'Sharjah']
    df_input['user_country'] = df_input['user_country'].str.strip()
    df = df_input[["attraction", "location", "governorate","category","user_country"]]
    complete_list = []
    complete_list.extend(nations)
    complete_list.extend(us_states)
    complete_list.extend(us_states_codes)
    complete_list.extend(canadian_provinces)
    complete_list.extend(canadian_provinces_code)
    complete_list.extend(australian_provinces)
    complete_list.extend(australian_provinces_codes)
    df = df[df["user_country"].isin(complete_list)]
    df.loc[df['user_country'] == "UK", 'user_country'] = "United Kingdom"
    df.loc[df['user_country'] == "USA", 'user_country'] = "United States"
    df.loc[df['user_country'] == "US", 'user_country'] = "United States"
    df.loc[df["user_country"].isin(us_states), "user_country"] = "United States"
    df.loc[df["user_country"].isin(us_states_codes), "user_country"] = "United States"
    df.loc[df["user_country"].isin(australian_provinces), "user_country"] = "Australia"
    df.loc[df["user_country"].isin(australian_provinces_codes), "user_country"] = "Australia"
    df.loc[df["user_country"].isin(canadian_provinces), "user_country"] = "Canada"
    df.loc[df["user_country"].isin(canadian_provinces_code), "user_country"] = "Canada"
    df.loc[df["user_country"].isin(arab_emirates), "user_country"] = "United Arab Emirates"
    df_nationalities = pd.merge(df, countries, on='user_country')
    df_nationalities["users_count"] = 1
    return df_nationalities

def display_world_map(df, title, sizing_theme, locations, scope="world"):
    mapbox_access_token = 'pk.eyJ1IjoiYmFoaWdlc2FhYiIsImEiOiJja3l5djA4czMwdzhoMnFxbDdqZXVhc2xjIn0.lqEdOX_HSMS4u-qNA6NXEQ'

    px.set_mapbox_access_token(mapbox_access_token)

    fig = px.choropleth(df, locations=locations,
                        labels={'user_country':'Country', 'color': 'Number of Reviewers'},
                        locationmode='country names', color=sizing_theme,
                        color_continuous_scale='Inferno_r',
                        scope= scope, title=title)

    return fig


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


def get_googlemaps_reviews(csv_file):
    reviews = pd.read_csv(csv_file)
    # Convert review_date to year from year ago to the year of the review:
    reviews['review_date'] = reviews['review_date'].apply(convert_to_year)
    return reviews


def plot_horiz_group_barchart_google(df, y_column, x_column1, title, height=500):
    fig = px.bar(df, y=y_column, x=x_column1, orientation='h', height = height, title=title, hover_data={'attraction': True})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    yaxis_title=None,
    xaxis_title=None
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})  # add only this line

    return fig


def display_map_lebanon(reviews_queried, title=""):
    mapbox_access_token = 'pk.eyJ1IjoiYmFoaWdlc2FhYiIsImEiOiJja3l5djA4czMwdzhoMnFxbDdqZXVhc2xjIn0.lqEdOX_HSMS4u-qNA6NXEQ'

    px.set_mapbox_access_token(mapbox_access_token)
    fig_two = px.scatter_mapbox(reviews_queried, lat="latitude", lon="longitude",
                                text="location", zoom=6.5, title= title,
                                center=dict(lat=33.83, lon=35.83))
    fig_two.update_traces(textposition='bottom right')
    
    return fig_two


def plot_scatter_ratings(df, reviews_type):

    df["discrete_rating"] = df["overall_rating"].astype(str)
    fig = px.scatter(df, x="overall_rating", y="total_ratings", color="category", symbol="category",
                     title=f"Attraction Ratings vs Number of Ratings for {reviews_type}", height=700,
                     hover_data={'attraction': True, "category":True}, 
                     labels={"total_ratings": "Total Number of Ratings", "overall_rating": "Attraction Rating",
                             "discrete_rating":"Attraction Rating"})

    return fig
