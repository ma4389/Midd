import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


df = pd.read_csv('car_prices.csv')
st.header("Insights of Seller")
st.markdown("Seller: The entity selling the car (e.g., Kia Motors America Inc, Enterprise Vehicle Exchange)")
has_seller_column = "seller" in df.columns
if not has_seller_column:
    st.error("The 'seller' column is not available in the dataset.")
    st.stop()  # Stop execution if seller column is missing


interest_options = df.select_dtypes(include=[np.number]).columns.tolist()  # Get numerical columns
if interest_options:
    interest = st.sidebar.selectbox("Select Feature for Analysis", interest_options)
    max_value = df[interest].max()
    min_value = df[interest].min()
    avg_value = round(df[interest].mean(), 1)
    st.metric(label=f"Max {interest}", value=max_value)
    st.metric(label=f"Min {interest}", value=min_value)
    st.metric(label=f"Avg {interest}", value=avg_value)

    mydf = df.nlargest(10, interest)
    st.plotly_chart(px.bar(mydf, x="seller", y=interest, title=f"Top 10 {interest}" , color = 'seller'), use_container_width=True)
else:
    st.write("No numerical columns found for seller analysis.")
st.header(f"Line Plot of seller vs. {interest}")
fig_scatter = px.scatter(df, x='seller', y=interest)
st.plotly_chart(fig_scatter, use_container_width=True)


if df[interest].dtype == "object":
  st.header(f"Distribution of Cars by {interest}")
  fig_pie = px.pie(df, names=interest, values=df.groupby(interest)['seller'].count().reset_index()['seller'])  # Count cars by interest category
  st.plotly_chart(fig_pie, use_container_width=True)
else:
  st.write(f"Pie chart not suitable for continuous Y-axis ({interest}).")
# Top 10/Bottom 10 data
if interest_options:
    top_df = df.nlargest(10, interest)
    bottom_df = df.nsmallest(10, interest)

    col1, col2 = st.columns(2)
    col1.markdown(f'<h2 style="text-align: center; color: #191970 ;">Top 10 {interest}</h2>', unsafe_allow_html=True)
    col1.dataframe(top_df)

    col2.markdown(f'<h2 style="text-align: center; color: #191970 ;">Bottom 10 {interest}</h2>', unsafe_allow_html=True)
    col2.dataframe(bottom_df)
else:
    st.write("No numerical columns found for Top 10/Bottom 10 analysis.")
