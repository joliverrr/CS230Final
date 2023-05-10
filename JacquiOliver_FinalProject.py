'''
Name:       Jacqui Oliver
CS230:      Section 4
Data:       RollerCoasters-Geo.csv
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:
This program has a map with icons, tables with sorting, and other visuals and features that help the user visualize and analyze data from the roller coaster database file.
'''

import streamlit as st
import matplotlib.pyplot as plt
import csv
from PIL import Image
import pydeck as pdk
import pandas as pd
import seaborn as sns
import altair as alt

st.set_page_config(page_title='USA Coaster Finder', page_icon=':roller_coaster:')
data_file = pd.read_csv("C:/Users/Jacqui/OneDrive - Bentley University/CS230/CS230/Homework/Final Project/RollerCoasters-Geo (2).csv")
st.title('USA Roller Coaster Finder!')
st.header("Use visuals and filters to find the perfect roller coaster experience!")
Coaster_image = Image.open("C:/Users/Jacqui/OneDrive - Bentley University/CS230/CS230/Homework/Final Project/RollerCoasterImage.jpg")
st.image(Coaster_image, use_column_width=True)

sidebar = st.container()
with sidebar:
    st.sidebar.header('Coaster Filters')
    def page1():
        st.header("Home Page")
        st.write("Welcome to the USA Roller Coaster Database!")
    def page2():
        st.header("Coaster Map")
        st.write("This Page Allows You to Filter Coasters by Location!")
        data_file = pd.read_csv("C:/Users/Jacqui/OneDrive - Bentley University/CS230/CS230/Homework/Final Project/RollerCoasters-Geo (2).csv")
        stateslist = []
        for s in data_file['State']:
            if s not in stateslist:
                stateslist.append(s)
        stateslist = sorted(stateslist)
        selected_statebox = st.selectbox("Please select a state:", stateslist)
        st.write("The state you selected is:", selected_statebox)
        filtered_data = data_file[data_file['State'] == selected_statebox]

        citieslist = []
        for index, row in filtered_data.iterrows():
            if row['City'] not in citieslist:
                citieslist.append(row['City'])
        citieslist = sorted(citieslist)
        selected_citybox = st.selectbox("Please select a city:", citieslist)
        st.write("The city you selected is:", selected_citybox)

        filtered_data = filtered_data[filtered_data['City'] == selected_citybox]

        map_data = filtered_data[['Coaster', 'Park', 'City', 'State', 'Type', 'Design', 'Year_Opened', 'Latitude', 'Longitude']]

        icon_data = {
            "url": "https://cdn-icons-png.flaticon.com/512/1054/1054858.png",
            "width": 100,
            "height": 100,
            "anchorY": 100
        }

        tool_tip = {"html": "Coaster:<br/> <b>{Coaster}</b><br/>\
                    Park:<br/> <b>{Park}</b><br/>\
                    Location:<br/> <b>{City}, {State}</b>",
                    "style": {"backgroundColor": "blue",
                            "color": "white"}
                    }
        view_state = pdk.ViewState(
            longitude=map_data['Longitude'].mean(),
            latitude=map_data['Latitude'].mean(),
            zoom=10,
            pitch=0
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[Longitude, Latitude]",
            get_color="[255, 30, 0, 160]",
            get_radius=1000,
            pickable=True
        )
        icon_layer = pdk.Layer(
            type='IconLayer',
            data=map_data,
            get_icon=icon_data['url'],
            get_size=5,
            size_scale=15,
            get_position='[Longitude, Latitude]',
            get_radius = 1000,
            pickable = True
        )

        map = pdk.Deck(
            map_style="mapbox://styles/mapbox/navigation-day-v1",
            initial_view_state=view_state,
            layers=[icon_layer, layer],
            tooltip=tool_tip
        )
        st.pydeck_chart(map)

    def page3():
        st.header("Coaster Speed & Height Data")
        st.write("This Page Allows You to View Coasters by Speed and Height!")

        sns.scatterplot(data=data_file, x="Max_Height", y="Top_Speed")
        plt.title("Roller Coaster Speed vs. Height", fontsize=20)
        plt.xlabel("Height (feet)", fontsize=15, color='blue')
        plt.ylabel("Speed (mph)", fontsize=15, color='blue')
        plot = plt.gcf()
        st.pyplot(plot)

        heightdata = data_file.sort_values(by=["Max_Height"], ascending=False).reset_index(drop=True)
        st.write("USA Roller Coasters by Height")
        st.write(heightdata[["Coaster", "State", "Max_Height"]])

        speeddata = data_file.sort_values(by=["Top_Speed"], ascending=False).reset_index(drop=True)
        st.write("USA Roller Coasters by Speed")
        st.write(speeddata[["Coaster", "State", "Top_Speed"]])

    # Coaster filter
        columns = ["Coaster", "Park", "City", "State", "Type", "Max_Height", "Top_Speed", "Duration", "Year_Opened", "Num_of_Inversions"]
        selected_columns = st.multiselect("Select columns to display", columns, default=columns)
        sort_by = st.selectbox("Sort by", selected_columns)
        ascending = st.checkbox("Ascending", value=True)
        filtertable = data_file[selected_columns].sort_values(by=sort_by, ascending=ascending)
        st.write("Roller Coaster Filter")
        st.table(filtertable)


    def page4():
        st.header("Coaster Opening & Count by State")
        st.write("This Page Allows You to View Coasters by Opening Year and State!")

        # Chart of number of coasters opened by state each year
        st.write("Number of Coasters Opened Each Year by State")
        data_file["Cumulative_Total"] = data_file.groupby("Year_Opened").cumcount() + 1
        chart = alt.Chart(data_file).mark_bar().encode(
            x="Year_Opened",
            y="count()",
            color="State",
            tooltip=["Cumulative_Total", "count()", "State", "Year_Opened"]
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

        columns = ["Year_Opened", "Cumulative_Total", "State"]
        sort_by = st.selectbox("Sort by", columns)
        yeartable = data_file[columns].sort_values(by=sort_by, ascending=True)
        st.write("Roller Coaster's Opened by Year")
        st.table(yeartable)


pages = {
    "page1": "Home Page",
    "page2": "Coaster Map",
    "page3": "Coaster Speed & Height Data",
    "page4": "Coaster Opening & Count by State"
}

default_page = "page1"
selected_page = st.sidebar.radio("Select a page", list(pages.values()), index=list(pages.keys()).index(default_page))
if selected_page == "Home Page":
    page1()
elif selected_page == "Coaster Map":
    page2()
elif selected_page == "Coaster Speed & Height Data":
    page3()
elif selected_page == "Coaster Opening & Count by State":
    page4()









