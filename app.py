import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Food Delivery Analytics", layout="wide")

@st.cache_data
def load_and_clean_data():
    # Attempt to load the dataset
    try:
        df = pd.read_csv("Food_Delivery_Times.csv")
        
        # Data Cleaning based on source observations:
        # 1. Strip any leading/trailing spaces from column names
        df.columns = df.columns.str.strip()
        
        # 2. Handle missing values found in sources (e.g., rows 313, 549, 939) [1-3]
        # We fill categorical NAs with 'Unknown' and numerical with the median
        df['Weather'] = df['Weather'].fillna('Unknown')
        df['Traffic_Level'] = df['Traffic_Level'].fillna('Unknown')
        df['Time_of_Day'] = df['Time_of_Day'].fillna('Unknown')
        df['Courier_Experience_yrs'] = df['Courier_Experience_yrs'].fillna(df['Courier_Experience_yrs'].median())
        
        return df
    except FileNotFoundError:
        return None

df = load_and_clean_data()

st.title("🚚 Food Delivery Time Analysis")

if df is not None:
    # Sidebar filters using categories identified in the sources [1]
    st.sidebar.header("Filter Deliveries")
    
    # Weather options: Windy, Clear, Foggy, Rainy, Snowy [1]
    weather_list = sorted(df['Weather'].unique().tolist())
    weather = st.sidebar.selectbox("Select Weather", weather_list)
    
    # Traffic levels: Low, Medium, High [1]
    traffic_list = sorted(df['Traffic_Level'].unique().tolist())
    traffic = st.sidebar.selectbox("Traffic Level", traffic_list)
    
    # Vehicle types: Scooter, Bike, Car [1]
    vehicle_list = sorted(df['Vehicle_Type'].unique().tolist())
    vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_list)

    # Filtered View
    filtered_df = df[
        (df['Weather'] == weather) & 
        (df['Traffic_Level'] == traffic) & 
        (df['Vehicle_Type'] == vehicle)
    ]

    # Metrics Display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Trips in Category", len(filtered_df))
    with col2:
        avg_time = filtered_df['Delivery_Time_min'].mean() if not filtered_df.empty else 0
        st.metric("Avg Delivery Time", f"{avg_time:.1f} mins")
    with col3:
        avg_dist = filtered_df['Distance_km'].mean() if not filtered_df.empty else 0
        st.metric("Avg Distance", f"{avg_dist:.1f} km")

    # Historical Data Table
    st.subheader(f"Historical Logs: {weather} Weather / {traffic} Traffic")
    if not filtered_df.empty:
        st.dataframe(filtered_df[['Order_ID', 'Distance_km', 'Time_of_Day', 'Delivery_Time_min']])
    else:
        st.info("No records match these exact criteria in the source data.")

else:
    st.error("Dataset not found! Please ensure 'Food_Delivery_Times.csv' is in your GitHub repository.")

except FileNotFoundError:

    st.error("Please ensure 'Food_Delivery_Times.csv' is uploaded to your GitHub repository.")
