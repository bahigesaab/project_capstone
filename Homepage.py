import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


from sentiment_analysis import plot_time_series_count, plot_time_series_count_google_reviews
from streamlit_objects import get_tripadvisor_reviews, selection_box, display_info, get_reviewers_nationalities_df, \
    display_world_map, get_googlemaps_reviews, display_map_lebanon


#*****************************************************************************************************#

def count_google_ratings(df, rating):
    df = df.apply(lambda x: True
    if x['review_rating'] == rating else False, axis=1)

    num_rows = len(df[df == True].index)

    return num_rows

#*****************************************************************************************************#


st.set_page_config(page_title="Lebanon's Touristic Attraction Analyzer",
                   page_icon="🏛️",
                   layout="wide")

#*****************************************************************************************************#


st.title("Lebanon's Touristic Attraction Analyzer")



dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews = get_tripadvisor_reviews("final_trip_advisor_reviews_sa.csv")

elif dataset_selected == "Google Reviews":
    reviews = get_googlemaps_reviews("final_google_reviews_sa.csv")


st.markdown("""---""")

#*****************************************************************************************************#

attraction_box = selection_box(reviews, "attraction", "Attraction")

reviews_queried = reviews.query(
    "attraction==@attraction_box"
)

# *****************************************************************************************

attraction_name = reviews_queried["attraction"].iloc[0] if attraction_box[0] != "All"  else ""
city_name = reviews_queried["location"].iloc[0] if attraction_box[0] != "All"  else ""
governorate_name = reviews_queried["governorate"].iloc[0] if attraction_box[0] != "All"  else ""
category_value = reviews_queried["category"].iloc[0] if attraction_box[0] != "All"  else ""

# *****************************************************************************************

# Reviews
total_ratings = reviews_queried["total_ratings"].iloc[0] if attraction_box[0] != "All"  else ""
overall_avg_rating = reviews_queried["overall_rating"].iloc[0] if attraction_box[0] != "All"  else ""

if dataset_selected == "Trip Advisor":
    written_reviews_number = reviews_queried["written_reviews_number"].iloc[0] if attraction_box[0] != "All"  else ""

    # *****************************************************************************************

    # Ratings
    excellent_ratings = reviews_queried["excellent_ratings"].iloc[0] if attraction_box[0] != "All"  else ""
    very_good_ratings = reviews_queried["very_good_ratings"].iloc[0] if attraction_box[0] != "All"  else ""
    average_ratings = reviews_queried["average_ratings"].iloc[0] if attraction_box[0] != "All"  else ""
    poor_ratings = reviews_queried["poor_ratings"].iloc[0] if attraction_box[0] != "All"  else ""
    terrible_ratings = reviews_queried["terrible_ratings"].iloc[0] if attraction_box[0] != "All"  else ""

# *****************************************************************************************

elif dataset_selected == "Google Reviews":

    # Ratings
    excellent_ratings = count_google_ratings(reviews_queried, 5) if attraction_box[0] != "All" else ""
    very_good_ratings = count_google_ratings(reviews_queried, 4) if attraction_box[0] != "All" else ""
    average_ratings = count_google_ratings(reviews_queried, 3) if attraction_box[0] != "All" else ""
    poor_ratings = count_google_ratings(reviews_queried, 2) if attraction_box[0] != "All" else ""
    terrible_ratings = count_google_ratings(reviews_queried, 1) if attraction_box[0] != "All" else ""

# *****************************************************************************************

st.header(attraction_name)

separator1 = st.markdown("""---""") if attraction_box[0] != "All"  else ""

# *****************************************************************************************

tab1, tab2, tab3, tab4, tab5  = st.tabs(["General Info", "Geographic Distribution of Reviewers",
                                   "Timeline of Reviews", "Percentage of Ratings in Reviews",
                                        "Location of Attraction in Lebanon"])

