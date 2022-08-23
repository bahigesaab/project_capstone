import streamlit as st

from sentiment_analysis import plot_word_cloud_for_sa
from streamlit_objects import selection_box, get_tripadvisor_reviews, plot_word_cloud, get_googlemaps_reviews
from topic_modeling import freq_words

#*****************************************************************************************************#

st.set_page_config(page_title="Individual General Analysis of Reviews of Touristic Sites in Lebanon",
                   page_icon="🏙️",
                   layout="wide")


#*****************************************************************************************************#

dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews_2 = get_tripadvisor_reviews("final_trip_advisor_reviews_tm_nouns.csv")

elif dataset_selected == "Google Reviews":
    reviews_2 = get_googlemaps_reviews("final_google_reviews_tm.csv")


st.markdown("""---""")

#*****************************************************************************************************#

governorate_cell, city_cell, attraction_cell = st.columns(3)


with governorate_cell:
    governorate_box = selection_box(reviews_2, "governorate", "Governorate")

    reviews_by_governorate = reviews_2.query("governorate==@governorate_box")


with city_cell:
    disable_city_box = True if governorate_box[0]=="All" else False

    city_box = selection_box(reviews_by_governorate, "location", "City", disable_box=disable_city_box)

    reviews_by_city = reviews_by_governorate.query("location==@city_box")


with attraction_cell:
    disable_attraction_box = True if (governorate_box[0]=="All" or city_box[0]=="All") else False

    attraction_box = selection_box(reviews_by_city, "attraction", "Attraction", disable_box= disable_attraction_box)

    reviews_by_attractions = reviews_by_city.query("attraction==@attraction_box")

    reviews_queried = reviews_2.query(
        "governorate==@governorate_box"\
        "& location==@city_box & attraction==@attraction_box"
    )

#*****************************************************************************************************#

attraction_name = " " if (attraction_box[0] == "All") else reviews_queried["attraction"].iloc[0]
city_name = f'Location: {reviews_queried["location"].iloc[0]}' if city_box[0] != "All" else "Location: All Locations"
governorate_name = f'Governorate: {reviews_queried["governorate"].iloc[0]}' if governorate_box[0] != "All" else "Governorate: All Governorates"
category_value = f'Category: {reviews_queried["category"].iloc[0]}' if attraction_box[0] != "All"  else " "

st.header(attraction_name)
st.subheader(city_name)
st.subheader(governorate_name)
st.subheader(category_value)

#*****************************************************************************************************#

tab1, tab2, tab3 = st.tabs(["Overall Word Cloud", "Rating Word Clouds", "Frequency Word Charts"])

#*****************************************************************************************************#

with tab1:
    st.subheader("Word Cloud for Preprocessed Reviews: ")
    word_cloud_plot = plot_word_cloud(reviews_queried, "reviewsPreprocessed", "Word Cloud for Specified Attractions")
    st.pyplot(word_cloud_plot)

#*****************************************************************************************************#

with tab2:

    st.subheader("Word Cloud for Preprocessed Reviews According to Rate: ")

    five_stars_cell, four_stars_cell = st.columns(2)

    with five_stars_cell:
        five_stars_reviews = plot_word_cloud_for_sa(reviews_queried, "review_rating", "reviewsPreprocessed", 5, "Word Cloud for Five Star Ratings Reviews", display_mask=True)
        st.pyplot(five_stars_reviews)

    with four_stars_cell:
        four_stars_reviews = plot_word_cloud_for_sa(reviews_queried, "review_rating", "reviewsPreprocessed", 4, "Word Cloud for Four Star Ratings Reviews", display_mask=True)
        st.pyplot(four_stars_reviews)

    three_stars_cell, two_stars_cell, one_star_cell = st.columns(3)

    with three_stars_cell:
        three_stars_reviews = plot_word_cloud_for_sa(reviews_queried, "review_rating", "reviewsPreprocessed", 3, "Word Cloud for Three Star Ratings Reviews", display_mask=True)
        st.pyplot(three_stars_reviews)

    with two_stars_cell:
        two_stars_reviews = plot_word_cloud_for_sa(reviews_queried, "review_rating", "reviewsPreprocessed", 2, "Word Cloud for Two Star Ratings Reviews", display_mask=True)
        st.pyplot(two_stars_reviews)

    with one_star_cell:
        one_star_reviews = plot_word_cloud_for_sa(reviews_queried, "review_rating", "reviewsPreprocessed", 1, "Word Cloud for One Star Ratings Reviews", display_mask=True)
        st.pyplot(one_star_reviews)

#*****************************************************************************************************#


with tab3:
    st.subheader("Frequency of Words Graph for Preprocessed Reviews: ")

    frequent_words_fig = freq_words(reviews_queried["reviewsPreprocessed"])
    st.pyplot(frequent_words_fig)





