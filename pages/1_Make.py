import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('car_prices.csv')

# Drop NaN values
df.dropna(inplace=True)

# Page header
st.header("Insights of Car Prices by Make")
st.markdown("Explore various metrics by car make, including bar, scatter, line, and pie charts.")

# Dropdown for selecting interest option
interest_options = ['year', 'condition', 'odometer', 'mmr', 'sellingprice']
interest = st.selectbox('Select Your Option', interest_options)

# Bar chart for top 10
mydf = df.nlargest(10, interest)
st.plotly_chart(px.bar(mydf, x='make', y=interest, title=f'Top 10 {interest}', color='make'), use_container_width=True)

# Scatter plot
st.header(f"Scatter Plot of Make vs. {interest}")
fig_scatter = px.scatter(df, x='make', y=interest, color='make')
st.plotly_chart(fig_scatter, use_container_width=True)

# Line chart
st.header(f"Line Chart of Make vs. {interest}")
fig_line = px.line(df, x='make', y=interest, color='make', title=f'Line Chart of Make vs. {interest}')
st.plotly_chart(fig_line, use_container_width=True)

# Pie chart
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
