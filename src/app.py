import pandas as pd 
import numpy as np 
import os
import shapely
import pydeck
import streamlit as st 
from MapData import MapData
from utils import *
import matplotlib.pyplot as plt

#Get data and cache it:
@st.cache
def get_data():
    '''Get data from the source'''
    dfe = pd.read_csv('travel_to_edu')
    dfe["Total"] = dfe["Total"] - dfe["Study_at_home"].replace(-999, 0)
    dfw = pd.read_csv('travel_to_work')
    dfw["Total"] = dfw["Total"] - dfw["Work_at_home"].replace(-999, 0)
    return (dfe, dfw)


dfe, dfw = get_data()

#First sidebar:
#This is the sidebar for either work or education
st.sidebar.header('**__Select the following features for visualization__**')

commute_for = st.sidebar.selectbox(
    "Commuting for ",
    ("Work", "Education")
)

#select the data to use:
if commute_for == "Work":
    df = MapData(dfw)
    col_home = "Work_at_home"
else:
    df = MapData(dfe)
    col_home = "Study_at_home"

means_of_transport = tuple([x.replace("_", " ") for x in df.getmeans() if "_home" not in x ])

#This is the sidebar of means of travel
commute_means = st.sidebar.selectbox(
    "Commuting by",
    means_of_transport,
    index = 9
)

#Select Territory
territory = st.sidebar.selectbox(
    "For Territory",
    df.territories,
    index = 39
)

st.sidebar.markdown('You selected commuting for {0} by {1} in territory {2}'.format(commute_for, commute_means, territory))

#Main page
st.title("There and Back Again")
st.header("**__Data visualization for New Zealand commuting trends__**")
st.markdown("**__The following geographical map and bar chart shows the summary of travels to and fro from the selected area__**")
#Select SA area in territory
region = st.selectbox(
    "Select Area", 
    df.getarea(territory)
)

st.markdown("_Geographical Map showing the arc of travel from source(red) to target(green)_")

r = getMap(df, commute_means.replace(" ", "_"), region)
st.pydeck_chart(r)

st.text(" ")

#Bar chart 
st.markdown("_Bar Chart showing the Commuting from {0} and to {0} for {1}_".format(region, commute_for))
#Get data for to and fro
df_selected = df.getregiondata(region).replace(-999, 0)
cols_chart = df.getmeans()
cols_chart.remove("Total")
cols_chart.remove(col_home)
#Get column name for at home: col_home
df_selected_bar = df_selected[df_selected.columns[~df_selected.columns.isin(["Total", col_home])]]

#Melt data Home
melt_data_fro = df_selected_bar[df_selected_bar.SA2_name_h == region].melt(id_vars=["SA2_name_h"], value_vars=cols_chart, var_name="var_means", value_name="Number of commutes")
grp_fro = melt_data_fro.groupby(["var_means"], as_index=False).sum()
grp_fro["Source"] = ["From" for i in range(grp_fro.shape[0])]

#Melt data To
melt_data_to = df_selected_bar[df_selected_bar.SA2_name_d == region].melt(id_vars=["SA2_name_d"], value_vars=cols_chart, var_name="var_means", value_name="Number of commutes")
grp_to = melt_data_to.groupby(["var_means"], as_index=False).sum()
grp_to["Source"] = ["To" for i in range(grp_to.shape[0])]
#Concat the data
concat_data = pd.concat([grp_fro, grp_to])
concat_data["Means"] = [getxticks(x) for x in concat_data["var_means"]]

chart_data = pd.pivot_table(
    concat_data,
    index = "Means",
    columns = "Source",
    values = "Number of commutes"
)

chart_data.plot.bar(figsize=(5,6))
plt.title("Bar Plot for Commuting from and to\n {0}".format(region))
plt.xlabel("Ways of Commute")
plt.ylabel("Number of Commutes")
plt.xticks(rotation=25, fontsize=9, ha="right")

st.pyplot()

#Pie chart
st.markdown("_Pie Chart for {1} preference _".format(region, commute_for))
df_selected_pie = df_selected[df_selected.columns[df_selected.columns.isin(["Total", col_home])]]
df_pie = df_selected_pie.sum()
df_pie.plot.pie(figsize=(5,5), colors = ["green", "red"], labels = [col_home, "Total" ])
plt.ylabel(" ")
st.pyplot()





