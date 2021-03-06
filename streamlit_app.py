import plotly.express as px
import streamlit as st

from data import *
from main import data


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")

st.title("Streamlit elections graphs")
st.caption("Task from the Prusa Research")

st.text("Please enter the name of city/village.")

textbox = st.text_input("", "Search...")

search_clicked = st.button("OK")
if search_clicked or textbox:

    options = data.find_places_by_name(textbox)
    options_str = ["{} [{}]".format(options.iloc[i]["city_name"], options.iloc[i]["district_name"]) for i in
                   range(len(options))]

    selected_place = st.selectbox("Multiple options available, please select:",
                                  options_str)
    if selected_place:
        index_selected = options_str.index(selected_place)

        votes = data.get_votes_by_city_id(
            int(options.iloc[index_selected]["city_id"]))

        involved_parties = votes["party"].replace(
            PARTIES)  # replace ID by NAME
        labels = list(involved_parties)

        percents = [float(x)
                    for x in list(votes["party_votes_percent"])]

        fig = px.pie(votes, values=percents, names=labels, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)
