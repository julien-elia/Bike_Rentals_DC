import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


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




st.title("Modelling")
st.write("To determine the optimal model and corresponding hyperparameters, we utilized the Pycaret library, which aids in selecting the best option and achieving the highest possible R2 score")

import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pycaret.regression import *
from sklearn.metrics import r2_score
import pickle
from datetime import datetime

#bike_df = pd.read_csv('bike-sharing_hourly.csv') #profile = True to get the insights
from pycaret.datasets import get_data
bike_df = get_data('bike-sharing_hourly', profile=False)

bike_df["Working_Hours"] = np.where((bike_df["workingday"] == 1) & (bike_df["hr"] >= 8) & (bike_df["hr"] <= 17), 1 , 0)
bike_df["Sleeping_Hours"] = np.where(((bike_df["hr"] <= 6) | (bike_df["hr"] >= 23)), 1 , 0)
bike_df["hum_temp_ratio"] = bike_df["hum"] / bike_df["temp"]
bike_df_data = bike_df.drop(columns = ["casual", "registered"], axis = 1)

data = bike_df_data[(bike_df_data["dteday"] >= '2011-01-01') & (bike_df_data["dteday"] < '2012-08-01')]
data_unseen = bike_df_data[(bike_df_data["dteday"] >= '2012-08-01')]

data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)


# Define a function to run the model and store the best model globally
def run_model(models):
    with st.spinner('Running model...'):
        model = setup(data, target="cnt", silent=True)
    # do more things with the model
        best_model = compare_models(include= models)
        tuned_model = tune_model(best_model, fold=5)
        model = finalize_model(tuned_model)
        pipeline = save_model(model, 'cnt_bikes')
            # Feature Importance Plot
        plot_model(tuned_model, plot='feature', save = True)
        plot_model(tuned_model, plot='error', save = True)
        plot_model(tuned_model, plot='residuals', save = True)
        plot_model(tuned_model, plot='learning', save = True)

    col1, col2 = st.columns(2)
    # Ask the user to input the date as a string
    with col1:     
        st.success("Done!")
    with col2:
        st.write(f"Best Model: {best_model}")


    
def main():    
    all_models = ['lr', 'knn', 'ridge', 'dt', 'svm', 'dummy', 'gbr', 'lasso', 'rf', 'br', 'ada', 'et', 'xgboost', 'lightgbm', 'catboost']

    # Create a multiselect widget with all available models
    selected_models = st.multiselect('Select models to include:', all_models, default=all_models)
    st.write("Click the button below to run the model setup.")
    if st.button("Run Model"):
        run_model(selected_models)
    
    
    
    col1, col2 = st.columns(2)
    # Ask the user to input the date as a string
    with col1: 
        option = st.selectbox("Choose model evaluation: ", ("Feature Importance", "Prediction Error", "Residuals", "Learning Curve"))
        if option == "Feature Importance":
            st.image("Feature Importance.png")
        elif option == "Prediction Error":
            st.image("Prediction Error.png")
        elif option == "Residuals":
            st.image("Residuals.png")
        elif option == "Learning Curve":
            st.image("Learning Curve.png")
    with col2:
        model = load_model(model_name="cnt_bikes")
        predictions = predict_model(model, data=data_unseen)
        predictions["Prediction"] = predictions["Label"].round()
        predictions.drop(columns = "Label", axis =1, inplace = True)
        r2 = r2_score(predictions["cnt"], predictions["Prediction"].round())
        st.markdown(f"<h3 style='text-align: center;'>R2 score: {r2:.2f}</h1>", unsafe_allow_html=True)
        
    st.subheader("Predictions" )
    st.write(predictions)
    

    fig = px.line(predictions, x=predictions.dteday, y=['cnt', 'Prediction'], color_discrete_sequence= ['#EF553B', '#00CC96'])
    st.plotly_chart(fig)
    
    test = predictions.drop(columns = "cnt" , axis = 1)
    combined_df = pd.concat([data, test], axis=0)
    fig = px.line(combined_df, x='dteday', y=['cnt' , 'Prediction'])
    # Set the title of the plot
    fig.update_layout(title='Actual vs. Predicted Bike Rentals', xaxis_title='Date', yaxis_title='Number of Rentals')
    # Show the plot in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
