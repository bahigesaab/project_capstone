import streamlit as st

from streamlit_objects import get_tripadvisor_reviews, get_attractions_dataframe, plot_horiz_group_barchart, \
    get_googlemaps_reviews, plot_horiz_group_barchart_google, plot_scatter_ratings

#*****************************************************************************************************#

st.set_page_config(page_title="Overall General Analysis of Reviews of Touristic Sites in Lebanon",
                   page_icon="🌆",
                   layout="wide")


st.title("Overall General Analysis of Reviews of Touristic Sites in Lebanon")

st.markdown("""---""")

#*****************************************************************************************************#

dataset_selected = st.radio("Select Platform Reviews", ["Trip Advisor", "Google Reviews"], horizontal=True)

if dataset_selected == "Trip Advisor":
    reviews_1 = get_tripadvisor_reviews("final_trip_advisor_reviews_sa.csv")
    attractions_df = get_attractions_dataframe(reviews_1)

elif dataset_selected == "Google Reviews":
    reviews_1 = get_googlemaps_reviews("final_google_reviews_sa.csv")
    attractions_df = get_attractions_dataframe(reviews_1, written_reviews=False)


st.markdown("""---""")
#*****************************************************************************************************#

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Attractions with the Most Number of Reviews", "Attractions with the Least Number of Reviews",
                                  "Reviews per Governorate", "Reviews per Category", "Attraction Rating vs Number of Ratings"])

with tab1:
    with st.container():
        if dataset_selected == "Trip Advisor":
            attractions_horiz_barchart = plot_horiz_group_barchart_google(attractions_df.tail(10), "attraction", "total_ratings",
                                                                          "Attractions with the Most Number of Reviews",
                                                                          height=600)

        elif dataset_selected == "Google Reviews":
            attractions_horiz_barchart = plot_horiz_group_barchart_google(attractions_df.tail(10), "attraction", "total_ratings",
                                                                          "Attractions with the Most Number of Reviews",
                                                                          height=600)


        st.plotly_chart(attractions_horiz_barchart, use_container_width=True)
        st.markdown("""---""")

#*****************************************************************************************************#

with tab2:
    with st.container():
        if dataset_selected == "Trip Advisor":
            attractions_horiz_barchart = plot_horiz_group_barchart_google(attractions_df.head(10), "attraction", "total_ratings",
                                                                          "Attractions with the Least Number of Reviews",
                                                                          height=600)

        elif dataset_selected == "Google Reviews":
            attractions_horiz_barchart = plot_horiz_group_barchart_google(attractions_df.head(10), "attraction", "total_ratings",
                                                                          "Attractions with the Least Number of Reviews",
                                                                          height=600)


        st.plotly_chart(attractions_horiz_barchart, use_container_width=True)
        st.markdown("""---""")

#*****************************************************************************************************#

with tab3:
    with st.container():
        if dataset_selected == "Trip Advisor":
            attractions_horiz_barchart_gov = plot_horiz_group_barchart_google(attractions_df, "governorate",
                                                                          "total_ratings",
                                                                          "Number of Trip Advisor Ratings and Reviews per Attraction Governorate",
                                                                          height=600)

        elif dataset_selected == "Google Reviews":
            attractions_horiz_barchart_gov = plot_horiz_group_barchart_google(attractions_df, "governorate",
                                                                          "total_ratings",
                                                                          "Number of Google Ratings and Reviews per Attraction Governorate",
                                                                          height=600)

        st.plotly_chart(attractions_horiz_barchart_gov, use_container_width=True)

    st.markdown("""---""")

#*****************************************************************************************************#

with tab4:
   with st.container():
    if dataset_selected == "Trip Advisor":
        attractions_horiz_barchart_cat = plot_horiz_group_barchart_google(attractions_df, "category",
                                                                          "total_ratings",
                                                                          "Number of Trip Advisor Ratings and Reviews per Attraction Category",
                                                                          height=600)

    elif dataset_selected == "Google Reviews":
        attractions_horiz_barchart_cat = plot_horiz_group_barchart_google(attractions_df, "category",
                                                                          "total_ratings",
                                                                          "Number of Google Ratings and Reviews per Attraction Category",
                                                                          height=600)

    st.plotly_chart(attractions_horiz_barchart_cat, use_container_width=True)

    st.markdown("""---""")

#*****************************************************************************************************#

with tab5:
    with st.container():
        if dataset_selected == "Trip Advisor":
            scatter_plot = plot_scatter_ratings(attractions_df, "Trip Advisor Reviews")

        elif dataset_selected == "Google Reviews":
            scatter_plot = plot_scatter_ratings(attractions_df, "Google Reviews")



        st.plotly_chart(scatter_plot, use_container_width=True)
        st.markdown("""---""")

#*****************************************************************************************************#





