import streamlit as st
import plotly.express as px

from sentiment_analysis import plot_bar_sentiment_analysis, plot_scatter_sentiment_analysis, plot_time_series_count, \
    plot_word_cloud_for_sa
from streamlit_objects import selection_box, get_tripadvisor_reviews, get_googlemaps_reviews

#*****************************************************************************************************#


st.set_page_config(page_title="Individual Sentiment Analysis of Reviews of Touristic Sites in Lebanon",
                   page_icon="🏙️",
                   layout="wide")


st.title("Individual Sentiment Analysis of Reviews of Touristic Sites in Lebanon")

#*****************************************************************************************************#

dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews_sa = get_tripadvisor_reviews("final_trip_advisor_reviews_sa.csv")

elif dataset_selected == "Google Reviews":
    reviews_sa = get_googlemaps_reviews("final_google_reviews_sa.csv")


st.markdown("""---""")

#*****************************************************************************************************#

governorate_cell, city_cell, attraction_cell = st.columns(3)


with governorate_cell:
    governorate_box = selection_box(reviews_sa, "governorate", "Governorate")

    reviews_by_governorate = reviews_sa.query("governorate==@governorate_box")


with city_cell:
    disable_city_box = True if governorate_box[0]=="All" else False
    city_box = selection_box(reviews_by_governorate, "location", "City", disable_box=disable_city_box)

    reviews_by_city = reviews_by_governorate.query("location==@city_box")


with attraction_cell:
    disable_attraction_box = True if (governorate_box[0] == "All" or city_box[0] == "All") else False
    attraction_box = selection_box(reviews_by_city, "attraction", "Attraction", disable_box= disable_attraction_box)

    reviews_by_attractions = reviews_by_city.query("attraction==@attraction_box")

    sa_reviews_queried = reviews_sa.query(
        "governorate==@governorate_box"\
        "& location==@city_box & attraction==@attraction_box"
    )

#*****************************************************************************************************#


attraction_name = " " if (attraction_box[0] == "All") else sa_reviews_queried["attraction"].iloc[0]
city_name = f'Location: {sa_reviews_queried["location"].iloc[0]}' if city_box[0] != "All" else "Location: All Locations"
governorate_name = f'Governorate: {sa_reviews_queried["governorate"].iloc[0]}' if governorate_box[0] != "All" else "Governorate: All Governorates"
category_value = f'Category: {sa_reviews_queried["category"].iloc[0]}' if attraction_box[0] != "All"  else ""

st.header(attraction_name)
st.subheader(city_name)
st.subheader(governorate_name)
st.subheader(category_value)

st.markdown("""---""")

#*****************************************************************************************************#

tab1, tab2, tab3, tab4 = st.tabs(["Overall Sentiment Analysis Chart", "SA Scatter Graph", "SA and Ratings Bar Graph", "SA Word Cloud"])


with tab1:
    st.subheader("Bar Graph of Sentiment Analysis of Reviews: ")

    sa_barplot = plot_bar_sentiment_analysis(sa_reviews_queried)
    st.pyplot(sa_barplot)

#*****************************************************************************************************#

with tab2:
    st.subheader("Scatter Graph of Sentiment Analysis of Reviews: ")

    sa_scatter_plot = plot_scatter_sentiment_analysis(sa_reviews_queried)
    st.plotly_chart(sa_scatter_plot, use_container_width=True)

#*****************************************************************************************************#

with tab3:
    st.subheader("Bar Graph of Reviews According Sentiment Analysis Categories and Ratings: ")

    # Preparing data for visualization
    sentiments_and_ratings = sa_reviews_queried[['review_rating','analysis']].value_counts().rename_axis(['review_rating','analysis']).reset_index(name='counts')

    # Plotting the Bar Graph
    fig = px.bar(sentiments_and_ratings, x="review_rating", y="counts", color='analysis',
                 color_discrete_sequence=px.colors.qualitative.Pastel,title="Sentiment & Ratings",labels={'x':'Ratings','y':'Total Number'})
    st.plotly_chart(fig, use_container_width=True)

#*****************************************************************************************************#

with tab4:
    st.subheader("Word Cloud of Reviews per Sentiment Analysis: ")

    positive_wc_cell, neutral_wc_cell, negative_wc_cell = st.columns(3)

    with positive_wc_cell:
        positive_reviews = plot_word_cloud_for_sa(sa_reviews_queried, "analysis", "reviewsPreprocessed", "Positive", "Word Cloud for Positive Reviews", display_mask= True)
        st.pyplot(positive_reviews)

    with neutral_wc_cell:
        neutral_reviews = plot_word_cloud_for_sa(sa_reviews_queried, "analysis", "reviewsPreprocessed", "Neutral", "Word Cloud for Neutral Reviews", display_mask= True)
        st.pyplot(neutral_reviews)

    with negative_wc_cell:
        negative_reviews = plot_word_cloud_for_sa(sa_reviews_queried, "analysis", "reviewsPreprocessed", "Negative", "Word Cloud for Negative Reviews", display_mask= True)
        st.pyplot(negative_reviews)


st.markdown("""---""")
