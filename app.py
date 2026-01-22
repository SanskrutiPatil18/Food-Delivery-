import streamlit as st
import pandas as pd
import numpy as np

# Title for the Food Delivery Application
st.set_page_config(page_title="Food Delivery Time Estimator", layout="wide")
st.title("🚚 Food Delivery Use Case Analysis")

# Load the dataset from the sources provided
# Note: Ensure "Food_Delivery_Times.csv" is in the same directory on GitHub
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Delivery_Times.csv")
    return df

try:
    df = load_data()
    st.sidebar.header("Filter/Input Order Details")

    # Feature inputs based on source data categories
    # Weather conditions found in sources: Windy, Clear, Foggy, Rainy, Snowy [1], [2], [4]
    weather_options = ["Clear", "Rainy", "Windy", "Foggy", "Snowy"]
    
    # Traffic levels found in sources: Low, Medium, High [1], [5]
    traffic_options = ["Low", "Medium", "High"]
    
    # Time of day options: Afternoon, Evening, Night, Morning [1], [6]
    time_options = ["Morning", "Afternoon", "Evening", "Night"]
    
    # Vehicle types: Scooter, Bike, Car [1], [2], [3]
    vehicle_options = ["Bike", "Scooter", "Car"]

    # Sidebar UI Elements
    distance = st.sidebar.slider("Distance (km)", 0.5, 20.0, 5.0) # Distances range up to ~19.9km [7]
    weather = st.sidebar.selectbox("Weather Condition", weather_options)
    traffic = st.sidebar.selectbox("Traffic Level", traffic_options)
    time_of_day = st.sidebar.selectbox("Time of Day", time_options)
    vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_options)
    prep_time = st.sidebar.number_input("Preparation Time (min)", 5, 30, 15) # Prep times range up to 29 min [8]
    experience = st.sidebar.number_input("Courier Experience (yrs)", 0, 10, 5) # Experience ranges up to 9 yrs [9]

    # Display basic metrics or filtered data
    st.subheader("Dataset Overview")
    st.write("This application draws insights from delivery logs including order IDs and various environmental factors.") [1]
    st.dataframe(df.head(10))

    # Simple logic to show average delivery time based on selected filters
    st.subheader("Delivery Insight")
    filtered_df = df[(df['Weather'] == weather) & (df['Traffic_Level'] == traffic)]
    
    if not filtered_df.empty:
        avg_time = filtered_df['Delivery_Time_min'].mean()
        st.success(f"Average Delivery Time for {weather} weather with {traffic} traffic: **{avg_time:.2f} minutes**")
    else:
        st.warning("No historical data found for this specific combination. Showing global average.")
        st.info(f"Global Average Delivery Time: **{df['Delivery_Time_min'].mean():.2f} minutes**")

except FileNotFoundError:
    st.error("Please ensure 'Food_Delivery_Times.csv' is uploaded to your GitHub repository.")