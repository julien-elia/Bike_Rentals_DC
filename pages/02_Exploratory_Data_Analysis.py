

import hydralit_components as hc
import pandas as pd

import geopandas
import streamlit as st
import numpy as np
import plotly.graph_objects as go

import plotly.express as px

#df_init = pd.read_csv('bike-sharing_hourly.csv')

  
from PIL import Image

st.set_page_config(
    page_title="Real-Time Data Dashboard",
    page_icon="Active",
    layout="wide"
)
# Include the Bootstrap stylesheet in the head section of the Streamlit app
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" crossorigin="anonymous">', unsafe_allow_html=True)

# Define the navbar as a function
# image = Image.open('image.png')


def navbar():
	st.markdown(""" <style>.navbar-brand{padding-top: 50px;}</style>

    <nav class="navbar navbar-expand-lg navbar-dark navbar navbar-dark bg-dark fixed-top" style="height: 120px;">
        <a class = "navbar-brand" href="#"><img src="" width="40p"></a>
    	<a class = "navbar-brand" href="#"><img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="200p" style="height: 120px;"></a>
    	<a class = "navbar-brand" href="#"><img src="" width="40p"></a>
    	# <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    	# 	<span class="navbar-toggler-icon"></span>
  		# </button>
  		<div class="collapse navbar-collapse" id="navbarNav">
    		<ul class="navbar-nav">
                <li class="nav-item">
        			<a  class="navbar-brand"class="nav-link" href="http://localhost:8501">Home</a>
      			</li>
      			<li class="nav-item">
        			<a  class="navbar-brand"class="nav-link" href="https://github.com/julien-elia/Bike_Rentals_DC">Source Code</a>
      			</li>
      			<li class="nav-item">
        			<a class="navbar-brand" class="nav-link" href="https://weather.com/weather/tenday/l/Washington+DC?canonicalCityId=4c0ca6d01716c299f53606df83d99d5eb96b2ee0efbe3cd15d35ddd29dee93b2">Weather in DC</a>
      			</li> 
                <li class="nav-item">
        			<a class="navbar-brand" class="nav-link" href="https://capitalbikeshare.com/explore">Learn more</a>
      			</li>               
      		</ul>
  		</div>      
    </nav>
    """, unsafe_allow_html=True)






navbar()
st.title("Exploratory Data Analysis")
st.write("In this analysis, we will explore the trends of bike rentals in 2011 and 2012 using Exploratory Data Analysis techniques, which will allow us to uncover patterns and insights that can inform future bike rental strategies.")
bike_df = pd.read_csv('bike-sharing_hourly.csv')
bike_df = bike_df.rename(columns={'yr': 'Year','hr':'Hour','mnth': 'Month','temp': 'Temperature', 'cnt': 'Count'})


season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
bike_df['season'] = bike_df['season'].replace(season_map)
weekday_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
bike_df['weekday'] = bike_df['weekday'].replace(weekday_map)




# Group by
df_date = bike_df.groupby(['dteday']).mean()
df_date = df_date.reset_index()

df_season = bike_df.groupby(['Year','season']).mean()
df_season = df_season.reset_index()

df_weekday = bike_df.groupby(['Year','weekday','Hour']).mean()
df_weekday = df_weekday.reset_index()

df_Year = bike_df.groupby(['Year']).mean()
df_Year = df_Year.reset_index()

df_hr = bike_df.groupby(['Year','Hour']).sum()
df_hr = df_hr.reset_index()

fig = px.line(df_date, x='dteday', y='Count')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
st.subheader('Bikes Rented Trends in 2011 & 2012')
st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns(2)

with col1:
	input = st.selectbox('Select the year for which you want to see the plots',('2011','2012'))

with col2:
	options = st.multiselect('Which question(s) do you want answered:',['What percentage of users are casual and what percentage are registered?', 
								    								'When are bikes most commonly used?', 
																	'What season sees the highest bike usage?', 
																	'Is there any correlation between bike usage and temperature?', 
																	'Which weekday experiences the highest bike usage?'], ['When are bikes most commonly used?', 
																	'What season sees the highest bike usage?'])




i = 0
if input == '2011':
	i = 0
else:
	i = 1
labels =['casual','registered']
values = [int(df_Year.loc[df_Year.Year == i]['casual']), int(df_Year.loc[df_Year.Year == i]['registered'])]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)
col9, col10 = st.columns(2)

