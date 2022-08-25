import streamlit as st
import plotly.express as px


from sentiment_analysis import plot_word_cloud_for_sa, plot_bar_sentiment_analysis, plot_scatter_sentiment_analysis
from streamlit_objects import get_tripadvisor_reviews, get_googlemaps_reviews, selection_box, selection_box_two


#*****************************************************************************************************#

def location_and_gov(location, governorate, box):
    full_sentence = f'{location} - {governorate}' if box != 'All' else ''
    return full_sentence

#*****************************************************************************************************#

st.set_page_config(page_title="Comparative Sentiment Analysis of Reviews of Touristic Sites in Lebanon",
                   page_icon="🏛️",
                   layout="wide")


st.title("Comparative Sentiment Analysis of Reviews of Touristic Sites in Lebanon")

st.markdown("""---""")

#*****************************************************************************************************#

dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews_4 = get_tripadvisor_reviews("final_trip_advisor_reviews_sa.csv")

elif dataset_selected == "Google Reviews":
    reviews_4 = get_googlemaps_reviews("final_google_reviews_sa.csv")


st.markdown("""---""")
#*****************************************************************************************************#

with st.container():
    category_box = selection_box_two(reviews_4, "category", "Category")

    reviews_by_category = reviews_4.query("category==@category_box")


#*****************************************************************************************************#

attraction_one_cell, attraction_two_cell = st.columns(2)

disable_attraction_box = True if category_box[0] == "All" else False

with attraction_one_cell:

    attraction_box_one = selection_box(reviews_by_category, "attraction", "first attraction:", disable_box= disable_attraction_box)

    reviews_by_attraction_one = reviews_by_category.query("attraction==@attraction_box_one")

    reviews_queried_one = reviews_4.query(
        "category==@category_box & attraction==@attraction_box_one"
    )


with attraction_two_cell:

    attraction_box_two = selection_box(reviews_by_category, "attraction", "second attraction:", disable_box= disable_attraction_box)

    reviews_by_attraction_two = reviews_by_category.query("attraction==@attraction_box_two")

    reviews_queried_two = reviews_4.query(
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

tab1, tab2, tab3, tab4, tab5, tab6  = st.tabs(["Sent Analysis Bar Graph", "Sent Analysis Scatter Graph",
                                   "Sent Analysis Bargraph According to Categories and Ratings", "Positive Reviews SA Word Cloud",
                                    "Neutral Reviews SA Word Cloud","Negative Reviews SA Word Cloud"])

with tab1:

    st.subheader("Bar Graph of Sentiment Analysis of Reviews:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        sa_barplot = plot_bar_sentiment_analysis(reviews_queried_one)
        st.pyplot(sa_barplot)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        sa_barplot = plot_bar_sentiment_analysis(reviews_queried_two)
        st.pyplot(sa_barplot)

# *****************************************************************************************************#

with tab2:

    st.subheader("Scatter Graph of Sentiment Analysis of Reviews: ")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        sa_scatter_plot = plot_scatter_sentiment_analysis(reviews_queried_one)
        st.plotly_chart(sa_scatter_plot, use_container_width=True)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        sa_scatter_plot = plot_scatter_sentiment_analysis(reviews_queried_two)
        st.plotly_chart(sa_scatter_plot, use_container_width=True)

# *****************************************************************************************************#

with tab3:

    st.subheader("Bar Graph of Reviews According Sentiment Analysis Categories and Ratings: ")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        # Preparing data for visualization
        sentiments_and_ratings = reviews_queried_one[['review_rating', 'analysis']].value_counts().rename_axis(
            ['review_rating', 'analysis']).reset_index(name='counts')

        # Plotting the Bar Graph
        fig = px.bar(sentiments_and_ratings, x="review_rating", y="counts", color='analysis',
                     color_discrete_sequence=px.colors.qualitative.Pastel, title="Sentiment & Ratings",
                     labels={'x': 'Ratings', 'y': 'Total Number'})
        st.plotly_chart(fig, use_container_width=True)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        sentiments_and_ratings = reviews_queried_two[['review_rating', 'analysis']].value_counts().rename_axis(
            ['review_rating', 'analysis']).reset_index(name='counts')

        # Plotting the Bar Graph
        fig = px.bar(sentiments_and_ratings, x="review_rating", y="counts", color='analysis',
                     color_discrete_sequence=px.colors.qualitative.Pastel, title="Sentiment & Ratings",
                     labels={'x': 'Ratings', 'y': 'Total Number'})
        st.plotly_chart(fig, use_container_width=True)

# *****************************************************************************************************#


with tab4:

    st.subheader("Word Cloud of Positive Sentiment Analysis Reviews:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        positive_reviews = plot_word_cloud_for_sa(reviews_queried_one, "analysis", "reviewsPreprocessed", "Positive", "Word Cloud for Positive Reviews")
        st.pyplot(positive_reviews)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        positive_reviews = plot_word_cloud_for_sa(reviews_queried_two, "analysis", "reviewsPreprocessed", "Positive", "Word Cloud for Positive Reviews")
        st.pyplot(positive_reviews)

# *****************************************************************************************************#

with tab5:

    st.subheader("Word Cloud of Neutral Sentiment Analysis Reviews:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        neutral_reviews = plot_word_cloud_for_sa(reviews_queried_one, "analysis", "reviewsPreprocessed", "Neutral", "Word Cloud for Neutral Reviews")
        st.pyplot(neutral_reviews)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        positive_reviews = plot_word_cloud_for_sa(reviews_queried_two, "analysis", "reviewsPreprocessed", "Neutral", "Word Cloud for Neutral Reviews")
        st.pyplot(neutral_reviews)

# *****************************************************************************************************#

with tab6:

    st.subheader("Word Cloud of Negative Sentiment Analysis Reviews:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        negative_reviews = plot_word_cloud_for_sa(reviews_queried_one, "analysis", "reviewsPreprocessed", "Negative", "Word Cloud for Negative Reviews")
        st.pyplot(neutral_reviews)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        negative_reviews = plot_word_cloud_for_sa(reviews_queried_two, "analysis", "reviewsPreprocessed", "Negative", "Word Cloud for Negative Reviews")
        st.pyplot(neutral_reviews)

# *****************************************************************************************************#