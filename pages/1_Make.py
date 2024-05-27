import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv(r'E:/AI/Notebooks/car_prices.csv')
df.dropna(inplace=True)

# Convert 'saledate' to datetime format and create 'month' and 'day' columns
df['saledate'] = pd.to_datetime(df['saledate'])
df['month'] = df['saledate'].dt.month
df['day'] = df['saledate'].dt.day

# Page header
st.header("Insights of Make")
st.markdown("Make: The manufacturer of the car (e.g., Ford, Kia, Chevrolet)")

# Dropdown for selecting interest option
interest_options = ['year', 'condition', 'odometer', 'mmr', 'sellingprice', 'month', 'day']
interest = st.selectbox('Select Your Option', interest_options)

# Bar chart for top 10
mydf = df.nlargest(10, interest)
st.plotly_chart(px.bar(mydf, x='make', y=interest, title=f'Top 10 {interest}', color='make'), use_container_width=True)

# Feature options for scatter plot
feature_options = df.columns.tolist()
feature_options.remove('make')

# Scatter plot
st.header(f"Scatter Plot of Make vs. {interest}")
fig_scatter = px.scatter(df, x='make', y=interest, color='make')
st.plotly_chart(fig_scatter, use_container_width=True)

# Pie Chart (assuming categorical Y-axis)
if df[interest].dtype == "object":
    st.header(f"Distribution of Cars by {interest}")
    fig_pie = px.pie(df, names=interest, title=f'Distribution of Cars by {interest}')
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.write(f"Pie chart not suitable for continuous Y-axis ({interest}).")

# Metrics
max_value = df[interest].max()
min_value = df[interest].min()
avg_value = round(df[interest].mean(), 1)

col1, col2, col3 = st.columns(3)
col1.metric(label=f'Max {interest}', value=max_value)
col2.metric(label=f'Min {interest}', value=min_value)
col3.metric(label=f'Avg {interest}', value=avg_value)

# Top 10 table
col1.markdown(f'<h2 style="text-align: center; color: #191970;">Top 10 {interest}</h2>', unsafe_allow_html=True)
top_df = df.nlargest(10, interest)
col1.dataframe(top_df)

# Bottom 10 table
col2.markdown(f'<h2 style="text-align: center; color: #191970;">Bottom 10 {interest}</h2>', unsafe_allow_html=True)
bottom_df = df.nsmallest(10, interest)
col2.dataframe(bottom_df)
