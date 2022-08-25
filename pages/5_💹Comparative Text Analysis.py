import streamlit as st
from topic_modeling import freq_words

from sentiment_analysis import plot_word_cloud_for_sa
from streamlit_objects import get_tripadvisor_reviews, get_googlemaps_reviews, selection_box, \
    plot_word_cloud, selection_box_two


#*****************************************************************************************************#

def location_and_gov(location, governorate, box):
    full_sentence = f'{location} - {governorate}' if box != 'All' else ''
    return full_sentence

#*****************************************************************************************************#

st.set_page_config(page_title="Comparative General Analysis of Reviews of Touristic Sites in Lebanon",
                   page_icon="🌃",
                   layout="wide")


st.title("Comparative General Analysis of Reviews of Touristic Sites in Lebanon")

st.markdown("""---""")

#*****************************************************************************************************#

dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews_3 = get_tripadvisor_reviews("final_trip_advisor_reviews_tm_nouns.csv")

elif dataset_selected == "Google Reviews":
    reviews_3 = get_googlemaps_reviews("final_google_reviews_tm.csv")


st.markdown("""---""")
#*****************************************************************************************************#

with st.container():
    category_box = selection_box_two(reviews_3, "category", "Category")

    reviews_by_category = reviews_3.query("category==@category_box")


#*****************************************************************************************************#

attraction_one_cell, attraction_two_cell = st.columns(2)

disable_attraction_box = True if category_box[0] == "All" else False

with attraction_one_cell:

    attraction_box_one = selection_box(reviews_by_category, "attraction", "first attraction:", disable_box= disable_attraction_box)

    reviews_by_attraction_one = reviews_by_category.query("attraction==@attraction_box_one")

    reviews_queried_one = reviews_3.query(
        "category==@category_box & attraction==@attraction_box_one"
    )


with attraction_two_cell:

    attraction_box_two = selection_box(reviews_by_category, "attraction", "second attraction:", disable_box= disable_attraction_box)

    reviews_by_attraction_two = reviews_by_category.query("attraction==@attraction_box_two")

    reviews_queried_two = reviews_3.query(
        "category==@category_box & attraction==@attraction_box_two")

st.markdown("""---""")

#*****************************************************************************************************#

attraction_name_one = reviews_queried_one["attraction"].iloc[0] if attraction_box_one[0] != "All" else ""
city_name_one = reviews_queried_one["location"].iloc[0] if attraction_box_one[0] != "All" else ""
governorate_name_one = reviews_queried_one["governorate"].iloc[0] if attraction_box_one[0] != "All" else ""


attraction_name_two = reviews_queried_two["attraction"].iloc[0] if attraction_box_two[0] != "All" else ""
city_name_two = reviews_queried_two["location"].iloc[0] if attraction_box_two[0] != "All" else ""
governorate_name_two = reviews_queried_two["governorate"].iloc[0] if attraction_box_two[0] != "All" else ""

#*****************************************************************************************************#

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Word Frequency Graph", "Overall Word Cloud",
                                                    "5 Star Word Cloud", "4 Star Word Cloud", "3 Star Word Cloud",
                                                    "2 Star Word Cloud", "1 Star Word Cloud"])

with tab1:

    st.subheader("Frequency of Words Graph for Preprocessed Reviews:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        frequent_words_fig = freq_words(reviews_queried_one["reviewsPreprocessed"])
        st.pyplot(frequent_words_fig)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        frequent_words_fig = freq_words(reviews_queried_two["reviewsPreprocessed"])
        st.pyplot(frequent_words_fig)

# *****************************************************************************************************#

with tab2:
    st.header("Overall Word Cloud of Preprocessed Reviews")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        word_cloud_plot_one = plot_word_cloud(reviews_queried_one, "reviewsPreprocessed",
                                          f'Word Cloud for {attraction_name_one}')
        st.pyplot(word_cloud_plot_one)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        word_cloud_plot_two = plot_word_cloud(reviews_queried_two, "reviewsPreprocessed",
                                          f'Word Cloud for {attraction_name_one}')
        st.pyplot(word_cloud_plot_two)

# *****************************************************************************************************#

with tab3:

    st.header("Overall Word Cloud of 5-stars Preprocessed Reviews")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        five_stars_reviews_one = plot_word_cloud_for_sa(reviews_queried_one, "review_rating", "reviewsPreprocessed", 5,
                                                    "Word Cloud for Five Star Ratings Reviews")
        st.pyplot(five_stars_reviews_one)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        five_stars_reviews_two = plot_word_cloud_for_sa(reviews_queried_two, "review_rating", "reviewsPreprocessed", 5,
                                                    "Word Cloud for Five Star Ratings Reviews")
        st.pyplot(five_stars_reviews_two)

# *****************************************************************************************************#

with tab4:
    st.header("Overall Word Cloud of 4-stars Preprocessed Reviews")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        stars_reviews_one = plot_word_cloud_for_sa(reviews_queried_one, "review_rating", "reviewsPreprocessed", 4,
                                                    "Word Cloud for Four Star Ratings Reviews")
        st.pyplot(five_stars_reviews_one)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        stars_reviews_two = plot_word_cloud_for_sa(reviews_queried_two, "review_rating", "reviewsPreprocessed", 4,
                                                    "Word Cloud for Four Star Ratings Reviews")
        st.pyplot(stars_reviews_two)

# *****************************************************************************************************#

with tab5:
    st.header("Overall Word Cloud of 3-stars Preprocessed Reviews")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        stars_reviews_one = plot_word_cloud_for_sa(reviews_queried_one, "review_rating", "reviewsPreprocessed", 3,
                                                    "Word Cloud for Three Star Ratings Reviews")
        st.pyplot(five_stars_reviews_one)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        stars_reviews_two = plot_word_cloud_for_sa(reviews_queried_two, "review_rating", "reviewsPreprocessed", 3,
                                                    "Word Cloud for Three Star Ratings Reviews")
        st.pyplot(stars_reviews_two)

# *****************************************************************************************************#


with tab6:
    st.header("Overall Word Cloud of 2-stars Preprocessed Reviews")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        stars_reviews_one = plot_word_cloud_for_sa(reviews_queried_one, "review_rating", "reviewsPreprocessed", 2,
                                                    "Word Cloud for Two Star Ratings Reviews")
        st.pyplot(five_stars_reviews_one)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        stars_reviews_two = plot_word_cloud_for_sa(reviews_queried_two, "review_rating", "reviewsPreprocessed", 2,
                                                    "Word Cloud for Two Star Ratings Reviews")
        st.pyplot(stars_reviews_two)

# *****************************************************************************************************#
with tab7:
    st.header("Overall Word Cloud of 5-stars Preprocessed Reviews")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        stars_reviews_one = plot_word_cloud_for_sa(reviews_queried_one, "review_rating", "reviewsPreprocessed", 1,
                                                    "Word Cloud for One Star Ratings Reviews")
        st.pyplot(five_stars_reviews_one)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        stars_reviews_two = plot_word_cloud_for_sa(reviews_queried_two, "review_rating", "reviewsPreprocessed", 1,
                                                    "Word Cloud for One Star Ratings Reviews")
        st.pyplot(stars_reviews_two)

# *****************************************************************************************************#


