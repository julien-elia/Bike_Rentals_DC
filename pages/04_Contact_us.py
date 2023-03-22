import geopandas
import streamlit as st
import numpy as np
import plotly.express as px
import glob

#df_init = pd.read_csv('bike-sharing_hourly.csv')

  
from PIL import Image


# Include the Bootstrap stylesheet in the head section of the Streamlit app
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" crossorigin="anonymous">', unsafe_allow_html=True)

# Define the navbar as a function


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






# Call the navbar function in your Streamlit app

navbar()

with st.container():
    st.title("Team Members")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("Maha.png", width=150)
        st.text("Maha Hamdi")
        st.markdown("mahahamdi@student.ie.edu", unsafe_allow_html=True)
    with col2:
        st.image("Julien.png", width=150)
        st.text("Julien Elia")  
        st.markdown("julien.elia@student.ie.edu", unsafe_allow_html=True)        
    with col3:
        st.image("walid.png", width=150)
        st.text("Walid Mneymneh")
        st.markdown("walid.mneymneh@student.ie.edu", unsafe_allow_html=True)
        
    col4, col5, col6 = st.columns(3)
    with col4:
        st.image("Alex.png", width=150)
        st.text("Alex García")
        st.markdown("alex.eaton@student.ie.edu", unsafe_allow_html=True)

    with col5:
        st.image("philip.png", width=150)
        st.text("Philipp Klement")
        st.markdown("philipp.klement@student.ie.edu", unsafe_allow_html=True)

    with col6:
        st.image("guiermo.png", width=150)
        st.text("GuillermoLópez") 
        st.markdown("guillermo.lmd@student.ie.edu", unsafe_allow_html=True)


    col7, col8 = st.columns(2)
    with col7:
        st.image("Gustavo.png", width=150)
        st.text("Gustavo Welsh")
        st.markdown("gustavo.welsh@student.ie.edu", unsafe_allow_html=True)