for index in options:
	with col1:
		if index == 'Is there any correlation between bike usage and temperature?':
			fig4 = px.scatter(x=df_date.loc[df_date.Year == i]['Temperature'], y=df_date.loc[df_date.Year == i]['Count'])
			st.subheader("The Impact of Temperature on Bike Usage")
			st.plotly_chart(fig4, use_container_width=True)
	with col2:
		if index == 'Is there any correlation between bike usage and temperature?':
			st.subheader("Insights:")
			st.write("This plot shows us that, as expected, the number of rented bikes increases when the temperature is more enjoyable. This is why we see a slight decrease in these numbers when the temperature gets too hot.")

	with col3:
		if index == 'What percentage of users are casual and what percentage are registered?':
			fig6 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
			st.subheader("Proportion of Casual and Registered Users")
			st.plotly_chart(fig6, use_container_width=True)
	with col4:
		if index == 'What percentage of users are casual and what percentage are registered?':
			st.subheader("Insights:")
			st.write("While the majority of users are registered users, 20% of them remain casual users")
	with col5:
		if index == 'When are bikes most commonly used?':
			fig1 = px.line(df_weekday.loc[df_weekday.Year == i], x="Hour", y="Count", color='weekday')
			st.subheader("Hourly/Daily Bike Usage Patterns")
			st.plotly_chart(fig1, use_container_width=True)
	with col6:
		if index == 'When are bikes most commonly used?':
			st.subheader("Insights:")
			st.write("We notice that the number of rented bikes peaks on rush hour (between 8:00-9:00 and 17:00-19:00). However, this trend is inverted on weekends, where most rentals occur during the day (from 10:00 to 16:00)")
	with col7:
		if index == 'What season sees the highest bike usage?':
			fig2 = px.bar(df_season.loc[df_season.Year == i], y='Count', x='season', text_auto='.2s')
			st.subheader("Comparison of Bike Usage Across Seasons")
			st.plotly_chart(fig2, use_container_width=True)
	with col8:
		if index == 'What season sees the highest bike usage?':
			st.subheader("Insights:")
			st.write("The overall amount of users remains constant in Fall, Winter and Summer, but we see a decrease of more than 50% in Spring.")
	with col9:
		if index == 'Which weekday experiences the highest bike usage?':
			fig5 = px.bar(df_weekday.loc[df_weekday.Year == i], y='Count', x='weekday', text_auto='.2s')
			st.subheader("Comparison of Bike Usage Across Week days")
			st.plotly_chart(fig5, use_container_width=True)
	with col10:
		if index == 'Which weekday experiences the highest bike usage?':
			st.subheader("Insights")
			st.write("Sunday is the day with the lowest number of users. The number of users then increases throughout the week and peaks on Saturday.")


import plotly.graph_objects as go
import pandas as pd

# Define mapbox access token
mapbox_access_token = 'pk.eyJ1IjoibWFoYW1haGFtIiwiYSI6ImNsZmVmbzB5NzBsdzYzdGxycDVrbGhwczkifQ.3tBOuJe1-EeMkkCUJ2BizA'

# Define the center coordinates and zoom level of the map
center_lat = 38.9072
center_lon = -77.0369
zoom = 10

# Define the locations of interest
locations = {
    'Logan Circle': {'lat': 38.9097, 'lon': -77.031978},
    'Navy Yard': {'lat': 38.8765, 'lon': -77.0006},
    'Georgetown': {'lat': 38.909675, 'lon': -77.0654},
    'Capitol hill': {'lat': 38.8860, 'lon': -76.9995},
    'Downtown': {'lat': 38.9037, 'lon': -77.0363},
    'Brightwood': {'lat': 38.9649, 'lon': -77.0277},
    'Northwest Washington': {'lat': 38.9381, 'lon': -77.0449}
}

# Define the color for each neighborhood


# Define the data for the map
data = []
for neighborhood, location in locations.items():
    data.append(go.Scattermapbox(
        lat=[location['lat']],
        lon=[location['lon']],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=20,
            symbol='circle',
            color='rgb(194, 24, 7)',
            opacity=0.8
        ),
        name=neighborhood
    ))

# Define the layout for the map

layout = go.Layout(
    autosize=True,
    hovermode='x',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=center_lat,
            lon=center_lon
        ),
        pitch=0,
        zoom=zoom,
        style='light'
    ),
)

# Create the figure and plot the map
fig = go.Figure(data=data, layout=layout)
fig.update_traces(showlegend=False)
st.subheader("Neighborhoods of Interest in Washington DC")
st.write('''
    As shown in the previous graphs, the number of users during the week is much larger at rush hour, we therefore suggest putting more bikes in residential neighbourhoods in the mornings, and in business districts during the day.
    ''')
st.plotly_chart(fig, use_container_width=True)
st.subheader("General Conclusions")
# st.markdown("As shown in the previous graphs, the number of users during the week is much larger at rush hour, we therefore suggest putting more bikes in residential neighbourhoods in the mornings, and in business districts during the day.")
# st.markdown("Some interesting insights about this dataset are dead periods, periods of time during the day or during the year where the bike rentals drastically decrease. For example, during the week, outside rush hours, we see a decrease of almost 50% in the number of rented bikes. We see a similiar 50% overall decrease in the Spring season. These insights could be useful for the company to create targetted advertising and promotion to encourage people to rent more bikes during these periods. Another insight can be found by looking at the number of casual users. In both years, we notice that almost 20% of users are not registered. The company should therefore look deeper into these and encourage these casual users to become registered ones. On the other hand, these observations helped us create new features that can be useful to predict the hourly number of rented bikes. Firstly, we saw a clear distinction between day and night, and weekdays and weekend. We therefore created the features Working_Hours, indicating whether a time point occurs between Monday and Friday, from 8:00 to 17:00, and Sleeping_Hours to distinguish daytime from nighttime. The other added feature hum_temp_ratio, calculates the ratio between the humidity and the temperatures, since there is a clear correlation between the weather and the number of rented bikes.")
st.write('''Some interesting insights about this dataset are "dead periods", periods of time during the day or during the year where the bike rentals drastically decrease. For example, during the week, outside rush hours, we see a decrease ofalmost 50% in the number of rented bikes. We see a similiar 50% overall decrease in the Spring season. These insights could be useful for the company to create targetted advertising and promotion to encourage people to rent more bikes during these periods.
Another insight can be found by looking at the number of "casual" users. In both years, we notice that almost 20% of users are not registered. The company should therefore look deeper into these and encourage these casual users to become registered ones.
On the other hand, these observations helped us create new features that can be useful to predict the hourly number of rented bikes. Firstly, we saw a clear distinction between day and night, and weekdays and weekend. We therefore created the features "Working_Hours", indicating whether a time point occurs between Monday and Friday, from 8:00 to 17:00, and "Sleeping_Hours" to distinguish daytime from nighttime. The other added feature "hum_temp_ratio", calculates the ratio between the humidity and the temperatures, since there is a clear correlation between the weather and the number of rented bikes.''')
