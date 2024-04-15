import streamlit as st
import pandas as pd


st.markdown("<h1 style='text-align: center; color: #191970 ;'>Vehicle Sales Data Visulaisation Dashboard</h1>", unsafe_allow_html=True)
image_url = "https://www.cars.com/images/sell/sale-dealer-woman.jpg"
st.image(image_url , use_column_width=True)

st.markdown(''' 
            * This web application represent a EDA Visualisation for Vehicle Sales Data Set 
            * The Data is obtained from [Kaggle](https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data)
            * You can select one of the options from the sidebar to Explore the data.''')
st.markdown("""
This Vehicle Sales  Dashboard appears to contain information about various car models and their associated prices. It likely includes columns for:

* **Model:** The name or identifier of the car model.
* **Year:** The year the car was manufactured.
* **Condition:** The overall condition of the car (e.g., excellent, good, fair).
* **Odometer:** The total mileage recorded on the car's odometer.
* **MMR (possibly Market Median Retail):** An estimated average market price for the car.
* **Selling Price:** The actual selling price of the car.

**Additional characteristics:**

* The number of columns and their exact names might vary depending on the specific dataset.
* The code assumes the presence of a "models" column, which is used for visualizations based on car models (e.g., Top 10 cars by a particular feature).
* It's possible there are other columns containing additional car-related information not explicitly mentioned in the code (e.g., engine type, transmission, features).

**Overall, this dataset seems suitable for analyzing car prices and identifying trends based on various factors like model year, condition, mileage, and market estimates.**
""")
vehicle = pd.read_csv('car_prices.csv')

vehicle.dropna(inplace=True)
st.subheader('After All Here is The Sample Of Dataset')
if st.checkbox('Show Dataset'):
    st.dataframe(vehicle.head(5))