with tab1:

    governorate_cell, city_cell, category_cell = st.columns(3)

    with governorate_cell:
        gov_info = display_info("Governorate", governorate_name) if attraction_box[0] != "All"  else ""

    with city_cell:
        city_info = display_info("Location", city_name) if attraction_box[0] != "All"  else ""

    with category_cell:
        cat_info = display_info("Category", category_value) if attraction_box[0] != "All"  else ""


    separator2 = st.markdown("""---""") if attraction_box[0] != "All"  else ""


    # *****************************************************************************************

    total_ratings_cell, overall_rating,  written_reviews_cell = st.columns(3)

    with total_ratings_cell:
        tr_info = display_info("Total Number of Ratings", total_ratings, right_unit="📄") if attraction_box[0] != "All"  else ""

    with overall_rating:
        ov_rating_info = display_info("Overall Average Rating", overall_avg_rating, right_unit="⭐") if attraction_box[0] != "All"  else ""

    with written_reviews_cell:
        if dataset_selected == "Trip Advisor":
            written_reviews_info = display_info("Total Number of Written Reviews", written_reviews_number, right_unit="📄") if attraction_box[0] != "All"  else ""



    separator3 = st.markdown("""---""") if attraction_box[0] != "All"  else ""


    # *****************************************************************************************

    excellent_cell, very_good_cell, average_cell, poor_cell, terrible_cell = st.columns(5)

    with excellent_cell:
        exc_info = display_info("Number of Excellent Ratings", excellent_ratings, right_unit="⭐") if attraction_box[0] != "All"  else ""


    with very_good_cell:
        vg_info = display_info("Number of Very Good Ratings", very_good_ratings, right_unit="⭐") if attraction_box[0] != "All"  else ""


    with average_cell:
        avg_info = display_info("Number of Average Ratings", average_ratings, right_unit="⭐") if attraction_box[0] != "All"  else ""


    with poor_cell:
        poor_info = display_info("Number   of  Poor  Ratings", poor_ratings, right_unit="⭐") if attraction_box[0] != "All"  else ""


    with terrible_cell:
        terrible_info = display_info("Number of Terrible Ratings", terrible_ratings, right_unit="⭐") if attraction_box[0] != "All"  else ""

    separator4 = st.markdown("""---""") if attraction_box[0] != "All" else ""

    if dataset_selected == "Google Reviews":
        st.warning("For touristic sites with more than 1000 ratings, not all the ratings were scraped. The maximum number of reviews" \
                   " scraped is 900. Therefore in their case, the excellent, very good, average, poor, and terrible ratings" \
                   " sum up to the total number of ratings.")


    # *****************************************************************************************


with tab2:

     if dataset_selected == "Trip Advisor":

        df_nationalities = get_reviewers_nationalities_df(reviews_queried)

        with st.container():

            df_grouped = df_nationalities.groupby(["user_country"])["users_count"].count().reset_index(
                name="users_count")
            countries = pd.read_csv("countries.csv")
            df_grouped_final = pd.merge(df_grouped, countries, on='user_country')
            map_lat = df_grouped_final.latitude
            map_long = df_grouped_final.longitude
            df_grouped_final = df_grouped_final.set_index('users_count')
            title = "<b>Nationalities of Trip Advisor Users who Reviewed about Lebanon</b>" if attraction_box[0] == "All" else f"<b>Nationalities of Trip Advisor Users who Reviewed about {attraction_name}</b>"

            map = display_world_map(df_grouped_final,
                                    title,
                                    np.absolute((df_grouped_final.index)), 'user_country')
            st.plotly_chart(map, use_container_width=True)

     elif dataset_selected == "Google Reviews":
         st.info("Google Reviews does not share data about the nationalities of its reviewers.")

    # *****************************************************************************************

with tab3:
    st.subheader("Time Series Graph of Reviews According to Years: ")

    if dataset_selected == "Trip Advisor":
        sa_time_plot = plot_time_series_count(reviews_queried)
        st.plotly_chart(sa_time_plot, use_container_width=True)

    elif dataset_selected == "Google Reviews":
        sa_time_plot = plot_time_series_count_google_reviews(reviews_queried)
        st.plotly_chart(sa_time_plot, use_container_width=True)


    # *****************************************************************************************************#

with tab4:

    st.subheader("Distribution of Reviews per Rating: ")

    ratings_distribution = reviews_queried['review_rating'].value_counts().rename_axis(['review_rating']).reset_index(name='counts')

    # Plotting  pie chart for ratings
    fig_pie = px.pie(values=ratings_distribution.counts, names=ratings_distribution.review_rating, title='Rating Distribution of Reviews',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

    # *****************************************************************************************************#

with tab5:
    st.subheader("Location of Attraction in Lebanon")
    fig_two = display_map_lebanon(reviews_queried)
    st.plotly_chart(fig_two)


# *****************************************************************************************

